from odoo import models, fields, api

from odoo.tools import ustr, pycompat, formataddr, email_normalize, encapsulate_email, email_domain_extract, email_domain_normalize
from collections import defaultdict
from odoo import tools



class MailMail(models.Model):
    _inherit = 'mail.mail'

    def _split_by_mail_configuration(self):
        mail_values = self.read(['id', 'email_from', 'mail_server_id'])

        # First group the <mail.mail> per mail_server_id and per email_from
        group_per_email_from = defaultdict(list)
        for values in mail_values:
            mail_server_id = values['mail_server_id'][0] if values['mail_server_id'] else False
            group_per_email_from[(mail_server_id, values['email_from'])].append(values['id'])

        # Then find the mail server for each email_from and group the <mail.mail>
        # per mail_server_id and smtp_from
        mail_servers = self.env['ir.mail_server'].sudo().search([('company_id', '=', self.env.company.id)], order='sequence')
        group_per_smtp_from = defaultdict(list)
        for (mail_server_id, email_from), mail_ids in group_per_email_from.items():
            if not mail_server_id:
                mail_server, smtp_from = self.env['ir.mail_server']._find_mail_server(email_from, mail_servers)
                mail_server_id = mail_server.id if mail_server else False
            else:
                smtp_from = email_from

            group_per_smtp_from[(mail_server_id, smtp_from)].extend(mail_ids)
        sys_params = self.env['ir.config_parameter'].sudo()
        batch_size = int(sys_params.get_param('mail.session.batch.size', 1000))

        for (mail_server_id, smtp_from), record_ids in group_per_smtp_from.items():
            for batch_ids in tools.split_every(batch_size, record_ids):
                yield mail_server_id, smtp_from, batch_ids


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    company_id = fields.Many2one('res.company', name='Company Id')

    def _find_mail_server(self, email_from, mail_servers=None):
        """Find the appropriate mail server for the given email address.

        Returns: Record<ir.mail_server>, email_from
        - Mail server to use to send the email (None if we use the odoo-bin arguments)
        - Email FROM to use to send the email (in some case, it might be impossible
          to use the given email address directly if no mail server is configured for)
        """
        email_from_normalized = email_normalize(email_from)
        email_from_domain = email_domain_extract(email_from_normalized)
        notifications_email = email_normalize(self._get_default_from_address())
        notifications_domain = email_domain_extract(notifications_email)

        if mail_servers is None:
            mail_servers = self.sudo().search([('company_id', '=', self.env.company.id)], order='sequence')

        # 1. Try to find a mail server for the right mail from
        mail_server = mail_servers.filtered(lambda m: email_normalize(m.from_filter) == email_from_normalized)
        if mail_server:
            return mail_server[0], email_from

        mail_server = mail_servers.filtered(lambda m: email_domain_normalize(m.from_filter) == email_from_domain)
        if mail_server:
            return mail_server[0], email_from

        # 2. Try to find a mail server for <notifications@domain.com>
        if notifications_email:
            mail_server = mail_servers.filtered(lambda m: email_normalize(m.from_filter) == notifications_email)
            if mail_server:
                return mail_server[0], notifications_email

            mail_server = mail_servers.filtered(lambda m: email_domain_normalize(m.from_filter) == notifications_domain)
            if mail_server:
                return mail_server[0], notifications_email

        # 3. Take the first mail server without "from_filter" because
        # nothing else has been found... Will spoof the FROM because
        # we have no other choices
        mail_server = mail_servers.filtered(lambda m: not m.from_filter)
        if mail_server:
            return mail_server[0], email_from

        # 4. Return the first mail server even if it was configured for another domain
        if mail_servers:
            return mail_servers[0], email_from

        # 5: SMTP config in odoo-bin arguments
        from_filter = self.env['ir.config_parameter'].sudo().get_param(
            'mail.default.from_filter', tools.config.get('from_filter'))

        if self._match_from_filter(email_from, from_filter):
            return None, email_from

        if notifications_email and self._match_from_filter(notifications_email, from_filter):
            return None, notifications_email

        return None, email_from
