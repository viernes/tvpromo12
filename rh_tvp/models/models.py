# -*- coding: utf-8 -*-

from odoo import api, _, tools, fields, models, exceptions,  SUPERUSER_ID
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta


class RHFields(models.Model):

	_inherit = 'hr.employee'

	antiquity = fields.Char(string='Antigüedad', compute='_antiquity_calculation')
	antiquity_years = fields.Integer(string='Antigüedad Años',compute ='_compute_years')

	date_in = fields.Date(string='Fecha de Ingreso')
	date_out = fields.Date(string='Fecha de Baja')
	reason = fields.Selection([('1','Renuncia'),('2','Recorte de Personal'),('3','Fin de Contrato'),('4','Otro')],string='Motivo de Baja')
	commnets = fields.Text(string='Comentarios')


	@api.one
	@api.depends('date_in','date_out','antiquity','active')
	def _antiquity_calculation(self):
			if 	self.active == True:
				if self.date_in:
					diff = relativedelta(datetime.today(), datetime.strptime(str(self.date_in), '%Y-%m-%d'))
					years = diff.years
					months = diff.months
					days = diff.days					
					self.antiquity = '{} Años {} Meses {} Dias'.format(years, months, days)
				else:
					if self.date_out and self.date_in: 
						diff = relativedelta(datetime.datetime(self.date_in), datetime.strptime(str(self.date_out), '%Y-%m-%d'))
						years = diff.years
						months = diff.months
						days = diff.days					
						self.antiquity = '{} Años {} Meses {} Dias'.format(years, months, days)

#Revisar la funcion if de por que no funciona o manda la fecha cuando esta active false

	@api.multi
	@api.depends('date_in','antiquity_years')
	def _compute_years(self):
	    for record in self:
	        if record.date_in and record.date_in <= fields.Date.today():
	            record.antiquity_years = relativedelta(
	                fields.Date.from_string(fields.Date.today()),
	                fields.Date.from_string(record.date_in)).years 
	        else: 
	            record.antiquity_years = 0	


class leavefields(models.Model):
	_inherit = 'hr.leave.type'

	validity = fields.Integer(string='Vigencia en meses', default=18)
	days = fields.Integer(string='Dias')
	antiquity_years = fields.Integer(string='Antigüedad')


class leaveasignations(models.Model):
	_inherit = 'hr.leave.allocation'		

	antiquity = fields.Integer(string='Antigüedad Años')
	validity = fields.Integer(string='Vigencia en meses', default=18)
	date_in = fields.Date(string='Fecha de Ingreso')
	antiquity_years_allocation = fields.Integer(related='holiday_status_id.antiquity_years',string='')
	comple_laboral = fields.Date(string='Cumpleaños Laboral',compute='_cumple_laboral_calcution')
	vencimiento = fields.Date(string='Vencimiento',compute='_cumple_laboral_calcution')

	@api.onchange('employee_id')
	def _onchange_antiquity(self):
		if self.employee_id:
			self.antiquity = self.employee_id.antiquity_years
			self.date_in = self.employee_id.date_in

	@api.onchange('holiday_status_id')
	def _onchange_days(self):
		if self.holiday_status_id:
			self.number_of_days_display = self.holiday_status_id.days

	@api.one
	@api.depends('date_in','comple_laboral','antiquity','validity')
	def _cumple_laboral_calcution(self):
			if self.date_in:
				self.comple_laboral = fields.Date.from_string(self.date_in) + relativedelta(years=self.antiquity)
				self.vencimiento = fields.Date.from_string(self.comple_laboral) + relativedelta(months=self.validity)



    # @api.onchange('number_of_days')
    # def number_of_days_change(self):
    #     if self.number_of_days:
    #         if self.start_date:
    #             end_date_dt = fields.Date.from_string(self.start_date) + relativedelta(days=self.number_of_days - 1)
    #             end_date = fields.Date.to_string(end_date_dt)
    #             if self.end_date != end_date:
    #                 self.end_date = end_date
    #         elif self.end_date:
    #             self.start_date = fields.Date.from_string(self.end_date) -\
    #                 relativedelta(days=self.number_of_days - 1)



	# @api.onchange('antiquity')
	# def _onchange_days(self):
	# 	if self.antiquity:
	# 		self.holiday_status_id = self.search([('holiday_status_id.antiquity_years', '=', self.antiquity)], limit=1)

	# @api.onchange('antiquity','antiquity_years_allocation')
	# def _onchange_days(self):
	# 	if self.antiquity:
	# 		self.holiday_status_id = self.env['hr.leave.allocation'].search([('antiquity_years_allocation', '=', self.antiquity)], limit=1)


    # def calculate_age(birth_date):
    #     today = date.today()
    #     age = today.year - birth_date.year
    #     full_year_passed = (today.month, today.day) < (birth_date.month, birth_date.day)
    #     if not full_year_passed:
    #         age -= 1
    #     return age>>> from datetime import date


# >>> current_date=date.today()
# >>> carry, new_month=divmod(current_date.month-1+1, 12)
# >>> new_month+=1
# >>> current_date=current_date.replace(year=current_date.year+carry, month=new_month)
# >>> print date.today()
# 2011-05-21
# >>> print current_date
# 2011-06-21
# >>>

