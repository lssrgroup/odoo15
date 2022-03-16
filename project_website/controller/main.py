from odoo.http import request, route, Controller
import json
import re
import base64
from odoo import _


class ProjectTaskPortalSVG(Controller):
    def prepare_project_task_values(self, values):
        task_vals = {}
        for vals in values:
            if 'attachment_ids' not in vals:
                task_vals[vals] = values[vals]
        return task_vals

    @route(["/svg/submit/<string:model_name>"], type='http', auth="public", methods=['POST'], website=True)
    def create_task_for_svg(self, **post):
        post.pop('model_name')
        values = self.prepare_project_task_values(post)
        project_id = request.env['project.project'].sudo().search([('webpage_id','=', request.env.ref('project_website.st_vincent_incorporation_questionnaire_page').id)])
        if not project_id:
            error = _("Project Is Not Set By The Administrator")
            return json.dumps({
                'error': error,
            })
        values['project_id'] = project_id.id
        values['user_ids'] = [(6, 0, [project_id.user_id.id])]
        values['company_id'] = project_id.company_id.id
        values['name'] = post['client_name']
        task = request.env['project.task']
        task_id = task.sudo().create(values)
        regx = re.compile("^attachment_ids*")
        for attachments in post:
            if regx.match(attachments):
                name = post.get(attachments).filename
                file = post.get(attachments)
                request.env['ir.attachment'].sudo().create({
                    'name': name,
                    'type': 'binary',
                    'datas': base64.b64encode(file.read()),
                    'res_model': task._name,
                    'res_id': task_id.id
                })
        return json.dumps({'id': task_id.id})


class ProjectTaskPortalUK(Controller):

    def prepare_project_task_values(self, values):
        task_vals = {}
        for vals in values:
            if 'attachment_ids' not in vals:
                task_vals[vals] = values[vals]
        return task_vals

    @route(["/uk/submit/<string:model_name>"], type='http', auth="public", methods=['POST'], website=True)
    def create_task_for_svg(self, **post):
        post.pop('model_name')
        values = self.prepare_project_task_values(post)
        project_id = request.env['project.project'].sudo().search(
            [('webpage_id', '=', request.env.ref('project_website.uk_incorporation_questionnaire_page').id)])
        if not project_id:
            error = _("Project Is Not Set By The Administrator")
            return json.dumps({
                'error': error,
            })
        values['project_id'] = project_id.id
        values['user_ids'] = [(6, 0, [project_id.user_id.id])]
        values['company_id'] = project_id.company_id.id
        values['name'] = post['client_name']
        task = request.env['project.task']
        task_id = task.sudo().create(values)
        regx = re.compile("^attachment_ids*")
        for attachments in post:
            if regx.match(attachments):
                name = post.get(attachments).filename
                file = post.get(attachments)
                request.env['ir.attachment'].sudo().create({
                    'name': name,
                    'type': 'binary',
                    'datas': base64.b64encode(file.read()),
                    'res_model': task._name,
                    'res_id': task_id.id
                })
        return json.dumps({'id': task_id.id})
