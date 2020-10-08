# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

try:
    import erppeek
except Exception:
    raise ValidationError('La libraire de synchronisation est manquante!')

import psycopg2

class AccountInvoiceSynch(models.TransientModel):
    _name = 'account.invoice.synch'


    def get_account(self, client, account_id):
        remote_account = False
        line_account_id = client.search('account.account', [('code', '=', account_id.code)])
        if line_account_id:
            remote_account = line_account_id[0]
        else:
            user_type = client.search('account.account.type',
                                       [('name', '=', account_id.user_type_id.name)],
                                      )
            if not user_type:
                raise ValidationError(u'Type de compte %s non trouvé!' %(account_id.user_type_id.name, ))

            line_account_id = client.create('account.account',{'code': account_id.code,
                                                                      'name': account_id.name,
                                                                      'user_type_id': user_type[0]
                                                                      })
            remote_account = line_account_id
            return remote_account


    def synchronise_invoice(self):
        active_ids = self._context.get('active_ids')
        invoice_ids = self.env['account.move'].search([('id', 'in', active_ids)])
        new_invoices = []
        # Verifier si toutes les factures selectionnées sont validées
        if any(not x.name or x.name == '/' for x in invoice_ids):
            raise ValidationError('Toutes les factures à synchroniser doivent avoir un numéro!')

        #  connection a la base fisc avec erppeek

        SERVER = self.env.user.company_id.second_base_url
        client = erppeek.Client(server=SERVER)
        client.context = {'lang': self.env.user.lang}
        try:
            client.login(database=self.env.user.company_id.db_name,
                         user=self.env.user.company_id.admin_user, password=self.env.user.company_id.admin_password)
        except Exception as e:
            raise ValidationError('Erreur de connection à la deuxième base')

        for invoice in invoice_ids:
            #  verifier si la facture n'est pas deja synchronisée

            sync_invoice = client.search('account.move', [('synch_id', '=', invoice.id)])

            #  Préparation du dictionnaire de la facture
            if not sync_invoice:
                vals= {'name': invoice.name,
                       'invoice_date': invoice.invoice_date,
                       'invoice_date_due': invoice.invoice_date_due,
                       'synch_id': invoice.id,
                       'type': invoice.type,
                       'ref':invoice.ref,
                       'invoice_origin': invoice.invoice_origin,
                       }

                invoice_partner = invoice.partner_id
                invoice_user = invoice.user_id
                if invoice.fiscal_position_id:
                    fp_id = client.search('account.fiscal.position', [('name', '=', invoice.fiscal_position_id.name)],
                                          )
                    if fp_id:
                        vals['fiscal_position_id'] =  fp_id[0]
                    else:
                        raise ValidationError(u'Veuillez créer la position fiscale %s sur la base fiscal'%(invoice.fiscal_position_id.name))
                #  Rechercher le partenaire sinon le créer

                partner_id = client.search('res.partner', [('synch_id', '=', invoice_partner.id)],
                                 )
                if partner_id:
                    vals['partner_id'] = partner_id[0]
                else:
                    position = False
                    if invoice_partner.property_account_position_id:
                        fp_id = client.search('account.fiscal.position',
                                              [('name', '=', invoice_partner.property_account_position_id.name)],
                                              )
                        if fp_id:
                            position = fp_id[0]
                        else:
                            raise ValidationError(u'Veuillez créer la position fiscale du partenaire %s sur la base fiscal' % (
                                invoice_partner.property_account_position_id.name))
                    print('fffffffffffffposition', position)
                    partner_vals = {'name': invoice_partner.name,
                                                                  'street': invoice_partner.street,
                                                                  'street2': invoice_partner.street2,
                                                                  'city': invoice_partner.city,
                                                                  'phone': invoice_partner.phone,
                                                                  'mobile': invoice_partner.mobile,
                                                                  'email': invoice_partner.email,
                                                                  'ref': invoice_partner.ref,
                                                                  'synch_id': invoice_partner.id,
                                                                  'supplier_rank': invoice_partner.supplier_rank,
                                                                  'customer_rank': invoice_partner.customer_rank,
                                                                  'zip': invoice_partner.zip,
                                                                  'country_id': invoice_partner.country_id and invoice_partner.country_id.id or False

                                                                  }
                    if position:
                        partner_vals['property_account_position_id'] = position
                    partner = client.create('res.partner', partner_vals)

                    vals['partner_id'] = partner



                #  Rechercher le vendeur sinon le créer

                user_id = client.search('res.users', [('name', '=', invoice_user.name)])
                if user_id:
                    vals['user_id'] = user_id[0]
                # Recherche du journal
                journal_id = client.search('account.journal', [('name', '=', invoice.journal_id.name)])
                if journal_id:
                    vals['journal_id'] = journal_id[0]
                else:
                    raise ValidationError("Le journal %s n'a pas pu être repéré dans la base de destination" %(invoice.journal_id.name,))
                #  Rechercher les conditions de paiements
                if invoice.invoice_payment_term_id:
                    self.env.cr.execute("""select name from account_payment_term where id =%s""", (invoice.invoice_payment_term_id.id,))
                    term_name = self.env.cr.fetchone()

                    payment_term = client.search('account.payment.term', [('name', '=',  invoice.invoice_payment_term_id.name)])

                    if payment_term:
                        vals['invoice_payment_term_id'] = payment_term[0]
                    else:
                        raise ValidationError("la conditions de paiement %s n'est pas disponible dans la base fiscale. Merci de la créer " %invoice.invoice_payment_term_id.name)
                if invoice.currency_id:
                    currency = client.search('res.currency', [('name', '=', invoice.currency_id.name)])
                    if currency:
                        vals['currency_id'] = currency[0]
                    else:
                        raise ValidationError('Merci de créer ou activer la devise %s' (invoice.currency_id.name))

                lines = []
                #  Création des lignes de la facture

                for line in invoice.invoice_line_ids:
                    line_vals = {'name': line.name,
                                 'quantity':line.quantity,
                                 'price_unit': line.price_unit,
                                 }
                    if line.product_id:
                        #  Rechercher l'article sinon le créer

                        # cur.execute(
                        #     """SELECT * from product_product  where synch_id = %s""",
                        #     (line.product_id.id,))
                        # product_id = cur.fetchone()
                        product_id = client.search('product.product', [('synch_id', '=', line.product_id.id)])

                        if product_id:
                            line_vals['product_id'] = product_id[0]
                        else:
                            product_val = {'name': line.product_id.name,
                                           'default_code': line.product_id.default_code,
                                           'lst_price':line.product_id.lst_price,
                                           'standard_price':line.product_id.standard_price,
                                           'synch_id':line.product_id.id
                                           }
                            #  Rechercher la categorie de l'article sinon la créer

                            categ_id = client.search('product.category', [('synch_id', '=', line.product_id.categ_id.id)])

                            if categ_id:
                                product_val['categ_id'] = categ_id[0]
                            if not categ_id:
                                categ_vals = {'name': line.product_id.categ_id.name, 'synch_id':line.product_id.categ_id.id}
                                if line.product_id.categ_id.parent_id:

                                    parent_categ = client.search('product.category',
                                                             [('synch_id', '=', line.product_id.categ_id.parent_id.id)])

                                    if parent_categ:
                                        categ_vals['parent_id'] = parent_categ[0]
                                categ_id = client.create('product.category', categ_vals)
                                product_val['categ_id'] = categ_id
                            product = client.create('product.product',product_val)
                            line_vals['product_id'] = product
                    #  Rechercher le compte de la ligne sinon le créer

                    if line.account_id:


                            line_vals['account_id'] = self.get_account(client, line.account_id)
                    taxes = []
                    if line.tax_ids:
                        for tax in line.tax_ids:

                            taxe = client.search('account.tax', [('name', '=', tax.name), ('type_tax_use', '=', tax.type_tax_use),
                                                                 ('amount_type', '=', tax.amount_type), ('amount', '=', tax.amount)])

                            if taxe:
                                taxes.append(taxe[0])
                        line_vals['tax_ids']= [(6,0,taxes)]
                    lines.append((0, 0, line_vals))
                vals['invoice_line_ids'] = lines
                # new_invoice = client.model('account.move').create(vals)
                new_invoice = client.create('account.move', vals)
                model_move = erppeek.Model(client, 'account.move')
                new_invoice_id = model_move.browse(new_invoice)
                invoice.synch_id = new_invoice
                if invoice.state == "posted" and not invoice.partner_id.is_vc:
                    client.execute('account.move', 'remote_action_post', new_invoice)

                    reconciled_moves = invoice.line_ids.mapped('matched_debit_ids.debit_move_id') \
                                       + invoice.line_ids.mapped('matched_credit_ids.credit_move_id')
                    reconciled_payment_ids = reconciled_moves.filtered(lambda move: not move.move_id.is_invoice())
                    if reconciled_payment_ids:
                        payment_remote = client.search('account.payment', [('synch_id', 'in', reconciled_payment_ids.mapped('payment_id').mapped('id'))])
                        if payment_remote:
                            print('new_invoice_id.line_id', new_invoice_id.line_ids)

                            lines = client.search('account.move.line', [('move_id', '=', new_invoice),
                                                                        ('account_internal_type', 'in', ('receivable', 'payable'))])

                            payment_line_id = client.search('account.move.line', [('payment_id', 'in', payment_remote),
                                                                                  ('account_internal_type', 'in', ('receivable', 'payable'))])

                            client.execute('account.move.line','reconcile', lines+payment_line_id )

                        self.env[ 'account.payment.synch'].with_context({'active_ids':reconciled_payment_ids.mapped('payment_id').mapped('id') }).synchronise_payment()
                        print('reconciled_payment_ids', reconciled_payment_ids)

                if invoice.partner_id.is_vc:
                    client.write('account.move', new_invoice,{'nd_move': True} )

                new_invoices.append(new_invoice)

        return new_invoices