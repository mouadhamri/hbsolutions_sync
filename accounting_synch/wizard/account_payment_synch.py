# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

try:
    import erppeek
except Exception:
    raise ValidationError('La libraire de synchronisation est manquante!')


class AccountPaymentSynch(models.TransientModel):
    _name = 'account.payment.synch'

    def synchronise_payment(self):
        active_ids = self._context.get('active_ids')
        payment_ids = self.env['account.payment'].search([('id', 'in', active_ids)])


        SERVER = self.env.user.company_id.second_base_url
        client = erppeek.Client(server=SERVER)
        try:
            client.login(database=self.env.user.company_id.db_name,
                         user=self.env.user.company_id.admin_user, password=self.env.user.company_id.admin_password)
        except Exception as e:
            raise ValidationError('Erreur de connection à la deuxième base')

        for payment in payment_ids:
            #  verifier si la facture n'est pas deja synchronisée

            sync_payment = client.search('account.payment', [('synch_id', '=', payment.id)])
            #  Préparation du dictionnaire de la facture
            if not sync_payment:
                vals= {
                    'payment_date': payment.payment_date,
                    'amount': payment.amount,
                    "payment_type": payment.payment_type,
                    "partner_type": payment.partner_type,
                    "communication": payment.communication,
                    'name': payment.name,
                    'synch_id': payment.id
                    }

                payment_partner = payment.partner_id
                #  Rechercher le partenaire sinon le créer

                partner_id = client.search('res.partner', [('synch_id', '=', payment_partner.id)])
                if partner_id:
                    vals['partner_id'] = partner_id[0]
                else:
                    partner = client.create('res.partner',{'name': payment_partner.name,
                                                                  'street': payment_partner.street,
                                                                  'street2': payment_partner.street2,
                                                                  'city': payment_partner.city,
                                                                  'phone': payment_partner.phone,
                                                                  'mobile': payment_partner.mobile,
                                                                  'email': payment_partner.email,
                                                                  'ref': payment_partner.ref,
                                                                  'synch_id': payment_partner.id,
                                                                  'supplier_rank': payment_partner.supplier_rank,
                                                                  'customer_rank': payment_partner.customer_rank,
                                                                  'zip': payment_partner.zip,
                                                                  'country_id': payment_partner.country_id and payment_partner.country_id.id,

                                                                  })
                    vals['partner_id'] = partner.id



                if payment.journal_id:
                    #  Rechercher le journal sinon le créer

                    journal_id = client.search('account.journal', [('name', '=', payment.journal_id.name)])

                    if journal_id:
                        vals['journal_id'] = journal_id[0]
                    else:
                        raise ValidationError("Le journal %s n'a pa pu être reperé dans la base de destination!" % payment.journal_id.name)
                if payment.currency_id:
                    #  Rechercher le journal sinon le créer

                    currency = client.search('res.currency', [('name', '=', payment.currency_id.name)])

                    if currency:
                        vals['currency_id'] = currency[0]
                    else:
                        raise ValidationError("La devise %s n'a pa pu être reperé dans la base de destination!" % payment.currency_id.name)

                payment_method = client.search('account.payment.method',[('code', '=', 'manual'), ('payment_type', '=', payment.payment_type)])
                vals['payment_method_id'] = payment_method[0]
                new_payment = client.create('account.payment',vals)
                payment.synch_id = new_payment
                if payment.state not in ('draft', 'cancelled'):
                    print('payment.invoice_ids', payment.reconciled_invoice_ids)
                    if payment.reconciled_invoice_ids:
                        invoices = client.search('account.move', [('synch_id', 'in', payment.reconciled_invoice_ids.mapped('id'))])
                        print('invoices', invoices)
                        if len(invoices)>0:

                            client.write('account.payment', new_payment, {'invoice_ids': invoices})


                    client.execute('account.payment', 'post', new_payment)
        return True