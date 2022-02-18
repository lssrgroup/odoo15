from odoo import models, fields, api
from odoo.http import request



class Project(models.Model):
    _inherit = 'project.project'

    visible_fields = fields.Many2many('ir.model.fields', string='Visible Fields', invisible=True)
    trigger_create_new_task = fields.Boolean('Create New Task On Completion')
    new_task_project = fields.Many2one('project.project', string='Project')
    new_stage = fields.Many2one('project.task.type', string='Starting Stage')
    get_values_from_webpage = fields.Boolean(string="Get Values From Webpage")
    webpage_id = fields.Many2one('website.page', string="Webpage Id")

    project_website_url = fields.Char('Questionnaire URL', compute='get_questionnaire_url')

    def get_questionnaire_url(self):
        for rec in self:
            rec.project_website_url = False
            if rec.get_values_from_webpage and rec.webpage_id:
                rec.project_website_url = request.httprequest.host_url+rec.webpage_id.url.split('/')[1]


    @api.model
    def load_views(self, views, options=None):
        res = super(Project, self).load_views(views)
        if 'form' in res.get('fields_views'):
            views = res.get('fields_views')
            if 'fields' in views.get('form'):
                form = views.get('form')
                if 'visible_fields' in form.get('fields'):
                    values = form.get('fields').get('visible_fields')
                    fields_in_use = self.env['ir.model.fields'].search(
                        [('model_id.model', '=', 'project.task'),('store','=',True)]).filtered(lambda x: x.modules == 'project_website')
                    values['domain'] = [('id', 'in', fields_in_use.ids)]
        return res
