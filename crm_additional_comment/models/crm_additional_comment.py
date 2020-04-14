# -*- coding: utf-8 -*-

import logging
import itertools
from werkzeug import url_encode
import pytz

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource
from odoo.addons.resource.models.resource_mixin import timezone_datetime

_logger = logging.getLogger(__name__)

comment_temps = {
    "1":"had long conversation, but lead not interested in our service\n",
    "2":"after some talks lead is interested to order next items:\n",
    "3":"Lead unexpectedly hangup, didn't answered on my callback\n",
    "4":"Lead interested in our service, but for no he/she have not enough funds on account\n",
    
}

class crmLeadComments(models.Model):
    _name = "crm.lead.comments"
    _description = "CRM Lead additional comments"
    
    comment = fields.Text(string = "Comment")
    m2o_crm_lead = fields.Many2one("crm.lead")
    



#class for popup records when we need nnot to save any data, just using them as temporary info holders
class crmLeadCommentPopUps(models.TransientModel):
    _name = 'crm.lead.comment.popup'
    _descrtiption = 'Comment popups'
    
    record_id = fields.Char(string="Id", help="field where we store id from the record it was initated")
    text = fields.Text(string="Comment")
    add_to_notes = fields.Boolean(string="Add to notes", help="if this field is checked, input text will be added to notes to the end, notes wont be lost")
    override_notes = fields.Boolean(string="Override notes", help="if this field is checked, notes will be overwited by the input text")
    comment_templates = fields.Selection([
        ('1','Not interested'),
        ('2', 'interested'),
        ('3', 'hangup'),
        ('4', 'not enough funds')], string="Comment Template")
    
    @api.onchange('comment_templates')
    def _onchange_template(self):
        if self.comment_templates:
            if self.text:
                self.text = self.text + ' ' + comment_temps[self.comment_templates]
            else:
                self.text = comment_temps[self.comment_templates]

    
    
    def comment(self):
        lead_record = self.env['crm.lead'].search([('id','=',int(self.record_id))])
        # create comment
        self.env['crm.lead.comments'].sudo().create({"comment":self.text, "m2o_crm_lead":lead_record.id})
        if self.add_to_notes:
            try: text = lead_record.description + '\n' + self.text
            except: text = self.text
            lead_record.write({"description":text})
        if self.override_notes:
            text = self.text
            lead_record.write({"description":text})
        
        

    
class Lead(models.Model):
    _inherit = "crm.lead"
    
    o2m_lead_comments = fields.One2many("crm.lead.comments","m2o_crm_lead",string="Comments")
    
    def add_comment(self):
        action_id = self.env.ref('crm_additional_comment.view_additional_comment_popup')
        needed_context = {'default_record_id':self.id, 'default_add_to_notes':True}
        return {
            'name': action_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead.comment.popup',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': needed_context,
        }
      
    