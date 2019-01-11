# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError

class HrLeave(models.Model):
	_inherit = "hr.leave"

	def _check_approval_update(self, state):
		""" Check if target state is achievable. """
		current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
		# is_officer = self.env.user.has_group('hr_holidays.group_hr_holidays_user')
		is_manager = self.env.user.has_group('hr_holidays.group_hr_holidays_manager')
		for holiday in self:
			val_type = holiday.holiday_status_id.validation_type
			if state == 'confirm':
				continue

			if state == 'draft':
				if holiday.employee_id != current_employee and not is_manager:
					raise UserError(_('Only a Leave Manager can reset other people leaves.'))
				continue

			# if not is_officer:
			# 	raise UserError(_('Only a Leave Officer or Manager can approve or refuse leave requests.'))

			# if is_officer:
			# 	# use ir.rule based first access check: department, members, ... (see security.xml)
			holiday.check_access_rule('write')

			if holiday.employee_id == current_employee and not is_manager:
				raise UserError(_('Only a Leave Manager can approve its own requests.'))

			if (state == 'validate1' and val_type == 'both') or (state == 'validate' and val_type == 'manager'):
				manager = holiday.employee_id.parent_id or holiday.employee_id.department_id.manager_id
				if (manager and manager != current_employee) and not self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
					raise UserError(_('You must be either %s\'s manager or Leave manager to approve this leave') % (holiday.employee_id.name))

			if state == 'validate' and val_type == 'both':
				if not self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
					raise UserError(_('Only an Leave Manager can apply the second approval on leave requests.'))



# class rem_officer_leave(models.Model):
#	 _name = 'rem_officer_leave.rem_officer_leave'

#	 name = fields.Char()
#	 value = fields.Integer()
#	 value2 = fields.Float(compute="_value_pc", store=True)
#	 description = fields.Text()
#
#	 @api.depends('value')
#	 def _value_pc(self):
#		 self.value2 = float(self.value) / 100