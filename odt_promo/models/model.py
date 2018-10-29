from odoo import api, _, tools, fields, models, exceptions
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime, date, time


class crmlead(models.Model):
	"""docstring for crmlead"""
	_inherit = 'crm.lead'

	marca = fields.Many2one('crm_marca', string='Marca')
	target = fields.Char(string='Target')
	product = fields.Char(string='Producto')
	project = fields.Many2one('project.project',string='Proyecto')
	term_promo_date = fields.Date(string='Vigencia de la promocion')
	temporalidad = fields.Char(string='Temporalidad')
	slogan_marca = fields.Char(string='Eslogan')
	logo_marca = fields.Binary(string='Logo')

	""" Quiz Fields """

	rp_1 = fields.Char(string='¿Para que estamos haciendo este proyecto y cual es el reto?')
	rp_2 = fields.Char(string='¿Que queremos que se sepa y sienta la gente sobre el proeycto?')
	rp_3 = fields.Char(string='¿Que buscamos lograr?')
	rp_4 = fields.Char(string='¿Cual es el problema a resolver?')
	on_1 = fields.Char(string='¿Crecimiento?')
	on_2 = fields.Char(string='¿Mayor margen de utilidad?')
	on_3 = fields.Char(string='¿Posicionamiento de un nuevo producto o servicio?')
	on_4 = fields.Char(string='¿Hacer frente a la competencia?')
	ob_1 = fields.Char(string='¿Conocimiento?')
	ob_2 = fields.Char(string='¿Posicionamiento?')
	ob_3 = fields.Char(string='¿Diferenciacion?')
	cm_1 = fields.Char(string='¿Como se define y posiciona la marca en cuanto a si misma?')
	cm_2 = fields.Char(string='¿Que linea de comunicacion esta implementando la marca actualmente?')
	cm_3 = fields.Char(string='¿Descripcion de la marca (Joven, solida, dinamica, innovadora, flexible, segura, institucional, preocupada por el consumidor)?')
	cm_4 = fields.Char(string='¿Que tono se debe adoptar?')

class marca_crm(models.Model):
	"""docstring for marca_crm"""
	_name = 'crm_marca'
	_description = 'Informacion acerca de las marcas o empresas'

	name = fields.Char(string='Nombre')