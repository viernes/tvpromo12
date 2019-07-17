# copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api

class OdtDiseno(models.Model):

	_inherit = "odt.diseno"

	@api.onchange('d_presentacion')
	def _onchange_d_presentacion(self):
		if self.d_presentacion == True:
			self.cont_presentacion = 1
		else:
			self.cont_presentacion = 0

	@api.onchange('d_template')
	def _onchange_d_template(self):
		if self.d_template == True:
			self.cont_template = 1
		else:
			self.cont_template = 0

	@api.onchange('d_master_graph')
	def _onchange_d_master_graph(self):
		if self.d_master_graph == True:
			self.cont_graph = 1
		else:
			self.cont_graph = 0

	@api.onchange('d_adaptacion_pop')
	def _onchange_d_adaptacion_pop(self):
		if self.d_adaptacion_pop == True:
			self.cont_pop = 1
		else:
			self.cont_pop = 0

	@api.onchange('d_ohoo')
	def _onchange_d_ohoo(self):
		if self.d_ohoo == True:
			self.cont_ohoo = 1
		else:
			self.cont_ohoo = 0

	@api.onchange('d_logotipo')
	def _onchange_d_logotipo(self):
		if self.d_logotipo == True:
			self.cont_logotipo = 1
		else:
			self.cont_logotipo = 0

	@api.onchange('d_visualizacion')
	def _onchange_d_visualizacion(self):
		if self.d_visualizacion == True:
			self.cont_visualizacion = 1
		else:
			self.cont_visualizacion = 0

	@api.onchange('d_adaptacion_digital')
	def _onchange_d_adaptacion_digital(self):
		if self.d_adaptacion_digital == True:
			self.cont_digital = 1
		else:
			self.cont_digital = 0

	@api.onchange('d_otro')
	def _onchange_d_otro(self):
		if self.d_otro == True:
			self.cont_otro = 1
		else:
			self.cont_otro = 0

	# Para controlar Servicios solicitados
	cont_presentacion = fields.Float(string="Contador Presentacion")
	cont_template = fields.Float(string="Contador Template")
	cont_graph = fields.Float(string="Contador Graphic")
	cont_pop = fields.Float(string="Contador POP")
	cont_ohoo = fields.Float(string="Contador Ohoo")
	cont_logotipo = fields.Float(string="Contador Logotipo")
	cont_visualizacion = fields.Float(string="Contador Visualizacion")
	cont_digital = fields.Float(string="Contador Digital")
	cont_otro = fields.Float(string="Contador Otro")