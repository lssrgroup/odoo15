from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Task(models.Model):
    _inherit = 'project.task'

    def compute_fields_visible(self):
        for rec in self:
            rec.company_visible = False
            rec.company_name_visible = False
            rec.client_name_visible = False
            rec.client_email_visible = False
            rec.monthly_fees_visible = False
            rec.product_id_visible = False
            rec.paid_from_visible = False
            rec.paid_to_visible = False
            rec.lead_source_visible = False
            rec.proposal_visible = False
            rec.client_phone_visible = False
            rec.payment_visible = False
            rec.share_holding_visible = False
            rec.client_website_visible = False
            rec.client_country_visible = False
            rec.company_type_visible = False
            project = rec.search([('parent_id', 'child_of', rec.id)]).mapped('project_id')
            if project:
                fields = project.visible_fields.mapped('name')
                if 'res_company_id' in fields:
                    rec.company_visible = True
                if 'company_name' in fields:
                    rec.company_name_visible = True
                if 'client_name' in fields:
                    rec.client_name_visible = True
                if 'client_email' in fields:
                    rec.client_email_visible = True
                if 'monthly_fees' in fields:
                    rec.monthly_fees_visible = True
                if 'product_id' in fields:
                    rec.product_id_visible = True
                if 'paid_from' in fields:
                    rec.paid_from_visible = True
                if 'paid_to' in fields:
                    rec.paid_to_visible = True
                if 'lead_source' in fields:
                    rec.lead_source_visible = True
                if 'proposal' in fields:
                    rec.proposal_visible = True
                if 'client_phone' in fields:
                    rec.client_phone_visible = True
                if 'payment' in fields:
                    rec.payment_visible = True
                if 'share_holding' in fields:
                    rec.share_holding_visible = True
                if 'client_website' in fields:
                    rec.client_website_visible = True
                if 'client_country' in fields:
                    rec.client_country_visible = True
                if 'company_type' in fields:
                    rec.company_type_visible = True




    proposal = [('Saint Vincent FX Company', 'Saint Vincent FX Company'),
                ('Saint Vincent Crypto Company', 'Saint Vincent Crypto Company'),
                ('UK LTD Company', 'UK LTD Company'),
                ('Seychelles IBC', 'Seychelles IBC'),
                ('Mauritius Inv Dealers License', 'Mauritius Inv Dealers License'),
                ('Seychelles Securities License', 'Seychelles Securities License'),
                ('Cyprus CIF License', 'Cyprus CIF License'),
                ('Labuan Money Broking License', 'Labuan Money Broking License'),
                ('Mauritius PIS License', 'Mauritius PIS License'),
                ('RAK IBC', 'RAK IBC'),
                ('RAK FZE', 'RAK FZE'),
                ('Mauritius AC', 'Mauritius AC')]

    payment = [("Bank Wire - USD , EUR , GBP", "Bank Wire - USD , EUR , GBP"),
               ("BTC", "BTC"),
               ("INR - Payment Link / Bank Transfer", "INR - Payment Link / Bank Transfer"),
               ("USDT - ERC20 / TRC20", "USDT - ERC20 / TRC20"),
               ("Paypal - 5% Processing Fees Apply", "Paypal - 5% Processing Fees Apply"),
               ("Credit / Debit Card - 5% Processing Fees Apply", "Credit / Debit Card - 5% Processing Fees Apply"),
               ("SKIP - I HAVE ALREADY PAID", "SKIP - I HAVE ALREADY PAID")]

    task_priority = fields.Selection(
        selection=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Very Urgent')],
        string='Priority', default='low')
    res_company_id = fields.Many2one('res.company', string='Company')
    company_name = fields.Char(string='Company Name')
    client_name = fields.Char('Client Name')
    client_email = fields.Char('Client Email')
    monthly_fees = fields.Char('Monthly Fees')
    product_id = fields.Many2one('product.product', string='Product')
    paid_from = fields.Many2one('res.partner.bank', string='Paid From')
    paid_to = fields.Many2one('res.partner', string='Paid To')
    lead_source = fields.Selection(
        selection=[('match_trade', 'Match Trade'), ('metaquotes', 'Metaquotes'), ('partner', 'Partner'),
                   ('organic', 'Organic')], string="Lead Source")
    proposal = fields.Selection(selection=proposal, string="Proposal")
    client_phone = fields.Char('Phone')
    payment = fields.Selection(selection=payment, string="Payment Options")
    share_holding = fields.Text('Company Share Holders')
    client_website = fields.Char('Website Address')
    client_country = fields.Char('Country')
    company_type = fields.Selection(selection=[("BC - Business Company", "BC - Business Company"),
                                               ("LLC - Limited Liablity Company", "LLC - Limited Liablity Company")],
                                    string="Company Type")

    company_visible = fields.Boolean('company visible', compute='compute_fields_visible')
    company_name_visible = fields.Boolean('company name visible', compute='compute_fields_visible')
    client_name_visible = fields.Boolean('client name visible', compute='compute_fields_visible')
    client_email_visible = fields.Boolean('client email visible', compute='compute_fields_visible')
    monthly_fees_visible = fields.Boolean('Monthly fees visible', compute='compute_fields_visible')
    product_id_visible = fields.Boolean('product_id_visible', compute='compute_fields_visible')
    paid_from_visible = fields.Boolean('paid_from_visible', compute='compute_fields_visible')
    paid_to_visible = fields.Boolean('paid_to_visible', compute='compute_fields_visible')
    lead_source_visible = fields.Boolean('lead_source_visible', compute='compute_fields_visible')
    proposal_visible = fields.Boolean('proposal_visible', compute='compute_fields_visible')
    client_phone_visible = fields.Boolean('client_phone_visible', compute='compute_fields_visible')
    payment_visible = fields.Boolean('company_visible', compute='compute_fields_visible')
    share_holding_visible = fields.Boolean('company_visible', compute='compute_fields_visible')
    client_website_visible = fields.Boolean('company_visible', compute='compute_fields_visible')
    client_country_visible = fields.Boolean('company_visible', compute='compute_fields_visible')
    company_type_visible = fields.Boolean('company_visible', compute='compute_fields_visible')

    @api.constrains('stage_id')
    def create_new_task_for_new_project(self):
        if self.stage_id.is_closed:
            if self.project_id and self.project_id.trigger_create_new_task:
                if not self.project_id.new_task_project:
                    raise ValidationError('Please Assign The Project where the task is needed to be created')
                new_task = self.copy()
                new_task.write({
                    'project_id': self.project_id.new_task_project.id,
                    'stage_id': self.project_id.new_stage.id
                })


