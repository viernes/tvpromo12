# -*- coding: utf-8 -*-

from odoo import api, _, tools, fields, models, exceptions,  SUPERUSER_ID
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta


class helpdesk(models.Model):

	_inherit = 'helpdesk.sla'

	time_minutes = fields.Integer(help='En este campo podras ingresar los minutos asignados al ticket')
	
class clasificacionTeam(models.Model):
	"""docstring for clasificacionTeam"""
	_inherit = 'helpdesk.team'
	
	class_id = fields.Selection([('1','Mantenimiento'),('2','Mensajeria'),('3','Sistemas / Soporte')], string='Especificacion de Equipo', requiered=True)

class Clasificacion(models.Model):
	_inherit = 'helpdesk.ticket'

	clasi_mantenimiento = fields.Selection([('1','Electricidad'),('2','Carpintería'),('3','Cerrajería'),('4','Plomería'),
											('5','Albañilería'),('6','Pintura'),('7','Pisos'),('8','Otros')], string='Clasificacion')
	clasi_sistemas = fields.Selection([('1','Hardware'),('2','Software'),('3','Capacitación'),('4','Usuario'),('5','Electricidad'),('6','Internet'),('7','Telefonía'),('8','Antivirus')],string='Clasificacion')
	alias_check = fields.Integer(string='Alias',compute='_alias')
	others = fields.Text(string='Otros')	

	@api.depends('team_id')
	def _alias(self):
		if	self.team_id:
			self.alias_check = self.team_id.class_id	

class expensesfields(models.Model):

	_inherit = 'hr.expense.sheet'

	delivery_amount = fields.Monetary(string='Cantidad de Entrega')
	prove_amount = fields.Monetary(related='total_amount', string='Cantidad Comprobada')
	returned = fields.Monetary(string='Devuelto')
	diferencia = fields.Monetary(string='Diferencia', compute="_total_mejoras")
	approved = fields.Boolean(string='Aprovado')
	tipo_gasto = fields.Selection([('1','BTL'),('2','Produccion'),('3','Diseño'),('4','Gestoria'),('5','Contact Center'),('6','Marketing Digital'),('7','Medios'),('8','logistica'),('9','Estrategia')], string='Area')

	@api.depends('prove_amount','returned','diferencia','delivery_amount')
	def _total_mejoras(self):
	    self.diferencia = (float(self.delivery_amount)) - (float(self.prove_amount)) - (float(self.returned))

class Reembolso(models.Model):
	"""docstring for Reembolso"""
	_inherit = 'hr.expense'

	tipo_gasto = fields.Selection([('1','BTL'),('2','Produccion'),('3','Diseño'),('4','Gestoria'),('5','Contact Center'),('6','Marketing Digital'),('7','Medios'),('8','logistica'),('9','Estrategia')], string='Tipo de Gasto')

		
	
class inventory(models.Model):

	_inherit = 'stock.picking'

	return_reason = fields.Char(string='Motivo de la Devolucion')
	receive = fields.Char(string='Quien recibe')
	folio_ganador = fields.Char(string='Folio consecutivo de ganador')
	ejecutivo = fields.Many2one('hr.employee', string='Ejecutivo Asignado')
	promosion = fields.Char(string='Promocion')



class Flotilla(models.Model):

	_inherit = 'fleet.vehicle'

	date_emision_tc = fields.Date(string='Fecha de Emision TC')
	date_vencimiento_tc = fields.Date(string='Fecha de Vencimiento TC')
	date_verificacion = fields.Date(string='Fecha de Verificacion')
	reason = fields.Selection([('1','Venta'),('2','Siniestro')], string='Razon')
	comments = fields.Text(string='Comentarios')
	compania_seguro = fields.Char(string='Compañia de seguro')
	start_date = fields.Date(string='Fecha de inicio de seguro')
	end_date = fields.Date(string='Fecha de termino de seguro')
	next_km = fields.Integer(string='Siguiente Kilometraje')
	next_service = fields.Date(string='Siguiente Servicio')
	no_poliza = fields.Integer(string='No. Poliza', size=100)


