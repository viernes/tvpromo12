# -*- coding: utf-8 -*-

from odoo import api, _, tools, fields, models, exceptions,  SUPERUSER_ID
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
	odt_count = fields.Integer(string='lead', compute='_compute_odt_count')

	btl = fields.Float(string='BTL/PDV')
	produccion = fields.Float(string='Produccion')
	diseño_creatividad = fields.Float(string='Diseño')
	gestoria_logistica = fields.Float(string='Gestoria y Logistica')
	call_center = fields.Float(string='Contact Center')
	digital = fields.Float(string='Marketing Digital')
	medios = fields.Float(string='Medios')
	logistica = fields.Float(string='Logistica')
	estrategia = fields.Float(string='Estrategia')



	@api.multi
	def _compute_odt_count(self):
		count = self.env['odt.crm']
		self.odt_count = count.search_count([('crm_odt_id', 'in', [a.id for a in self])])

	""" Quiz Fields """

	rp_1 = fields.Char(string='¿Para que estamos haciendo este proyecto y cual es el reto?', track_visibility=True)
	rp_2 = fields.Char(string='¿Que queremos que se sepa y sienta la gente sobre el proeycto?', track_visibility=True)
	rp_3 = fields.Char(string='¿Que buscamos lograr?', track_visibility=True)
	rp_4 = fields.Char(string='¿Cual es el problema a resolver?', track_visibility=True)
	on_1 = fields.Char(string='¿Crecimiento?', track_visibility=True)
	on_2 = fields.Char(string='¿Mayor margen de utilidad?', track_visibility=True)
	on_3 = fields.Char(string='¿Posicionamiento de un nuevo producto o servicio?', track_visibility=True)
	on_4 = fields.Char(string='¿Hacer frente a la competencia?', track_visibility=True)
	ob_1 = fields.Char(string='¿Conocimiento?', track_visibility=True)
	ob_2 = fields.Char(string='¿Posicionamiento?', track_visibility=True)
	ob_3 = fields.Char(string='¿Diferenciacion?', track_visibility=True)
	cm_1 = fields.Char(string='¿Como se define y posiciona la marca en cuanto a si misma?', track_visibility=True)
	cm_2 = fields.Char(string='¿Que linea de comunicación esta implementando la marca actualmente?', track_visibility=True)
	cm_3 = fields.Char(string='¿Descripcion de la marca (Joven, solida, dinamica, innovadora, flexible, segura, institucional, preocupada por el consumidor)?', track_visibility=True)
	cm_4 = fields.Char(string='¿Que tono se debe adoptar?', track_visibility=True)
	qcs_1 = fields.Char(string='¿Quiénes son los competidores?', track_visibility=True)
	qcs_2 = fields.Char(string='¿En qué se diferencia la marca ante la competencia (beneficios al consumidor)?', track_visibility=True)
	qcs_3 = fields.Char(string='¿Qué piensan y sienten los consumidores acerca de la competencia?', track_visibility=True)
	vh_1 = fields.Char(string='¿NSE, TARGET?', track_visibility=True)
	vh_2 = fields.Char(string='¿Cuál es el comportamiengo habitual?', track_visibility=True)
	vh_3 = fields.Char(string='¿Qué piensan y sienten acerca de la marca?', track_visibility=True)
	dc_1 = fields.Char(string='7. ¿QUÉ DEBEMOS COMUNICAR?', track_visibility=True)
	dc_2 = fields.Char(string='¿Qué queremos que piensen y sientan de la marca?', track_visibility=True)
	dc_3 = fields.Char(string='¿Qué queremos que se sepa y sienta la gente sobre esta comunicación?', track_visibility=True)
	qc_1 = fields.Char(string='8. ¿QUÉ NO QUEREMOS COMUNICAR?', track_visibility=True)
	qc_2 = fields.Char(string='9. ¿CÓMO SE COMPORTA EL CONSUMIDOR RESPECTO AL PRODUCTO O SERVICIO ACTUALMENTE (CONDUCTAS Y CARENCIAS)?', track_visibility=True)
	ccp_1 = fields.Char(string='10. ¿QUÉ OTRAS PROMOCIONES HA TENIDO LA MARCA?', track_visibility=True)
	ccp_2 = fields.Char(string='¿Qué resultados obtuvieron?', track_visibility=True)
	cdp_1 = fields.Char(string='¿Qué medios se utilizarán para la implementación?', track_visibility=True)
	cdp_2 = fields.Char(string='¿Qué medios se utilizarán para la difusión?', track_visibility=True)
	cdp_3 = fields.Char(string='¿Qué medios se utilizarán para la participación?', track_visibility=True)
	qz_12 = fields.Char(string='¿CUÁL ES EL MARCO LEGAL?(RTC, SEGOB, PROFECO, MICROSITIOS Y PROMOWEB)', track_visibility=True)
	qz_13 = fields.Char(string='¿HAY REQUERIMIENTO ADICIONALES? /n Medios de datos y consideraciones creativas, mandatorios con respecto al uso de la marca, aspectos legales, manejo de los modulos,etc', track_visibility=True)
	qz_14 = fields.Char(string='¿HAY UN ESTIMADO DE PRESUPUESTO?', track_visibility=True)
	qz_15 = fields.Char(string='¿CUÁLES SON LOS ENTREGABLES?', track_visibility=True)
	qz_16 = fields.Char(string='¿SE TRABAJARA EN CONJUNCO CON ALGUNA AGENCIA DE LA MARCA?', track_visibility=True)


class odt(models.Model):

	_name = 'odt.crm'
	_description = 'Vista Kanban para visualizar informacion de crm en solo lectura'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	def _default_probability(self):
		stage_id = self._default_stage_id()
		if stage_id:
			return self.env['crm.stage'].browse(stage_id).probability
		return 10

	def _default_stage_id(self):
		team = self.env['crm.team'].sudo()._get_default_team_id(user_id=self.env.uid)
		return self._stage_find(team_id=team.id, domain=[('fold', '=', False)]).id

	# Funcion para la sumatoria de lineas dentro de la tabla cotizacion

	@api.depends('tabla_cotizacion_btl')
	def _btl_totales(self):
		self.total_precio_unitario_btl = sum(line.precio_unitario_btl for line in self.tabla_cotizacion_btl)
		self.total_costo_proveedor_btl = sum(line.costo_proveedor_btl for line in self.tabla_cotizacion_btl)


	@api.depends('tabla_cotizacion_produccion')
	def _produccion_totales(self):
		self.total_cliente_produ = sum(line.costo_cliente for line in self.tabla_cotizacion_produccion)
		self.total_gtvo_produ = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_produccion)
		self.total_terceros_produ = sum(line.pago_terceros for line in self.tabla_cotizacion_produccion)
		self.total_interno_produ = sum(line.costo_interno for line in self.tabla_cotizacion_produccion)
		self.total_recuperacion_produ = sum(line.recuperacion for line in self.tabla_cotizacion_produccion)

	@api.depends('tabla_cotizacion_diseno')
	def _diseno_totales(self):
		self.total_cliente_diseno = sum(line.costo_cliente for line in self.tabla_cotizacion_diseno)
		self.total_gtvo_diseno = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_diseno)
		self.total_terceros_diseno = sum(line.pago_terceros for line in self.tabla_cotizacion_diseno)
		self.total_interno_diseno = sum(line.costo_interno for line in self.tabla_cotizacion_diseno)
		self.total_recuperacion_diseno = sum(line.recuperacion for line in self.tabla_cotizacion_diseno)

	@api.depends('tabla_cotizacion_estrategia')
	def _estrategia_totales(self):
		self.total_cliente_estrategia = sum(line.costo_cliente for line in self.tabla_cotizacion_estrategia)
		self.total_gtvo_estrategia = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_estrategia)
		self.total_terceros_estrategia = sum(line.pago_terceros for line in self.tabla_cotizacion_estrategia)
		self.total_interno_estrategia = sum(line.costo_interno for line in self.tabla_cotizacion_estrategia)
		self.total_recuperacion_estrategia = sum(line.recuperacion for line in self.tabla_cotizacion_estrategia)

	@api.depends('tabla_cotizacion_gestoria')
	def _gestoria_totales(self):
		self.total_cliente_gestoria = sum(line.costo_cliente for line in self.tabla_cotizacion_gestoria)
		self.total_gtvo_gestoria = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_gestoria)
		self.total_terceros_gestoria = sum(line.pago_terceros for line in self.tabla_cotizacion_gestoria)
		self.total_interno_gestoria = sum(line.costo_interno for line in self.tabla_cotizacion_gestoria)
		self.total_recuperacion_gestoria = sum(line.recuperacion for line in self.tabla_cotizacion_gestoria)

	# @api.depends('tabla_cotizacion_callcenter')
	# def _callcenter_totales(self):
	# 	self.total_cliente_callcenter = sum(line.costo_cliente for line in self.tabla_cotizacion_callcenter)
	# 	self.total_gtvo_callcenter = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_callcenter)
	# 	self.total_terceros_callcenter = sum(line.pago_terceros for line in self.tabla_cotizacion_callcenter)
	# 	self.total_interno_callcenter = sum(line.costo_interno for line in self.tabla_cotizacion_callcenter)
	# 	self.total_recuperacion_callcenter = sum(line.recuperacion for line in self.tabla_cotizacion_callcenter)


	@api.depends('tabla_cotizacion_digital')
	def _digital_totales(self):
		self.total_costo_interno_digital = sum(line.costo_interno for line in self.tabla_cotizacion_digital)
		self.total_pago_terceros_digital = sum(line.pago_terceros for line in self.tabla_cotizacion_digital)
		self.total_recuperacion_digital= sum(line.recuperacion for line in self.tabla_cotizacion_digital)
		self.total_costo_cliente_digital = sum(line.costo_cliente for line in self.tabla_cotizacion_digital)
		self.total_monto_venta_digital = sum(line.monto_venta for line in self.tabla_cotizacion_digital)


	project_name = fields.Char(string='Nombre del proyecto')
	crm_odt_id = fields.Many2one('crm.lead', 'Opportunity')
	name = fields.Char(string='Nombre')
	tag_ids = fields.Many2many('crm.lead.tag', 'crm_lead_tag_rel', 'lead_id', 'tag_id',related='crm_odt_id.tag_ids', string='Tags', help="Classify and analyze your lead/opportunity categories like: Training, Service")
	stage_id = fields.Many2one('crm.stage', string='Stage', ondelete='restrict', track_visibility='onchange', index=True,
		domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
		group_expand='_read_group_stage_ids', default=lambda self: self._default_stage_id())
	team_id = fields.Many2one('crm.team',related='crm_odt_id.team_id', string='Sales Team', oldname='section_id', default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(user_id=self.env.uid),
		index=True, track_visibility='onchange', help='When sending mails, the default email address is taken from the Sales Team.')
	kanban_state = fields.Selection([('normal','In Progress'),('blocked','Blocked'),('done','Ready for next Stage')], 'Kanban State', default='normal')
	user_id = fields.Many2one('res.users', related='crm_odt_id.user_id',string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
	partner_id = fields.Many2one('res.partner',related='crm_odt_id.partner_id', string='Customer', track_visibility='onchange', track_sequence=1, index=True,
				help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
	priority = fields.Selection([('0','Low'),('1','Normal'),('2','High'),('3','Very High')],related='crm_odt_id.priority',string='Priority', default='1')
	color = fields.Integer(related='crm_odt_id.color',string='Color Index')
	active = fields.Boolean(related='crm_odt_id.active',string='Active', default=True, track_visibility=True)
	email_from = fields.Char('Email', help="Email address of the contact", track_visibility='onchange', track_sequence=4, index=True)
	partner_address_email = fields.Char(related='crm_odt_id.partner_address_email',string='Partner Contact Email', readonly=True)
	partner_address_phone = fields.Char(related='crm_odt_id.partner_address_phone',string='Partner Contact Phone', readonly=True)
	date_deadline = fields.Date(related='crm_odt_id.date_deadline',string='Expected Closing', help="Estimate of the date on which the opportunity will be won.")
	partner_name = fields.Char(related='crm_odt_id.partner_name',string='Customer Name')
	date_conversion = fields.Datetime(related='crm_odt_id.date_conversion',string='Conversion Date', readonly=True)
	description = fields.Text(related='crm_odt_id.description',string='Notes', track_visibility='onchange', track_sequence=6)
	contact_name = fields.Char(related='crm_odt_id.contact_name',string='Contact Name', track_visibility='onchange', track_sequence=3)
	day_close = fields.Float(related='crm_odt_id.day_close',string='Days to Close', store=True)
	day_open = fields.Float(related='crm_odt_id.day_open',string='Days to Assign', store=True)
	referred = fields.Char(related='crm_odt_id.referred',string='Referred By')
	type = fields.Selection([('lead', 'Lead'), ('opportunity', 'Opportunity')],related='crm_odt_id.type',string='type', index=True, help="Type is used to separate Leads and Opportunities")
	campaign_id = fields.Many2one(related='crm_odt_id.campaign_id',string='Campaing')
	medium_id = fields.Many2one(related='crm_odt_id.medium_id',string='Medium')
	source_id = fields.Many2one(related='crm_odt_id.source_id',string='Source')
	street = fields.Char(related='crm_odt_id.street',string='Street')
	street2 = fields.Char(related='crm_odt_id.street2',string='Street2')
	zip = fields.Char(related='crm_odt_id.zip',string='Zip', change_default=True)
	city = fields.Char(related='crm_odt_id.city',string='City')
	state_id = fields.Many2one("res.country.state",related='crm_odt_id.state_id', string='State')
	country_id = fields.Many2one('res.country',related='crm_odt_id.country_id', string='Country')
	phone = fields.Char(related='crm_odt_id.phone',string='Phone', track_visibility='onchange', track_sequence=5)
	mobile = fields.Char(related='crm_odt_id.mobile',string='Mobile')
	function = fields.Char(related='crm_odt_id.function',string='Job Position')
	title = fields.Many2one('res.partner.title',related='crm_odt_id.title')
	company_id = fields.Many2one('res.company',related='crm_odt_id.company_id', string='Company', index=True, default=lambda self: self.env.user.company_id.id)
	lost_reason = fields.Many2one('crm.lost.reason',related='crm_odt_id.lost_reason', string='Lost Reason', index=True, track_visibility='onchange')
	partner_is_blacklisted = fields.Boolean(related='crm_odt_id.partner_is_blacklisted',string='Partner is blacklisted', readonly=True)
	is_blacklisted = fields.Boolean(related='crm_odt_id.is_blacklisted')
	marca = fields.Many2one('crm_marca', related='crm_odt_id.marca',string='Marca')
	target = fields.Char(string='Target')
	area = fields.Selection([('1','BTL/PDV'),('2','Produccion'),('3','Diseño'),('4','Gestoria'),('5','Contact Center'),('6','Marketing Digital'),('7','Medios'),('8','logistica'),('9','Estrategia')], string='Area', track_visibility=True)

	# seccion para odt medios
	med_spot_tv_abierta = fields.Boolean(string='Spot TV Abierta TVSA', track_visibility=True)
	med_aaee_tv = fields.Boolean(string='AAEE TV TVSA', track_visibility=True)
	med_brief_aaee = fields.Boolean(string='Brief AAEE', track_visibility=True)
	med_spoteo_carriers = fields.Boolean(string='Spoteo Carriers', track_visibility=True)
	med_net_televisa = fields.Boolean(string='Networks Televisa', track_visibility=True)
	med_otros_net = fields.Boolean(string='Otros Networks', track_visibility=True)
	med_radio = fields.Boolean(string='Radio', track_visibility=True)
	med_revista = fields.Boolean(string='Revista', track_visibility=True)
	med_prensa = fields.Boolean(string='Prensa', track_visibility=True)
	med_ooh = fields.Boolean(string='OOH', track_visibility=True)
	med_digital = fields.Boolean(string='Digital', track_visibility=True)
	med_analisis = fields.Boolean(string='Analisis', track_visibility=True)

	# BRIEF
	rp_1 = fields.Char(related='crm_odt_id.rp_1',string='¿Para que estamos haciendo este proyecto y cual es el reto?')
	rp_2 = fields.Char(related='crm_odt_id.rp_2',string='¿Que queremos que se sepa y sienta la gente sobre el proeycto?')
	rp_3 = fields.Char(related='crm_odt_id.rp_3',string='¿Que buscamos lograr?')
	rp_4 = fields.Char(related='crm_odt_id.rp_4',string='¿Cual es el problema a resolver?')
	on_1 = fields.Char(related='crm_odt_id.on_1',string='¿Crecimiento?')
	on_2 = fields.Char(related='crm_odt_id.on_2',string='¿Mayor margen de utilidad?')
	on_3 = fields.Char(related='crm_odt_id.on_3',string='¿Posicionamiento de un nuevo producto o servicio?')
	on_4 = fields.Char(related='crm_odt_id.on_4',string='¿Hacer frente a la competencia?')
	ob_1 = fields.Char(related='crm_odt_id.ob_1',string='¿Conocimiento?')
	ob_2 = fields.Char(related='crm_odt_id.ob_2',string='¿Posicionamiento?')
	ob_3 = fields.Char(related='crm_odt_id.ob_3',string='¿Diferenciacion?')
	cm_1 = fields.Char(related='crm_odt_id.cm_1',string='¿Como se define y posiciona la marca en cuanto a si misma?')
	cm_2 = fields.Char(related='crm_odt_id.cm_2',string='¿Que linea de comunicación esta implementando la marca actualmente?')
	cm_3 = fields.Char(related='crm_odt_id.cm_3',string='¿Descripcion de la marca (Joven, solida, dinamica, innovadora, flexible, segura, institucional, preocupada por el consumidor)?')
	cm_4 = fields.Char(related='crm_odt_id.cm_4',string='¿Que tono se debe adoptar?')
	qcs_1 = fields.Char(related='crm_odt_id.qcs_1',string='¿Quiénes son los competidores?')
	qcs_2 = fields.Char(related='crm_odt_id.qcs_2',string='¿En qué se diferencia la marca ante la competencia (beneficios al consumidor)?')
	qcs_3 = fields.Char(related='crm_odt_id.qcs_3',string='¿Qué piensan y sienten los consumidores acerca de la competencia?')
	vh_1 = fields.Char(related='crm_odt_id.vh_1',string='¿NSE, TARGET?')
	vh_2 = fields.Char(related='crm_odt_id.vh_2',string='¿Cuál es el comportamiengo habitual?')
	vh_3 = fields.Char(related='crm_odt_id.vh_3',string='¿Qué piensan y sienten acerca de la marca?')
	dc_1 = fields.Char(related='crm_odt_id.dc_1',string='7. ¿QUÉ DEBEMOS COMUNICAR?')
	dc_2 = fields.Char(related='crm_odt_id.dc_2',string='¿Qué queremos que piensen y sientan de la marca?')
	dc_3 = fields.Char(related='crm_odt_id.dc_3',string='¿Qué queremos que se sepa y sienta la gente sobre esta comunicación?')
	qc_1 = fields.Char(related='crm_odt_id.qc_1',string='8. ¿QUÉ NO QUEREMOS COMUNICAR?')
	qc_2 = fields.Char(related='crm_odt_id.qc_2',string='9. ¿CÓMO SE COMPORTA EL CONSUMIDOR RESPECTO AL PRODUCTO O SERVICIO ACTUALMENTE (CONDUCTAS Y CARENCIAS)?')
	ccp_1 = fields.Char(related='crm_odt_id.ccp_1',string='10. ¿QUÉ OTRAS PROMOCIONES HA TENIDO LA MARCA?')
	ccp_2 = fields.Char(related='crm_odt_id.ccp_2',string='¿Qué resultados obtuvieron?')
	cdp_1 = fields.Char(related='crm_odt_id.cdp_1',string='¿Qué medios se utilizarán para la implementación?')
	cdp_2 = fields.Char(related='crm_odt_id.cdp_2',string='¿Qué medios se utilizarán para la difusión?')
	cdp_3 = fields.Char(related='crm_odt_id.cdp_3',string='¿Qué medios se utilizarán para la participación?')
	qz_12 = fields.Char(related='crm_odt_id.qz_12',string='¿CUÁL ES EL MARCO LEGAL?(RTC, SEGOB, PROFECO, MICROSITIOS Y PROMOWEB)')
	qz_13 = fields.Char(related='crm_odt_id.qz_13',string='¿HAY REQUERIMIENTO ADICIONALES? /n Medios de datos y consideraciones creativas, mandatorios con respecto al uso de la marca, aspectos legales, manejo de los modulos,etc')
	qz_14 = fields.Char(related='crm_odt_id.qz_14',string='¿HAY UN ESTIMADO DE PRESUPUESTO?')
	qz_15 = fields.Char(related='crm_odt_id.qz_15',string='¿CUÁLES SON LOS ENTREGABLES?')
	qz_16 = fields.Char(related='crm_odt_id.qz_16',string='¿SE TRABAJARA EN CONJUNCO CON ALGUNA AGENCIA DE LA MARCA?')
	product = fields.Char(related='crm_odt_id.product',string='Producto', track_visibility=True)
	project = fields.Many2one('project.project',related='crm_odt_id.project',string='Proyecto', track_visibility=True)
	term_promo_date = fields.Date(related='crm_odt_id.term_promo_date',string='Vigencia de la promocion', track_visibility=True)
	temporalidad = fields.Char(related='crm_odt_id.temporalidad',string='Temporalidad', track_visibility=True)
	slogan_marca = fields.Char(related='crm_odt_id.slogan_marca',string='Eslogan', track_visibility=True)
	logo_marca = fields.Binary(related='crm_odt_id.logo_marca',string='Logo', track_visibility=True)
	personal = fields.Char(string='Personal', track_visibility=True)
	propiedad = fields.Char(string='PROPIEDAD:', track_visibility=True)
	descrption = fields.Text(string='Descrpicion', track_visibility=True)

	# BTL/PDV
	activation = fields.Boolean(string='Activación', track_visibility=True)
	mystery_shopper = fields.Boolean(string='Mystery Shopper', track_visibility=True)
	promotoria = fields.Boolean(string='Promotoria', track_visibility=True)
	sumpling = fields.Boolean(string='Sampling', track_visibility=True)
	production_material = fields.Boolean(string='Producción de Materiales', track_visibility=True)
	production_promocionales = fields.Boolean(string='Producción de Promocionales', track_visibility=True)
	auto_servicio  = fields.Boolean(string='Auto Servicio', track_visibility=True)
	departament   = fields.Boolean(string='Departamentales', track_visibility=True)
	centro_comercial  = fields.Boolean(string='Centros Comerciales', track_visibility=True)
	calle  = fields.Boolean(string='Calles', track_visibility=True)
	otros  = fields.Boolean(string='Otros (Por favor detallar actividad)', track_visibility=True)
	others = fields.Text(string='Otros', track_visibility=True)
	vigencia = fields.Date(string='Vigencia', track_visibility=True)
	activ_days = fields.Integer(string='Dias a Activar', size='3', track_visibility=True)
	coverage = fields.Char(string='Cobertura', track_visibility=True)
	material_apoyo = fields.Text(string='Materiales de apoyo (Descripción y Cantidad)', track_visibility=True)
	comentarios_add = fields.Text(string='Comentarios Adicionales', track_visibility=True)
	listado_tiendas = fields.Text(string='Listado de Tiendas', track_visibility=True)
	btl = fields.Float(related='crm_odt_id.btl',string='BTL/PDV P. Autorizado', track_visibility=True)
	firma1_btl = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_btl = fields.Binary(string='Firma 2', track_visibility=True)
	c_promocion = fields.Char(string='PROMOCIÓN: ', track_visibility=True)
	c_clave = fields.Char(string='CLAVE: ', track_visibility=True)
	c_fecha = fields.Date(string='FECHA: ', track_visibility=True)
	c_direccion = fields.Char(string='DIRECCIÓN: ', track_visibility=True)
	c_gerencia = fields.Char(string='GERENCIA: ', track_visibility=True)
	c_solicita = fields.Many2one('hr.employee',string='SOLICITA: ', track_visibility=True)
	c_proveedor = fields.Many2one('res.partner',string='PROVEEDOR: ', track_visibility=True)
	tabla_material_btl = fields.One2many('odt.materiales', 'material_id')
	tabla_cotizacion_btl = fields.One2many('odt.cotizacion','cotizacion_id')
	total_precio_unitario_btl = fields.Float(string='Total P. Unitario',compute=_btl_totales)
	total_costo_proveedor_btl = fields.Float(string='Total Proveedor',compute=_btl_totales)

		# Produccion
	p_spot_radio = fields.Boolean(string='Spot Radio', track_visibility=True)
	p_spot_tv = fields.Boolean(string='Spot TV (Live Action)', track_visibility=True)
	p_spot_tv1 = fields.Boolean(string='Spot TV (Mtion Graphics)', track_visibility=True)
	p_cap_digital = fields.Boolean(string='Cápsula Digital', track_visibility=True)
	p_cineminuto = fields.Boolean(string='Video', track_visibility=True)
	p_lev_imagen = fields.Boolean(string='Cpsula / Mencin', track_visibility=True)
	p_pieca = fields.Boolean(string='Jingle', track_visibility=True)
	p_super = fields.Boolean(string='Video Corporativo', track_visibility=True)
	p_shooting_photo = fields.Boolean(string='Inclusion de Grafico', track_visibility=True)
	p_edicion_video = fields.Boolean(string='Inclusion de super', track_visibility=True)
	p_post_video = fields.Boolean(string='Otro', track_visibility=True)
	p_cortinilla = fields.Boolean(string='Duracion', track_visibility=True)
	p_reel = fields.Boolean(string='Descripcion', track_visibility=True)
	p_render = fields.Boolean(string='Render', track_visibility=True)
	p_locucion = fields.Boolean(string='Locución o Música', track_visibility=True)
	p_edicion_audio = fields.Boolean(string='Edición de Video', track_visibility=True)
	p_gif = fields.Boolean(string='Gif', track_visibility=True)
	p_ftp = fields.Boolean(string='FTP Especificaciones', track_visibility=True)
	p_otros = fields.Boolean(string='Otros', track_visibility=True)
	p_otro_text = fields.Text(string='Otros', track_visibility=True)
	duracion = fields.Char(string='Duración', track_visibility=True)
	descripcion = fields.Text(string='Descripción', track_visibility=True)
	tipo_trabajo = fields.Selection([('1','Proyecto Cobrado'),('2','Proyecto Bonificado'),('3','Proyecto a Cotizar')], track_visibility=True)
	firma1_prod = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_prod = fields.Binary(string='Firma 2', track_visibility=True)
	produccion = fields.Float(related='crm_odt_id.produccion',string='Produccion P. Autorizado', track_visibility=True)
	tabla_material_produccion = fields.One2many('odt.materiales.produccion', 'material_produccion_id')
	tabla_cotizacion_produccion = fields.One2many('odt.cotizacion.produccion','cotizacion_produccion_id')
	total_cliente_produ = fields.Float(string='Total Cliente',compute=_produccion_totales)
	total_gtvo_produ = fields.Float(string='Total GTVP',compute=_produccion_totales)
	total_terceros_produ = fields.Float(string='Total Terceros',compute=_produccion_totales)
	total_interno_produ = fields.Float(string='Total Interno',compute=_produccion_totales)
	total_recuperacion_produ = fields.Float(string='Total Recuperacion',compute=_produccion_totales)

		# Diseño 
	d_presentacion = fields.Boolean(string='Presentación', track_visibility=True)
	d_template = fields.Boolean(string='Template', track_visibility=True)
	d_master_graph = fields.Boolean(string='MasterGraphic', track_visibility=True)
	d_adaptacion_pop = fields.Boolean(string='Adaptacion a POP', track_visibility=True)
	d_adaptacion_digital = fields.Boolean(string='Adaptación a Digital', track_visibility=True)
	d_adaptacion_ooh = fields.Boolean(string='Adaptación a OOH', track_visibility=True)
	d_logotipo = fields.Boolean(string='Logotipo', track_visibility=True)
	d_presentacion = fields.Boolean(string='Visualización', track_visibility=True)
	d_otro = fields.Boolean(string='Otros', track_visibility=True)
	d_otro_desc = fields.Text(string='Especificar', track_visibility=True)
	dc_especificacion = fields.Text(string='Comentarios y especificaciones', track_visibility=True)
	firma1_design = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_design = fields.Binary(string='Firma 2', track_visibility=True)
	diseño_creatividad = fields.Float(related='crm_odt_id.diseño_creatividad',string='Diseño P. Autorizado', track_visibility=True)
	tabla_material_diseno = fields.One2many('odt.materiales.diseno', 'material_diseno_id')
	tabla_cotizacion_diseno = fields.One2many('odt.cotizacion.diseno','cotizacion_diseno_id')
	total_cliente_diseno = fields.Float(string='Total Cliente',compute=_diseno_totales)
	total_gtvo_diseno = fields.Float(string='Total GTVP',compute=_diseno_totales)
	total_terceros_diseno = fields.Float(string='Total Terceros',compute=_diseno_totales)
	total_interno_diseno = fields.Float(string='Total Interno',compute=_diseno_totales)
	total_recuperacion_diseno = fields.Float(string='Total Recuperacion',compute=_diseno_totales)

	#Estrategia
	e_conc_promo = fields.Boolean(string='Concepto Promocional', track_visibility=True)
	e_conc_camp = fields.Boolean(string='Concepto de Campaña', track_visibility=True)
	e_mec_promv = fields.Boolean(string='Mecánica Promocional', track_visibility=True)
	e_estr_difu = fields.Boolean(string='Estrategia de Difusión', track_visibility=True)
	e_guion_r20 = fields.Boolean(string='Guión spot radio 20"', track_visibility=True)
	e_guion_r30 = fields.Boolean(string='Guión spot radio 30"', track_visibility=True)
	e_guion_10 = fields.Boolean(string='Guión spot radio 10"', track_visibility=True)
	e_guion_cineminuto = fields.Boolean(string='Guión Cineminuto', track_visibility=True)
	e_guion_capsula = fields.Boolean(string='Guión cápsula Tv/Web', track_visibility=True)
	e_copy = fields.Boolean(string='Copy', track_visibility=True)
	e_slogan = fields.Boolean(string='Slogan', track_visibility=True)
	e_naming = fields.Boolean(string='Naming', track_visibility=True)
	e_mailing = fields.Boolean(string='Mailing', track_visibility=True)
	e_creat_BTL = fields.Boolean(string='Creatividad BTL', track_visibility=True)
	e_concept = fields.Boolean(string='Concepto de eventos', track_visibility=True)
	e_otros = fields.Boolean(string='Otros', track_visibility=True)
	e_otro_text = fields.Text(string='Especificar', track_visibility=True)
	e_more_details = fields.Text(string='Mas Detalles', track_visibility=True)
	estrategia = fields.Float(related='crm_odt_id.estrategia',string='Estrategia P. Autorizado', track_visibility=True)
	firma1_estrategia = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_estrategia = fields.Binary(string='Firma 2', track_visibility=True)
	tabla_cotizacion_estrategia = fields.One2many('odt.cotizacion.estrategia','cotizacion_estrat_id')	
	total_cliente_estrategia = fields.Float(string='Total Cliente',compute=_estrategia_totales)
	total_gtvo_estrategia = fields.Float(string='Total GTVP',compute=_estrategia_totales)
	total_terceros_estrategia = fields.Float(string='Total Terceros',compute=_estrategia_totales)
	total_interno_estrategia = fields.Float(string='Total Interno',compute=_estrategia_totales)
	total_recuperacion_estrategia = fields.Float(string='Total Recuperacion',compute=_estrategia_totales)

	#Logistica
	tipo_promo = fields.Selection([('1','SEGOB'),('2','PROFECTO'),('3','RTC')], string='Tipo de promoción', track_visibility=True)
	mecanica_partici = fields.Text(string='Mecánica de participación', track_visibility=True)	
	total_ganador = fields.Char(string='Total ganadores', track_visibility=True)
	total_premio = fields.Char(string='Total Premios', track_visibility=True)
	total_ganador_premio = fields.Char(string='Total ganadores por tipo de premio', track_visibility=True)
	valor_premio = fields.Char(string='Valor de premios', track_visibility=True)
	caract_premio = fields.Text(string='Domensiones y pesos de premios', track_visibility=True)
	vigencia_promo = fields.Date(string='Vigencia de la promoción', track_visibility=True)
	geo_cobertura = fields.Text(string='Cobertura Geografica', track_visibility=True)
	firma1_logistica = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_logistica = fields.Binary(string='Firma 2', track_visibility=True)

	# 	 Gestoria
	gl_date_sorteo = fields.Date(string='Fecha del Sorteo', track_visibility=True)
	site_sorteo = fields.Char(string='Lugar del Sorteo', track_visibility=True)
	description_premio = fields.Text(string='Descripcion del premios', track_visibility=True)
	description_by_premio = fields.Text(string='Cantidad, dimensiones y peso por tipo de premios', track_visibility=True)
	valor_primio = fields.Text(string='Valor por tipo de premio', track_visibility=True)
	lugar_enterga_premio = fields.Text(string='Lugar de entrega del premio', track_visibility=True)
	dates_hrs_entrega = fields.Text(string='Fecha(s) y horario(s) de entrega de premios', track_visibility=True)
	responsable_promo = fields.Char(string='Responsable de la promocion', track_visibility=True)
	dl_comments = fields.Text(string='Comentarios adicionales', track_visibility=True)
	clave_proyecto = fields.Char(string='Clave del Proyecto', track_visibility=True)
	social_reason = fields.Char(string='Razon Social', track_visibility=True)
	respons_promocion = fields.Many2one('res.partner', string='Responsable de la Promocion', track_visibility=True)
	respons_trato_personal = fields.Many2one('hr.employee',string='Resposnsable de tratamiento de datos personales', track_visibility=True)
	name_promo = fields.Char(string='Nombre de la Promocion', track_visibility=True)
	geo_cobertura = fields.Char(string='Cobertura Geografica', track_visibility=True)
	vigencia_promo = fields.Char(string='Vigencia de la promocion', track_visibility=True)
	dl_sorteo = fields.Boolean(string='Sorteo', track_visibility=True)
	gl_concurso = fields.Boolean(string='Concurso', track_visibility=True)
	gr_rtc = fields.Boolean(string='RTC', track_visibility=True)
	gl_canje = fields.Boolean(string='Canje / Coleccionable', track_visibility=True)
	gl_otra = fields.Boolean(string='Otra', track_visibility=True)
	gl_vigencia_permiso = fields.Date(string='Vigencia del Permiso:', track_visibility=True)
	gl_talon_boleto = fields.Boolean(string='Talon / Boleto', track_visibility=True)
	gl_electr_boleto = fields.Boolean(string='Boleto electronico', track_visibility=True)
	gl_formacion_num = fields.Boolean(string='Formacion de Numeros', track_visibility=True)
	gl_sistema_info = fields.Boolean(string='Sistema Informatico "Random"', track_visibility=True)
	gl_sorteo_insta = fields.Boolean(string='Sorteo Instantaneo', track_visibility=True)
	gl_cal_gana = fields.Boolean(string='Calcula y Gana', track_visibility=True)
	gl_predeterminado = fields.Boolean(string='Predeterminado', track_visibility=True)
	gl_juego_linea = fields.Boolean(string='Juego en Linea', track_visibility=True)
	gl_mayor_puntaje = fields.Boolean(string='Mayor Puntaje', track_visibility=True)
	gl_con_otro = fields.Boolean(string='Otro', track_visibility=True)
	cert_foios = fields.Boolean(string='Certificacion de Folios (Predeterminados)', track_visibility=True)
	det_ganadores = fields.Boolean(string='Determinacion de Ganadores', track_visibility=True)
	entrega_premio = fields.Boolean(string='Entrega de premios', track_visibility=True)
	gl_description_premio = fields.Text(string='Descripcion de Premios a otorgar y valor unitario', track_visibility=True)
	gl_mecanica = fields.Text(string='Mecanica de participación', track_visibility=True)
	universal = fields.Boolean(string='Universal', track_visibility=True)
	excelsior = fields.Boolean(string='Excelsior', track_visibility=True)
	novedades = fields.Boolean(string='Novedades', track_visibility=True)
	la_prensa = fields.Boolean(string='La Prensa', track_visibility=True)
	el_record = fields.Boolean(string='El Record', track_visibility=True)
	publimetro = fields.Boolean(string='Publimetro', track_visibility=True)
	esto = fields.Boolean(string='Esto', track_visibility=True)
	jornada = fields.Boolean(string='La Jornada', track_visibility=True)
	gl_preiodico_otros = fields.Boolean(string='Otros', track_visibility=True)
	pagina_web = fields.Char(string='Pagina Web', track_visibility=True)
	extra = fields.Text(string='Fecha y lugar de entrega de premios mayores a 1,500 Salarios(Minimo vigente)', track_visibility=True)
	gl_observations = fields.Text(string='Observaciones', track_visibility=True)
	tabla_cotizacion_gestoria = fields.One2many('odt.cotizacion.gestoria','cotizacion_gestoria_id', track_visibility=True)
	total_cliente_gestoria = fields.Float(string='Total Cliente',compute=_gestoria_totales)
	total_gtvo_gestoria = fields.Float(string='Total GTVP',compute=_gestoria_totales)
	total_terceros_gestoria = fields.Float(string='Total Terceros',compute=_gestoria_totales)
	total_interno_gestoria = fields.Float(string='Total Interno',compute=_gestoria_totales)
	total_recuperacion_gestoria = fields.Float(string='Total Recuperacion',compute=_gestoria_totales)
	gestoria = fields.Float(related='crm_odt_id.gestoria_logistica',string='Gestoria P. Autorizado', track_visibility=True)
	firma1_gestoria = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_gestoria = fields.Binary(string='Firma 2', track_visibility=True)

	# Contact Center
	cc_telefono = fields.Boolean(string='Teléfono', track_visibility=True)
	cc_whats = fields.Boolean(string='WhatsApp', track_visibility=True)
	cc_email = fields.Boolean(string='E-mail', track_visibility=True)
	cc_twitter = fields.Boolean(string='Twitter', track_visibility=True)
	cc_face = fields.Boolean(string='Facebook', track_visibility=True)
	cc_chat = fields.Boolean(string='Chat', track_visibility=True)
	cc_escritorio = fields.Boolean(string='Escritorio', track_visibility=True)
	cc_otro = fields.Boolean(string='Otro', track_visibility=True)
	cc_especificar = fields.Text(string='Especificar', track_visibility=True)

	tipo_servicio1 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', default='1', track_visibility=True)
	dictaminacion1 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes1 = fields.Boolean(string='Lunes', track_visibility=True)
	martes1 = fields.Boolean(string='Martes', track_visibility=True)
	miercoles1 = fields.Boolean(string='Miércoles', track_visibility=True)
	jueves1 = fields.Boolean(string='Jueves', track_visibility=True)
	viernes1 = fields.Boolean(string='Viernes', track_visibility=True)
	sabado1 = fields.Boolean(string='Sábado', track_visibility=True)
	domingo1 = fields.Boolean(string='Domingo', track_visibility=True)
	festivos1 = fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart1 = fields.Datetime(string='Hora inicial', track_visibility=True)
	atencionend1 = fields.Datetime(string='Hora Término', track_visibility=True)

	tipo_servicio2 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', default='1', track_visibility=True)
	dictaminacion2 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes2 = fields.Boolean(string='Lunes', track_visibility=True)
	martes2 = fields.Boolean(string='Martes', track_visibility=True)
	miercoles2= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves2= fields.Boolean(string='Jueves', track_visibility=True)
	viernes2= fields.Boolean(string='Viernes', track_visibility=True)
	sabado2= fields.Boolean(string='Sábado', track_visibility=True)
	domingo2= fields.Boolean(string='Domingo', track_visibility=True)
	festivos2=fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart2= fields.Datetime(string='Hora inicial', track_visibility=True)
	atencionend2= fields.Datetime(string='Hora Término', track_visibility=True)

	tipo_servicio3 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', default='1', track_visibility=True)
	dictaminacion3 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes3= fields.Boolean(string='Lunes', track_visibility=True)
	martes3= fields.Boolean(string='Martes', track_visibility=True)
	miercoles3= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves3= fields.Boolean(string='Jueves', track_visibility=True)
	viernes3= fields.Boolean(string='Viernes', track_visibility=True)
	sabado3= fields.Boolean(string='Sábado', track_visibility=True)
	domingo3= fields.Boolean(string='Domingo', track_visibility=True)
	festivos3= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart3= fields.Datetime(string='Hora inicial', track_visibility=True)
	atencionend3= fields.Datetime(string='Hora Término', track_visibility=True)

	tipo_servicio4 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', default='1', track_visibility=True)
	dictaminacion4 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes4= fields.Boolean(string='Lunes', track_visibility=True)
	martes4= fields.Boolean(string='Martes', track_visibility=True)
	miercoles4= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves4= fields.Boolean(string='Jueves', track_visibility=True)
	viernes4= fields.Boolean(string='Viernes', track_visibility=True)
	sabado4= fields.Boolean(string='Sábado', track_visibility=True)
	domingo4= fields.Boolean(string='Domingo', track_visibility=True)
	festivos4= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart4= fields.Datetime(string='Hora inicial', track_visibility=True)
	atencionend4= fields.Datetime(string='Hora Término', track_visibility=True)

	tipo_servicio5 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', default='1', track_visibility=True)
	dictaminacion5 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes5= fields.Boolean(string='Lunes', track_visibility=True)
	martes5= fields.Boolean(string='Martes', track_visibility=True)
	miercoles5= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves5= fields.Boolean(string='Jueves', track_visibility=True)
	viernes5= fields.Boolean(string='Viernes', track_visibility=True)
	sabado5= fields.Boolean(string='Sábado', track_visibility=True)
	domingo5= fields.Boolean(string='Domingo', track_visibility=True)
	festivos5= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart5= fields.Datetime(string='Hora inicial', track_visibility=True)
	atencionend5= fields.Datetime(string='Hora Término', track_visibility=True)

	tipo_servicio6 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', default='1', track_visibility=True)
	dictaminacion6 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes6= fields.Boolean(string='Lunes', track_visibility=True)
	martes6= fields.Boolean(string='Martes', track_visibility=True)
	miercoles6= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves6= fields.Boolean(string='Jueves', track_visibility=True)
	viernes6= fields.Boolean(string='Viernes', track_visibility=True)
	sabado6= fields.Boolean(string='Sábado', track_visibility=True)
	domingo6= fields.Boolean(string='Domingo', track_visibility=True)
	festivos6= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart6= fields.Datetime(string='Hora inicial', track_visibility=True)
	atencionend6= fields.Datetime(string='Hora Término', track_visibility=True)

	tipo_servicio7 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', default='1', track_visibility=True)
	dictaminacion7 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes7= fields.Boolean(string='Lunes', track_visibility=True)
	martes7= fields.Boolean(string='Martes', track_visibility=True)
	miercoles7= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves7= fields.Boolean(string='Jueves', track_visibility=True)
	viernes7= fields.Boolean(string='Viernes', track_visibility=True)
	sabado7= fields.Boolean(string='Sábado', track_visibility=True)
	domingo7= fields.Boolean(string='Domingo', track_visibility=True)
	festivos7= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart7= fields.Datetime(string='Hora inicial', track_visibility=True)
	atencionend7= fields.Datetime(string='Hora Término', track_visibility=True)

	tipo_servicio8 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', default='1', track_visibility=True)
	dictaminacion8 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes8 = fields.Boolean(string='Lunes', track_visibility=True)
	martes8 = fields.Boolean(string='Martes', track_visibility=True)
	miercoles8 = fields.Boolean(string='Miércoles', track_visibility=True)
	jueves8 = fields.Boolean(string='Jueves', track_visibility=True)
	viernes8 = fields.Boolean(string='Viernes', track_visibility=True)
	sabado8 = fields.Boolean(string='Sábado', track_visibility=True)
	domingo8 = fields.Boolean(string='Domingo', track_visibility=True)
	festivos8 = fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart8 = fields.Datetime(string='Hora inicial', track_visibility=True)
	atencionend8 = fields.Datetime(string='Hora Término', track_visibility=True)
	firma1_contact = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_contact = fields.Binary(string='Firma 2', track_visibility=True)

	
	# tabla_cotizacion_callcenter = fields.One2many('odt.cotizacion.callcenter','cotizacion_callcenter_id')

	# total_cliente_callcenter = fields.Float(string='Total Cliente',compute=_callcenter_totales)
	# total_gtvo_callcenter = fields.Float(string='Total GTVP',compute=_callcenter_totales)
	# total_terceros_callcenter = fields.Float(string='Total Terceros',compute=_callcenter_totales)
	# total_interno_callcenter = fields.Float(string='Total Interno',compute=_callcenter_totales)
	# total_recuperacion_callcenter = fields.Float(string='Total Recuperacion',compute=_callcenter_totales)
	# call_center = fields.Float(related='crm_odt_id.call_center',string='Call Center P. Autorizado')

	# 	# Marketing Digital
	dg_web = fields.Boolean(string='Pagina web / micrositio', track_visibility=True)
	dg_galeria_video = fields.Boolean(string='Galeria de Videos', track_visibility=True)
	dg_descr = fields.Text(string='Descripcion General', track_visibility=True)
	dg_aplications = fields.Boolean(string=' Video Juego / aplicacion', track_visibility=True)
	dg_social_net = fields.Boolean(string='Redes sociales', track_visibility=True)
	dg_pautadg = fields.Boolean(string='Pauta digital', track_visibility=True)
	dg_promoweb = fields.Boolean(string='Promoweb', track_visibility=True)
	dg_estrategi = fields.Boolean(string='Estratega', track_visibility=True)
	dg_mantenimiento = fields.Boolean(string='Mantenimiento Mensual', track_visibility=True)
	dg_galeria = fields.Boolean(string='Galeria de fotos', track_visibility=True)
	dg_camara = fields.Boolean(string='Camara en vivo', track_visibility=True)
	dg_calendar = fields.Boolean(string='Calendario', track_visibility=True)
	dg_otro = fields.Boolean(string='Otro', track_visibility=True)
	dg_otro_detalle = fields.Text(string='Detallar', track_visibility=True)
	dg_sistema_votacion = fields.Boolean(string='Sistema de votacion', track_visibility=True)
	dg_registro = fields.Boolean(string='Registro de participacion', track_visibility=True)
	dg_newsletter = fields.Boolean(string='Newsletter', track_visibility=True)
	dg_trivias = fields.Boolean(string='Trivias', track_visibility=True)
	dg_aplications_realtime = fields.Boolean(string='Aplicacion de reportes en tiempo real', track_visibility=True)
	dg_descripcion_va = fields.Text(string='Descripcion', track_visibility=True)
	n_niveles = fields.Integer(string='Numero de niveles', track_visibility=True)
	dg_opt_1 = fields.Boolean(string='Animacion 2D', track_visibility=True)
	dg_opt_2 = fields.Boolean(string='Animacion 3D', track_visibility=True)
	dg_opt_3 = fields.Boolean(string='Plataforma IOS', track_visibility=True)
	dg_opt_4 = fields.Boolean(string='Plataforma Android', track_visibility=True)
	dg_opt_5 = fields.Boolean(string='Plataforma Sitio web', track_visibility=True)
	dg_opt_6 = fields.Boolean(string='Plataforma Facebook', track_visibility=True)
	dg_opt_7 = fields.Boolean(string='Facebook', track_visibility=True)
	dg_opt_8 = fields.Boolean(string='Youtube', track_visibility=True)
	dg_opt_9 = fields.Boolean(string='Linked in', track_visibility=True)
	dg_opt_10 = fields.Boolean(string='Foursquare', track_visibility=True)
	dg_opt_11 = fields.Boolean(string='Twitter', track_visibility=True)
	dg_opt_12 = fields.Boolean(string='Pinterest', track_visibility=True)
	dg_opt_13 = fields.Boolean(string='Instagram', track_visibility=True)
	dg_opt_14 = fields.Boolean(string='Otros', track_visibility=True)
	dg_propuesta = fields.Text(string='Propuestas', track_visibility=True)
	dg_presupuesto = fields.Char(string='Presupuesto', track_visibility=True)
	dg_objetivos = fields.Char(string='Objeticos', track_visibility=True)
	dg_alcance = fields.Char(string='Alcance', track_visibility=True)
	dg_banner = fields.Char(string='Banners', track_visibility=True)
	dg_observations = fields.Char(string='Observaciones', track_visibility=True)
	dg_opt_15 = fields.Boolean(string='Banner Principal', track_visibility=True)
	dg_opt_16 = fields.Boolean(string='Banner Secundario', track_visibility=True)
	dg_opt_17 = fields.Boolean(string='Contenidos Editoriales', track_visibility=True)
	dg_opt_18 = fields.Boolean(string='Promocion', track_visibility=True)
	dg_opt_19 = fields.Boolean(string='E-mailing', track_visibility=True)
	dg_opt_20 = fields.Boolean(string='Dominio', track_visibility=True)
	dg_opt_21 = fields.Boolean(string='Hosting', track_visibility=True)
	dg_opt_22 = fields.Boolean(string='Otro', track_visibility=True)
	dg_sub_detalle = fields.Boolean(string='Detalle', track_visibility=True)
	dg_opt_23 = fields.Boolean(string='Sistema Random', track_visibility=True)
	dg_opt_24 = fields.Boolean(string='Generacion de codigos Unicos', track_visibility=True)
	dg_cant_codigos = fields.Integer(string='Cantidad de Codigos', track_visibility=True)
	dg_cant_digitos = fields.Integer(string='Cantidad de Digitos', track_visibility=True)
	dg_opt_25 = fields.Boolean(string='Numericos', track_visibility=True)
	dg_opt_26 = fields.Boolean(string='Alfa numericos', track_visibility=True)
	dg_otros = fields.Text(string='Otro', track_visibility=True)
	firma1_digital = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_digital = fields.Binary(string='Firma 2', track_visibility=True)
	digital = fields.Float(related='crm_odt_id.digital',string='Marketing Digital P. Autorizado')

	tabla_cotizacion_digital = fields.One2many('odt.cotizacion.digital','cotizacion_digital_id')
	total_costo_interno_digital = fields.Float(string='Costo total interno',compute=_digital_totales)
	total_pago_terceros_digital = fields.Float(string='Pago a Terceros',compute=_digital_totales)
	total_recuperacion_digital = fields.Float(string='Recuperacion',compute=_digital_totales)
	total_costo_cliente_digital = fields.Float(string='Costo Cliente',compute=_digital_totales)
	total_monto_venta_digital = fields.Float(string='Monto de Venta',compute=_digital_totales)

	#	Medios
	med_folio = fields.Char(string='Folio', track_visibility=True)
	med_fecha_soli = fields.Datetime(string='Fecha de solicitud', track_visibility=True)
	med_hora_soli = fields.Datetime(string='Hora de Solicitud', track_visibility=True)
	med_fecha_entrega = fields.Datetime(string='Fecha Estimada de Entrega', track_visibility=True)
	med_fecha_real = fields.Datetime(string='Fecha Real de Entrega', track_visibility=True)
	med_elabora = fields.Char(string='Elaborará este Plan', track_visibility=True)
	med_nivel_complejidad = fields.Char(string='Nivel de complejidad', track_visibility=True)

	# odt medios
	med_odt_fecha_entrega = fields.Datetime(string='Fecha de entrega solicitada', track_visibility=True)
	med_clave_proyecto = fields.Char(string='Clave de Proyecto', track_visibility=True)
	med_tipo_trabajo = fields.Selection([('1','Revisión de Pauta'),('2','Análisis'),('3','Plan de Medios')], string='Tipo de Trabajo Requerido', track_visibility=True)
	# Plan de medios
	med_objetivo_comunicacion = fields.Char(string='Objetivo de comunicación', track_visibility=True)
	med_presupuesto_cliente = fields.Char(string='Presupuesto Global Cliente', track_visibility=True)
	med_periodo_camap = fields.Char(string='Periodo camapaña y/o promoción', track_visibility=True)
	med_tipo_analisis = fields.Selection([('1','Inversión Publicitarioa (Competencia)'),('2','Audiencia (Ratings)'),('3','Hábitos de Consumo (BIMSA)')],string='Tipo de Análisis', track_visibility=True)
	med_oberv_generales = fields.Text(string='Observaciones Generales', track_visibility=True)
	med_solicita = fields.Char(string='Nombre de quien solicita', track_visibility=True)
	med_getente = fields.Char(string='Gerente Medios', track_visibility=True)
	med_dirc_comercial = fields.Char(string='Dirección Comercial', track_visibility=True)
	med_icepresidencia = fields.Char(string='Vicepresidencia', track_visibility=True)

	#Solicitud TVSA
	tvsa_tipo_camp = fields.Selection([('1','TEASER'),('2','LANZAMIENTO'),('3','REGULAR')],string='Timpo de Campaña', track_visibility=True)
	tvsa_otro = fields.Char(string='Otro: (Especificar)')
	tvsa_catego_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
										('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
										('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
										('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido')], string='Categoria Televisa', track_visibility=True)
	tvsa_nse = fields.Selection([('1','ABC+ Alto + Medio alto'),('2','c Medio'),('3','D+ Medio Bajo'),('4','DE Bajo')], string="NSE", track_visibility=True)

	tvsa_grupo_edad_1 = fields.Boolean(string='4 - 12', track_visibility=True)
	tvsa_grupo_edad_2 = fields.Boolean(string='13 - 18', track_visibility=True)
	tvsa_grupo_edad_3 = fields.Boolean(string='19 - 29', track_visibility=True)
	tvsa_grupo_edad_4 = fields.Boolean(string='30 - 44', track_visibility=True)
	tvsa_grupo_edad_5 = fields.Boolean(string='45 - 54', track_visibility=True)
	tvsa_grupo_edad_6 = fields.Boolean(string='55+', track_visibility=True)
	tvsa_grupo_edad_otro = fields.Char(string='Otro', track_visibility=True)
	tvsa_sexo_p = fields.Boolean(string='Personas', track_visibility=True)
	tvsa_sexo_m = fields.Boolean(string='Mujeres', track_visibility=True)
	tvsa_sexo_h = fields.Boolean(string='Hombres', track_visibility=True)
	tvsa_rol_family = fields.Selection([('1','Jefes de Familia'),('2','Amas de Casa'),('3','Responsables de niños')],string='Rol Familiar', track_visibility=True)
	years_03 = fields.Boolean(string='0 a 3 años', track_visibility=True)
	years_48 = fields.Boolean(string='4 a 8 años', track_visibility=True)
	years_912 = fields.Boolean(string='9 a 12 años', track_visibility=True)
	target_secundario = fields.Char(string='Target Secundario', track_visibility=True)

	duracion_spot = fields.Char(string='Duración Spot', track_visibility=True)
	opcion_compra = fields.Selection([('1','CPR MODULOS'),('2','CPR FRANJAS'),('3','MIXTO MÓDULO Y FRANJA'),('4','CPR POR PROGRAMA'),('5','SPOTEO'),('6','SPOTEO COMPRA LIBRE')],string='Opciones de Compra', track_visibility=True)
	mixto_proporcion = fields.Char(string='En caso de ser Mixto especificar promoción', track_visibility=True)
	target_compra_modulo = fields.Char(string='Target de compra Módulos o Franja', track_visibility=True)
	target_especial = fields.Char(string='En caso de ser Target de compra Especial, Especificar', track_visibility=True)

	#regualcion
	cofepris = fields.Selection([('1','SI'),('2','NO')],string='COFEPRIS', track_visibility=True)
	a_favor = fields.Selection([('1','SI'),('2','NO')],string='A favor de lo mejor', track_visibility=True)
	kids_policy = fields.Selection([('1','SI'),('2','NO')],string='Kids Policy', track_visibility=True)
	sptv_periodo_camp1 = fields.Char(string='Periodo de la Campaña', track_visibility=True)
	canal_1 = fields.Boolean(string='2', track_visibility=True)
	canal_2 =  fields.Boolean(string='5', track_visibility=True)
	canal_3 =  fields.Boolean(string='9', track_visibility=True)
	tvsa_abierta = fields.Integer(string='Monto Máximo inversion TV abierta nacional (Costo clienten)', track_visibility=True)
	tv_abierta_duracion_spot = fields.Datetime(string='Duracion del Spot', track_visibility=True)

	canal_local = fields.Boolean(string='Canal Local', track_visibility=True)
	bloqueos = fields.Boolean(string='Bloqueos', track_visibility=True)
	sptv_periodo_camp2 = fields.Char(string='Periodo de la Campaña', track_visibility=True)
	foro_tv = fields.Boolean(string='Foro TV', track_visibility=True)
	foro_tv_descrip = fields.Text(string='Box', track_visibility=True)
	monto_inverison_tvabierta = fields.Float(string='Monto Maximo inversion TV Abierta Local (Costo Cliente)', track_visibility=True)
	tvsa_abierta_observaciones = fields.Text(string='Observaciones generales o condiciones especiales', track_visibility=True)

	# AAEETV

	aaee_categoria_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
										('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
										('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
										('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido')], string='Categoria Televisa', track_visibility=True)
	target_primario = fields.Char(string='Target Primario', track_visibility=True)
	tarjet_secudario = fields.Char(string='Target Secunndario', track_visibility=True)

	aaeetv_periodo_camp = fields.Char(string='Periodo de la Campaña', track_visibility=True)
	aaee_monto_maximo = fields.Float(string='Monto Máximon Propuesta (Costo Cliente)', track_visibility=True)
	aaee_monto_minimo = fields.Float(string='Monto Minimo Propuesta (Costo Cliente)', track_visibility=True)
	aaeetv_2 = fields.Boolean(string='2', track_visibility=True)
	aaeetv_5 = fields.Boolean(string='5', track_visibility=True)
	aaeetv_9 = fields.Boolean(string='9', track_visibility=True)
	aaeetv_foro_tv = fields.Boolean(string='Foro TV', track_visibility=True)
	conoce_programas = fields.Char(string='Si conoce el(los) programa(s) indicar', track_visibility=True)


	box_bool = fields.Boolean(string='Box', track_visibility=True)
	canal5_bool = fields.Boolean(string='Canal 5', track_visibility=True)
	canal9_bool = fields.Boolean(string='Canal 9', track_visibility=True)
	comedia_bool = fields.Boolean(string='Comedia', track_visibility=True)
	revista_bool = fields.Boolean(string='De Revista', track_visibility=True)
	deportivos_bool = fields.Boolean(string='Deportivos', track_visibility=True)
	foro_tv_bool = fields.Boolean(string='Foro TV', track_visibility=True)
	lucha_bool = fields.Boolean(string='Lucha Libre', track_visibility=True)
	noticiero_bool = fields.Boolean(string='Noticieros', track_visibility=True)

	box_text = fields.Text(string='Acciones', track_visibility=True)
	canal5_text = fields.Text(string='Acciones', track_visibility=True)
	canal9_text = fields.Text(string='Acciones', track_visibility=True)
	comedia_text = fields.Text(string='Acciones', track_visibility=True)
	revista_text = fields.Text(string='Acciones', track_visibility=True)
	foro_tv_text = fields.Text(string='Acciones', track_visibility=True)
	lucha_text = fields.Text(string='Acciones', track_visibility=True)
	noticiero_text = fields.Text(string='Acciones', track_visibility=True)
	deportivo_text = fields.Text(string='Acciones', track_visibility=True)
	box_selection = fields.Selection([('1','Super'),('2','Banner'),('3','Mención 10"'),('4','Mención 20"'),('5','Cortinilla a corte'),('6','Patrocinio de Programa'),('7','Patrocinio de Sección')], string='Box', track_visibility=True)
	
	canal5_selection = fields.Selection([('1','Edición creativa'),('2','Cortinilla a corte'),('3','L en contenido'),('4','Patrocinio de programa'),('5','Promos Vea'),('6','Social TV'),('7','BUG (Logo)')], string='Canal 5', track_visibility=True)
	
	canal9_selection = fields.Selection([('1','Patrocinio de programa'),('2','Cortinilla a corte')],string='Canal 9', track_visibility=True)
	
	comedia_selection = fields.Selection([('1','Cortinilla a corte'),('2','Avance del Programa'),('3','Patrocinio de programa')],string='Comedia', track_visibility=True)
	
	revista_selection = fields.Selection([('1','Pleca'),('2','Super'),('3','Banner'),('4','Mención 30"'),('5','Mención 60"'),
								('6','Mención 120"'),('7','Promos Vea'),('8','Patrocinio de Programa'),('9','Patrocinio de sección'),
								('10','Entrevista 60"'),('11','Entrevista 120"'),('12','Bumper'),('13','Wiper')], string='De Revista', track_visibility=True)
	
	deportivos_selection = fields.Selection([('1','Pleca'),('2','Super'),('3','Banner'),('4','Cortinilla a corte'),
											 ('5','Promos Vea'),('6','Mención 30"'),('7','Mención 60"'),('8','Patrocinio de sección'),('9','Patrocinio de sección con pie'),('10','Patrocinio de programa')], string='Deportivos', track_visibility=True)
	
	foro_tv_selection = fields.Selection([('1','Entrevista'),('2','Desarrollo de Tema'),('3','Mención 60"'),('4','INT Activa con Mención de Marca'),
										  ('5','Integración Activa'),('6','Integración Ambiental"'),('7','Mención 60"'),('8','Patrocinio de sección (5" + 5")'),
										  ('9','Patrocinio de sección (5" + 5")+LOGO'),('10','Patrocinio programa')], string='Foro Tv', track_visibility=True)
	
	lucha_libre_selection = fields.Selection([('1','Super'),('2','Banner'),('3','Mención 10"'),('4','Mención 30"'),('5','Mención 60"'),('6','Mención 120"'),('7','Cortinilla a corte'),
									('8','Patrocinio de Programa'),('9','Patrocinio de Sección'),('10','Patrocinio de sección con pie')], string='Lucha Libre AAA', track_visibility=True)
	
	noticieros_selection = fields.Selection([('1','Pleca'),('2','Super'),('3','Banner'),('4','Cortinilla a corte'),('5','Promos Vea'),('6','Avance del Programa'),
								 ('7','Patrocinio de Programa'),('8','Patrocinio de sección'),('9','Resumen Informativo')],string='Noticieros', track_visibility=True)


	aaeetv_abierta_local_periodo_camp = fields.Char(string='Periodo de la camapaña', track_visibility=True)
	tabla_plaza = fields.One2many('odt.medios.plaza','plazas_id')
	aaeetv_abierta_monto_maximo = fields.Float(string='Monto Maximo Propuesta (Costo cliente)', track_visibility=True)
	aaeetv_abierta_monto_maximo = fields.Float(string='Monto Minimo Propuesta (Costo cliente)', track_visibility=True)
	aaeee_observations = fields.Text(string='Observaciones', track_visibility=True)

	# Brief aaee
	tv_abierta_bool = fields.Boolean(string='TV Abierta', track_visibility=True)
	tv_local_bool = fields.Boolean(string='TV Local', track_visibility=True)
	Network_bool = fields.Boolean(string='Network', track_visibility=True)
	area_comercial_selection = fields.Selection([('1','Gabriela Martínez'),('2','Maricarmen Lobo'),('3','Pamela Urrutia'),('4','Brenda Aguirre'),('5','Vanessa Fuentes'),('6','Alejandra Cárdenas')],string='Dirección Área Comercial', track_visibility=True)
	brief_presupuesto_minimo = fields.Float(string='Presupuesto Estimado minimo (a costo cliente)', track_visibility=True)
	brief_presupuesto_maximo = fields.Float(string='Presupuesto Estimado maximo (a costo cliente)', track_visibility=True)
	braa_elabora = fields.Char(string='Elabora', track_visibility=True)
	braa_fecha = fields.Datetime(string='Fecha', track_visibility=True)
	braa_periodo = fields.Char(string='Periodo', track_visibility=True)
	braa_nombre_proyecto = fields.Char(string='Nombre o Tema del Proyecto', track_visibility=True)
	braa_descripcion_personalidad = fields.Text(string='Descrpición y personalidad del producto', track_visibility=True)
	braa_objetivo = fields.Text(string='Objetivo', track_visibility=True)
	braa_idea_comunicar = fields.Text(string='Idea a Comunicar', track_visibility=True)
	braa_ambiente_contexto = fields.Text(string='Ambiente o contexto compatible', track_visibility=True)
	braa_talento_personaje = fields.Text(string='En caso de requerirse talento, Caracteristicas de los personajes', track_visibility=True)
	braa_propuesta_idea = fields.Text(string='Propuesta o idea creativa (si la hay)', track_visibility=True)

	braa_opcion1 = fields.Boolean(string='Telenovela', track_visibility=True)
	braa_opcion2 = fields.Boolean(string='Revista', track_visibility=True)
	braa_opcion3 = fields.Boolean(string='Series', track_visibility=True)
	braa_opcion4 = fields.Boolean(string='Infantiles', track_visibility=True)
	braa_opcion5 = fields.Boolean(string='Repeticiones', track_visibility=True)
	braa_opcion6 = fields.Boolean(string='Reality', track_visibility=True)
	braa_opcion7 = fields.Boolean(string='Noticiero', track_visibility=True)
	braa_opcion8 = fields.Boolean(string='Comedia', track_visibility=True)
	braa_opcion9 = fields.Boolean(string='Deportivo', track_visibility=True)
	braa_opcion10 = fields.Boolean(string='Foro TV', track_visibility=True)

	braa_programa_especifico = fields.Text(string='Programa(s) Especifico(s) si ya se conoce(n)', track_visibility=True)
	braa_acciones = fields.Text(string='Acciones o Necesidades, Explicar: ', track_visibility=True)

	# medios = fields.Monetary(string='Medios P. Autorizado')


	@api.model
	def _read_group_stage_ids(self, stages, domain, order):

		team_id = self._context.get('default_team_id')
		if team_id:
			search_domain = ['|', ('id', 'in', stages.ids), '|', ('team_id', '=', False), ('team_id', '=', team_id)]
		else:
			search_domain = ['|', ('id', 'in', stages.ids), ('team_id', '=', False)]

		# perform search
		stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
		return stages.browse(stage_ids)

	def _stage_find(self, team_id=False, domain=None, order='sequence'):
		""" Determine the stage of the current lead with its teams, the given domain and the given team_id
			:param team_id
			:param domain : base search domain for stage
			:returns crm.stage recordset
		"""
		# collect all team_ids by adding given one, and the ones related to the current leads
		team_ids = set()
		if team_id:
			team_ids.add(team_id)
		for lead in self:
			if lead.team_id:
				team_ids.add(lead.team_id.id)
		# generate the domain
		if team_ids:
			search_domain = ['|', ('team_id', '=', False), ('team_id', 'in', list(team_ids))]
		else:
			search_domain = [('team_id', '=', False)]
		# AND with the domain in parameter
		if domain:
			search_domain += list(domain)
		# perform search, return the first found
		return self.env['crm.stage'].search(search_domain, order=order, limit=1)




class MediosDiseno(models.Model):
	_name = 'odt.medios.plaza'

	plazas_id = fields.Many2one("odt.crm",ondelete='cascade')
	plaza = fields.Char(string='Plaza(s)')
	tipo_accion = fields.Char(string='Tipo de Acción')

class MaterialesBTL(models.Model):
	_name = 'odt.materiales'

	material_id = fields.Many2one("odt.crm",ondelete='cascade')
	quantity = fields.Integer(string='Cantidad')
	tipo_material = fields.Selection([('1','Demostradora'),('2','Demo edecán'),('3','Promotor'),('4','Animador'),('5','Edecán A'),
									 ('6','Edecán AA'),('7','Edecán AAA'),('8','Gio A'),('9','Gio AA'),('10','Gio AAA'),('11','Modelos'),
									 ('12','Otros')],string='Tipo Material')
	medidas_formatos = fields.Char(string='Medidas / formatos')

class MaterialesProduccion(models.Model):
	_name = 'odt.materiales.produccion'

	material_produccion_id = fields.Many2one("odt.crm",ondelete='cascade')
	quantity = fields.Integer(string='Cantidad')
	tipo_material = fields.Char(string='Especificaciones de Material')
	medidas_formatos = fields.Char(string='Medidas / formatos / duracion')

class MaterialesDiseno(models.Model):
	_name = 'odt.materiales.diseno'

	material_diseno_id = fields.Many2one("odt.crm",ondelete='cascade')
	tipo_material = fields.Char(string='Tipo de Material')
	medidas = fields.Char(string='Medidas')
	formatos = fields.Char(string='Formatos')

# Cotizaicones
class CotizacionesBTL(models.Model):
	_name = 'odt.cotizacion'
		
	cotizacion_id = fields.Many2one('odt.crm')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	semanas = fields.Integer(string='Semanas')
	precio_unitario_btl = fields.Float(string='Precio Unitario')
	costo_proveedor_btl = fields.Float(string='Costo Proveedor')

class CotizacionesProduccion(models.Model):
	_name = 'odt.cotizacion.produccion'
		
	cotizacion_produccion_id = fields.Many2one('odt.crm',ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')

class CotizacionesDiseno(models.Model):
	_name = 'odt.cotizacion.diseno'
		
	cotizacion_diseno_id = fields.Many2one('odt.crm', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')

class CotizacionesEstategia(models.Model):
	_name = 'odt.cotizacion.estrategia'
		
	cotizacion_estrat_id = fields.Many2one('odt.crm', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')

class CotizacionesGestoria(models.Model):
	_name = 'odt.cotizacion.gestoria'
		
	cotizacion_gestoria_id = fields.Many2one('odt.crm', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	precio_uni_gtvp = fields.Float(string='Precio unitario')
	costo_cliente = fields.Float(string='Costo sugerido para cliente')
	pago_terceros = fields.Float(string='Pago a Terceros')
	costo_venta_cliente = fields.Float(string='Costo venta cliente*')

class CotizacionesCallcenter(models.Model):
	_name = 'odt.cotizacion.callcenter'
		
	cotizacion_callcenter_id = fields.Many2one('odt.crm', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')

class CotizacionesDigital(models.Model):
	_name = 'odt.cotizacion.digital'
		
	cotizacion_digital_id = fields.Many2one('odt.crm', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	periodo = fields.Char(string='Periodicidad')
	cantidad = fields.Integer(string='Cantidad')
	meses = fields.Char(string='Meses')
	horas = fields.Integer(string='Horas de servicio')
	costo_hora = fields.Float(string='Costo por Hora')
	costo_interno = fields.Float(string='*Costo Interno', compute='_costo_interno')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	recuperacion = fields.Float(string='*Costo minimo de recuperacion')
	costo_cliente = fields.Float(string='*Costo Cliente')
	monto_venta = fields.Float(string='*Monto de Venta')

	@api.depends('horas','costo_hora','costo_interno')
	def _costo_interno(self):
		self.costo_interno = (self.costo_hora * self.horas )
		


class TipoGasto(models.Model):	
	_name = 'odt.tipo.gasto'

	name = fields.Char(string='Tipo de Gasto')

class ColumnasSaleOrder(models.Model):
	_inherit = 'sale.order.line'

	tipo_gasto = fields.Selection([('1','BTL/PDV'),('2','Produccion'),('3','Diseño'),('4','Gestoria'),('5','Contact Center'),('6','Marketing Digital'),('7','Medios'),('8','Logistica'),('9','Estrategia')], string='Area Gasto')


class Gastos(models.Model):
	"""docstring for Gastos"""
	_name = 'project.gastos'
	

	gastos_id = fields.Many2one('project.project')
	fac_gastos = fields.Float(string='Factura gasto')
	disviacion = fields.Float(string='Desviacion')

class TablaGastos(models.Model):
	_inherit = 'project.project'


	tabla_gastos = fields.One2many('project.gastos','gastos_id')
	odt = fields.Many2one('odt.crm',string='ODT', domain="[('crm_odt_id.partner_id','=',partner_id)]")
	ref_project = fields.Many2one('crm.lead',string='Proyecto', compute='get_sale_order_reference')
	fin_clave = fields.Char(string='CLAVE')
	u_bruta_p = fields.Float(string='U. Bruta P', compute='_compute_saldo_autorizado')
	u_bruta_r = fields.Float(string='U. Bruta R')
	dates = fields.Date(related='ref_project.date_deadline', string='Fecha')
	ref_customer = fields.Many2one(related='partner_id', string='Cliente')
	total_pagar = fields.Float(string='planificado', compute='get_sale_order_total')
	saldo_autorizado = fields.Float(string='saldo autorizado', compute='_compute_saldo_autorizado')
	btl = fields.Float(related='ref_project.btl', string='BTL')
	produccion = fields.Float(related='ref_project.produccion',string='Produccion')
	diseño_creatividad = fields.Float(related='ref_project.diseño_creatividad',string='Diseño y Creatividad ')
	gestoria_logistica = fields.Float(related='ref_project.gestoria_logistica',string='Gestoria')
	call_center = fields.Float(related='ref_project.call_center',string='Contact Center')
	digital = fields.Float(related='ref_project.digital',string='Marketing Digital')
	medios = fields.Float(related='ref_project.medios',string='Medios')

    # @api.multi
    # def get_productwise_commission(self):
    #     sum_line_tipo_gasto = []
    #     for order in self:
    #         for line in order.sale_order_line:
    #         	if self.sale_order_id.tipo_gasto 
    #             sum_line_tipo_gasto.append((line.tipo_gasto * line.product_id.sales_manager_commission)/100)
    #             sum_line_tipo_gasto.
    #         amount_manager = sum(sum_line_manager)
    #     return amount_person

	@api.one
	def get_sale_order_reference(self):
		for rec in self:
			res = rec.env['sale.order'].search([('id', '=', self.sale_order_id.id)], limit=1)
			rec.ref_project = res.opportunity_id.id


	@api.one
	def get_sale_order_total(self):
		for rec in self:
			res = rec.env['sale.order'].search([('id', '=', self.sale_order_id.id)], limit=1)
			rec.total_pagar = float(res.amount_total)


# planificado es total a cobrar -los gastos autorizados
	@api.one
	@api.depends('ref_project','saldo_autorizado','u_bruta_p')
	def _compute_saldo_autorizado(self):
		if self.ref_project:
			self.saldo_autorizado = (self.ref_project.btl + self.ref_project.produccion + self.ref_project.diseño_creatividad + self.ref_project.call_center + self.ref_project.digital + self.ref_project.medios)
			self.u_bruta_p = (self.total_pagar - self.saldo_autorizado)
	


class marca_crm(models.Model):
	"""docstring for marca_crm"""
	_name = 'crm_marca'
	_description = 'Informacion acerca de las marcas o empresas'

	name = fields.Char(string='Nombre')

