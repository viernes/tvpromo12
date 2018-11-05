from odoo import api, _, tools, fields, models, exceptions
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime, date, time


class crmlead(models.Model):
	"""docstring for crmlead"""
	_inherit = 'crm.lead'

	odt_count = fields.Integer()
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
	cm_2 = fields.Char(string='¿Que linea de comunicación esta implementando la marca actualmente?')
	cm_3 = fields.Char(string='¿Descripcion de la marca (Joven, solida, dinamica, innovadora, flexible, segura, institucional, preocupada por el consumidor)?')
	cm_4 = fields.Char(string='¿Que tono se debe adoptar?')
	qcs_1 = fields.Char(string='¿Quiénes son los competidores?')
	qcs_2 = fields.Char(string='¿En qué se diferencia la marca ante la competencia (beneficios al consumidor)?')
	qcs_3 = fields.Char(string='¿Qué piensan y sienten los consumidores acerca de la competencia?')
	vh_1 = fields.Char(string='¿NSE, TARGET?')
	vh_2 = fields.Char(string='¿Cuál es el comportamiengo habitual?')
	vh_3 = fields.Char(string='¿Qué piensan y sienten acerca de la marca?')
	dc_1 = fields.Char(string='7. ¿QUÉ DEBEMOS COMUNICAR?')
	dc_2 = fields.Char(string='¿Qué queremos que piensen y sientan de la marca?')
	dc_3 = fields.Char(string='¿Qué queremos que se sepa y sienta la gente sobre esta comunicación?')
	qc_1 = fields.Char(string='8. ¿QUÉ NO QUEREMOS COMUNICAR?')
	qc_2 = fields.Char(string='9. ¿CÓMO SE COMPORTA EL CONSUMIDOR RESPECTO AL PRODUCTO O SERVICIO ACTUALMENTE (CONDUCTAS Y CARENCIAS)?')
	ccp_1 = fields.Char(string='10. ¿QUÉ OTRAS PROMOCIONES HA TENIDO LA MARCA?')
	ccp_2 = fields.Char(string='¿Qué resultados obtuvieron?')
	cdp_1 = fields.Char(string='¿Qué medios se utilizarán para la implementación?')
	cdp_2 = fields.Char(string='¿Qué medios se utilizarán para la difusión?')
	cdp_3 = fields.Char(string='¿Qué medios se utilizarán para la participación?')
	qz_12 = fields.Char(string='¿CUÁL ES EL MARCO LEGAL?(RTC, SEGOB, PROFECO, MICROSITIOS Y PROMOWEB)')
	qz_13 = fields.Char(string='¿HAY REQUERIMIENTO ADICIONALES? /n Medios de datos y consideraciones creativas, mandatorios con respecto al uso de la marca, aspectos legales, manejo de los modulos,etc')
	qz_14 = fields.Char(string='¿HAY UN ESTIMADO DE PRESUPUESTO?')
	qz_15 = fields.Char(string='¿CUÁLES SON LOS ENTREGABLES?')
	qz_16 = fields.Char(string='¿SE TRABAJARA EN CONJUNCO CON ALGUNA AGENCIA DE LA MARCA?')


class marca_crm(models.Model):
	"""docstring for marca_crm"""
	_name = 'crm_marca'
	_description = 'Informacion acerca de las marcas o empresas'

	name = fields.Char(string='Nombre')

class policysli(models.Model):

	_inherit = 'helpdesk.sla'

	time_minutes = fields.Integer(help='En este campo podras ingresar los minutos asignados al ticket')

class expensesfields(models.Model):

	_inherit = 'hr.expense.sheet'

	delivery_amount = fields.Monetary(string='Cantidad de Entrega')
	prove_amount = fields.Monetary(string='Cantidad Comprobada')
	returned = fields.Monetary(string='Devuelto')
	diferencia = fields.Monetary(string='Diferencia')
	approved = fields.Boolean(string='Aprovado')



	
class inventory(models.Model):

	_inherit = 'stock.picking'

	return_reason = fields.Char(string='Motivo de la Devolucion')
	receive = fields.Char(string='Quien recibe')
