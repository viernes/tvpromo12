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
	btl = fields.Float(string='BTL')
	produccion = fields.Float(string='Produccion')
	diseño_creatividad = fields.Float(string='Diseño y Creatividad ')
	gestoria_logistica = fields.Float(string='Gestoria y Logistica')
	call_center = fields.Float(string='Call Center')
	digital = fields.Float(string='Digital')
	medios = fields.Float(string='Medios')

	@api.multi
	def _compute_odt_count(self):
		count = self.env['odt.crm']
		self.odt_count = count.search_count([('crm_odt_id', 'in', [a.id for a in self])])



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


class odt(models.Model):

	_name = 'odt.crm'
	_description = 'Vista Kanban para visualizar informacion de crm en solo lectura'

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
		self.total_cliente_btl = sum(line.costo_cliente for line in self.tabla_cotizacion_btl)
		self.total_gtvo_btl = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_btl)
		self.total_terceros_btl = sum(line.pago_terceros for line in self.tabla_cotizacion_btl)
		self.total_interno_btl = sum(line.costo_interno for line in self.tabla_cotizacion_btl)
		self.total_recuperacion_btl = sum(line.recuperacion for line in self.tabla_cotizacion_btl)

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

	@api.depends('tabla_cotizacion_gestoria')
	def _gestoria_totales(self):
		self.total_cliente_gestoria = sum(line.costo_cliente for line in self.tabla_cotizacion_gestoria)
		self.total_gtvo_gestoria = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_gestoria)
		self.total_terceros_gestoria = sum(line.pago_terceros for line in self.tabla_cotizacion_gestoria)
		self.total_interno_gestoria = sum(line.costo_interno for line in self.tabla_cotizacion_gestoria)
		self.total_recuperacion_gestoria = sum(line.recuperacion for line in self.tabla_cotizacion_gestoria)

	@api.depends('tabla_cotizacion_callcenter')
	def _callcenter_totales(self):
		self.total_cliente_callcenter = sum(line.costo_cliente for line in self.tabla_cotizacion_callcenter)
		self.total_gtvo_callcenter = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_callcenter)
		self.total_terceros_callcenter = sum(line.pago_terceros for line in self.tabla_cotizacion_callcenter)
		self.total_interno_callcenter = sum(line.costo_interno for line in self.tabla_cotizacion_callcenter)
		self.total_recuperacion_callcenter = sum(line.recuperacion for line in self.tabla_cotizacion_callcenter)


	@api.depends('tabla_cotizacion_digital')
	def _digital_totales(self):
		self.total_cliente_digital = sum(line.costo_cliente for line in self.tabla_cotizacion_digital)
		self.total_gtvo_digital = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_digital)
		self.total_terceros_digital= sum(line.pago_terceros for line in self.tabla_cotizacion_digital)
		self.total_interno_digital = sum(line.costo_interno for line in self.tabla_cotizacion_digital)
		self.total_recuperacion_digital = sum(line.recuperacion for line in self.tabla_cotizacion_digital)
		
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
	area = fields.Selection([('1','BTL'),('2','Produccion'),('3','Diseño'),('4','Gestoria'),('5','Contact Center'),('6','Digital'),('7','Medios'),('8','logistica'),('9','Creatividad')], string='Area')

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
	product = fields.Char(related='crm_odt_id.product',string='Producto')
	project = fields.Many2one('project.project',related='crm_odt_id.project',string='Proyecto')
	term_promo_date = fields.Date(related='crm_odt_id.term_promo_date',string='Vigencia de la promocion')
	temporalidad = fields.Char(related='crm_odt_id.temporalidad',string='Temporalidad')
	slogan_marca = fields.Char(related='crm_odt_id.slogan_marca',string='Eslogan')
	logo_marca = fields.Binary(related='crm_odt_id.logo_marca',string='Logo')
	personal = fields.Char(string='Personal')
	propiedad = fields.Char(string='PROPIEDAD:')
	descrption = fields.Text(string='Descrpicion')

	# BTL
	activation = fields.Boolean(string='Activacion')
	mystery_shopper = fields.Boolean(string='Mystery Shopper')
	promotoria = fields.Boolean(string='Promotoria')
	sumpling = fields.Boolean(string='sumpling')
	production_material = fields.Boolean(string='Produccion de Materiales')
	production_promocionales = fields.Boolean(string='Produccion de Promocionales')
	auto_servicio  = fields.Boolean(string='Auto Servicio')
	departament   = fields.Boolean(string='Departamentales')
	centro_comercial  = fields.Boolean(string='Centros Comerciales')
	calle  = fields.Boolean(string='Calles')
	otros  = fields.Boolean(string='Otros (Por favor detallar actividad)')
	others = fields.Text(string='Otros')
	vigencia = fields.Date(string='Vigencia')
	activ_days = fields.Integer(string='Dias a Activar', size='3')
	coverage = fields.Char(string='Cobertura')
	material_apoyo = fields.Text(string='Materiales de apoyo (Descripcion y cantidad)')
	comentarios_add = fields.Text(string='Comentarios Adicionales')
	listado_tiendas = fields.Text(string='Listado de Tiendas')
	# tabla cotizacion
	tabla_material_btl = fields.One2many('odt.materiales', 'material_id')
	tabla_cotizacion_btl = fields.One2many('odt.cotizacion','cotizacion_id')
	total_cliente_btl = fields.Float(string='Total Cliente',compute=_btl_totales)
	total_gtvo_btl = fields.Float(string='Total GTVP',compute=_btl_totales)
	total_terceros_btl = fields.Float(string='Total Terceros',compute=_btl_totales)
	total_interno_btl = fields.Float(string='Total Interno',compute=_btl_totales)
	total_recuperacion_btl = fields.Float(string='Total Recuperacion',compute=_btl_totales)
	btl = fields.Float(related='crm_odt_id.btl',string='BTL P. Autorizado')

		# Produccion
	p_radio = fields.Boolean(string='Radio')
	p_tv = fields.Boolean(string='TV')
	p_internet = fields.Boolean(string='Internet')
	p_spot = fields.Boolean(string='Spot')
	p_video = fields.Boolean(string='Video')
	p_cpsula = fields.Boolean(string='Cpsula / Mencin')
	p_jingle = fields.Boolean(string='Jingle')
	p_corporativo = fields.Boolean(string='Video Corporativo')
	p_grafico = fields.Boolean(string='Inclusion de Grafico')
	p_soper = fields.Boolean(string='Inclusion de super')
	p_otro = fields.Boolean(string='Otro')
	duracion = fields.Text(string='Duracion')
	p_descripcion = fields.Text(string='Descripcion')
			# - Realizacion
	conduccion = fields.Boolean(string='Conduccion')
	voz = fields.Boolean(string='Voz')
	equipo_grabacion = fields.Boolean(string='Equipo de grabacion')
	equipo_audio = fields.Boolean(string='Equipo de Audio')
	locaci = fields.Boolean(string='Locaci')
	foro = fields.Boolean(string='Foro')
	blue_green = fields.Boolean(string='Blue / Green screen')
	linea = fields.Boolean(string='Linea')
	escaleta = fields.Boolean(string='Escaleta')
	fotografia = fields.Boolean(string='Fotografia')
	maquillaje = fields.Boolean(string='Maquillaje y/o vestimenta')
	p_otros = fields.Boolean(string='Otros')
	otro_descripcion2 = fields.Text(string='Otros')
			# - Servicios Post
	edicion = fields.Boolean(string='Edicion')
	musicalizacion = fields.Boolean(string='Musicalizacion')
	special_efects_2d = fields.Boolean(string='Efectos Especiales 2D')
	special_efects_3d = fields.Boolean(string='Efectos Especiales 3D')
	grafics_2D = fields.Boolean(string='Graficos 2D')
	gradic_3D = fields.Boolean(string='Graficos 3D')
	presu_asignado = fields.Boolean(string='Presupuesto Asignado')
	presu_libre = fields.Boolean(string='Presupuesto Libre')
	p_comments = fields.Text(string='Comentarios y especificaciones')
	p_fotos = fields.Boolean(string='Fotos')
	p_logotipo = fields.Boolean(string='Logotipos')
	p_producto = fields.Boolean(string='Producto')
	p_impresos = fields.Boolean(string='Impresos')
	p_video = fields.Boolean(string='Video')
	cye_otros = fields.Boolean(string='Otros')
	com_otros = fields.Text(string='Otro')
	# Tabla cotizacion
	tabla_material_produccion = fields.One2many('odt.materiales.produccion', 'material_produccion_id')
	tabla_cotizacion_produccion = fields.One2many('odt.cotizacion.produccion','cotizacion_produccion_id')


	total_cliente_produ = fields.Float(string='Total Cliente',compute=_produccion_totales)
	total_gtvo_produ = fields.Float(string='Total GTVP',compute=_produccion_totales)
	total_terceros_produ = fields.Float(string='Total Terceros',compute=_produccion_totales)
	total_interno_produ = fields.Float(string='Total Interno',compute=_produccion_totales)
	total_recuperacion_produ = fields.Float(string='Total Recuperacion',compute=_produccion_totales)
	produccion = fields.Float(related='crm_odt_id.produccion',string='Produccion P. Autorizado')
	firma1 = fields.Binary(string='Firma 1')

		# Diseño y Creatividad
	creativity_360 = fields.Boolean(string='Cretividad 360')
	creativity = fields.Boolean(string='creatividad')
	master_graph = fields.Boolean(string='Master graphic')
	material_pop = fields.Boolean(string='Material Pop')
	template = fields.Boolean(string='Template')
	diseno_presentacion = fields.Boolean(string='Diseño de presentacion')
	concepto = fields.Boolean(string='Conceptop')
	banners = fields.Boolean(string='Banners promoweb')
	dc_otros = fields.Boolean(string='Otro')
	dc_otros_text = fields.Text(string='Otros')
	dc_descripcion = fields.Text(string='Descripcion')
	tabla_material_diseno = fields.One2many('odt.materiales.diseno', 'material_diseno_id')
	tabla_cotizacion_diseno = fields.One2many('odt.cotizacion.diseno','cotizacion_diseno_id')
	d_fotos = fields.Boolean(string='Fotos')
	d_logotipo = fields.Boolean(string='Logotipos')
	d_presentacion = fields.Boolean(string='Presentacion')
	d_impresos = fields.Boolean(string='Impresos')
	d_guidlines = fields.Boolean(string='Guidlines')
	d_referencias = fields.Boolean(string='Referencias de la mesa (campañas, imagenes, criterios)')
	d_otros = fields.Boolean(string='Otros (especificar)')
	d_comments = fields.Text(string='Comentarios')
	dc_especificacion = fields.Text(string='Comentarios y especificaciones')
	total_cliente_diseno = fields.Float(string='Total Cliente',compute=_diseno_totales)
	total_gtvo_diseno = fields.Float(string='Total GTVP',compute=_diseno_totales)
	total_terceros_diseno = fields.Float(string='Total Terceros',compute=_diseno_totales)
	total_interno_diseno = fields.Float(string='Total Interno',compute=_diseno_totales)
	total_recuperacion_diseno = fields.Float(string='Total Recuperacion',compute=_diseno_totales)
	diseño_creatividad = fields.Float(related='crm_odt_id.diseño_creatividad',string='Diseño y Creatividad P. Autorizado')

		# Gestoria y logistica Sorteo
	gl_date_sorteo = fields.Date(string='Fecha del Sorteo')
	site_sorteo = fields.Char(string='Lugar del Sorteo')
	description_premio = fields.Text(string='Descripcion del premios')
	description_by_premio = fields.Text(string='Cantidad, dimensiones y peso por tipo de premios')
	valor_primio = fields.Text(string='Valor por tipo de premio')
	lugar_enterga_premio = fields.Text(string='Lugar de entrega del premio')
	dates_hrs_entrega = fields.Text(string='Fecha(s) y horario(s) de entrega de premios')
	responsable_promo = fields.Char(string='Responsable de la promocion')
	dl_comments = fields.Text(string='Comentarios adicionales')
			# - Concurso
	clave_proyecto = fields.Char(string='Clave del Proyecto')
	social_reason = fields.Char(string='Razon Social')
	respons_promocion = fields.Many2one('res.partner', string='Responsable de la Promocion')
	respons_trato_personal = fields.Many2one('hr.employee',string='Resposnsable de tratamiento de datos personales')
	name_promo = fields.Char(string='Nombre de la Promocion')
	geo_cobertura = fields.Char(string='Cobertura Geografica')
	vigencia_promo = fields.Char(string='Vigencia de la promocion')
			# - Sorteo
	dl_sorteo = fields.Boolean(string='Sorteo')
	gl_concurso = fields.Boolean(string='Concurso')
	gr_rtc = fields.Boolean(string='RTC')
	gl_canje = fields.Boolean(string='Canje / Coleccionable')
	gl_otra = fields.Boolean(string='Otra')
	gl_vigencia_permiso = fields.Date(string='Vigencia del Permiso:')
	gl_talon_boleto = fields.Boolean(string='Talon / Boleto')
	gl_electr_boleto = fields.Boolean(string='Boleto electronico')
	gl_formacion_num = fields.Boolean(string='Formacion de Numeros')
	gl_sistema_info = fields.Boolean(string='Sistema Informatico "Random"')
	gl_sorteo_insta = fields.Boolean(string='Sorteo Instantaneo')
	gl_cal_gana = fields.Boolean(string='Calcula y Gana')
	gl_predeterminado = fields.Boolean(string='Predeterminado')
	gl_juego_linea = fields.Boolean(string='Juego en Linea')
	gl_mayor_puntaje = fields.Boolean(string='Mayor Puntaje')
	gl_con_otro = fields.Boolean(string='Otro')
	cert_foios = fields.Boolean(string='Certificacion de Folios (Predeterminados)')
	det_ganadores = fields.Boolean(string='Determinacion de Ganadores')
	entrega_premio = fields.Boolean(string='Entrega de premios')
	gl_description_premio = fields.Text(string='Descripcion de Premios a otorgar y valor unitario')
	gl_mecanica = fields.Text(string='Mecanica de participación')
	universal = fields.Boolean(string='Universal')
	excelsior = fields.Boolean(string='Excelsior')
	novedades = fields.Boolean(string='Novedades')
	la_prensa = fields.Boolean(string='La Prensa')
	el_record = fields.Boolean(string='El Record')
	publimetro = fields.Boolean(string='Publimetro')
	esto = fields.Boolean(string='Esto')
	jornada = fields.Boolean(string='La Jornada')
	gl_preiodico_otros = fields.Boolean(string='Otros')
	pagina_web = fields.Char(string='Pagina Web')
	extra = fields.Text(string='Fecha y lugar de entrega de premios mayores a 1,500 Salarios(Minimo vigente)')
	gl_observations = fields.Text(string='Observaciones')
	tabla_cotizacion_gestoria = fields.One2many('odt.cotizacion.gestoria','cotizacion_gestoria_id')

	total_cliente_gestoria = fields.Float(string='Total Cliente',compute=_gestoria_totales)
	total_gtvo_gestoria = fields.Float(string='Total GTVP',compute=_gestoria_totales)
	total_terceros_gestoria = fields.Float(string='Total Terceros',compute=_gestoria_totales)
	total_interno_gestoria = fields.Float(string='Total Interno',compute=_gestoria_totales)
	total_recuperacion_gestoria = fields.Float(string='Total Recuperacion',compute=_gestoria_totales)
	gestoria_logistica = fields.Float(related='crm_odt_id.gestoria_logistica',string='Gestoria y Logistica P. Autorizado')

	# Call Center
	cc_registro = fields.Boolean(string='Registro')
	cc_atencion_promo = fields.Boolean(string='Atencion Promocion')
	cc_atencion = fields.Boolean(string='Atencion')
	cc_otro = fields.Boolean(string='Otros')
	cc_otro_des = fields.Text(string='Detalle actividad')
	cc_day_1 = fields.Boolean(string='Lunes')
	cc_day_2 = fields.Boolean(string='Martes')
	cc_day_3 = fields.Boolean(string='Miercoles')
	cc_day_4 = fields.Boolean(string='Jueves')
	cc_day_5 = fields.Boolean(string='Viernes')
	cc_day_6 = fields.Boolean(string='Sabado')
	cc_day_7 = fields.Boolean(string='Domingo')
	cc_hr_service = fields.Char(string='Horario de Servicio')
	phone_number = fields.Selection([('1','Asignar cualquier numero'),('2','Asignar numero con vanidad'),
								   ('3','Se utilizarán el numero del cliente')], string='Numero 01800 ')
	phone_number_used = fields.Char(string='Numero a usar')
	numero_estacion = fields.Char(string='Numero de estaciones')
	ivr = fields.Text(string='IVR')
	descp_ivr = fields.Text(string='Descripcion del proceso para IVR')
	cc_add_comments = fields.Text(string='Comentarios Adicionales')
	cc_medio_registro = fields.Text(string='Medios de Registro y/o participacion')
	cc_referencia_registro = fields.Text(string='Referencia de registros de proyecto anterior o similar')
	cc_comentarios = fields.Text(string='Comentairos Adicionales')
	tabla_cotizacion_callcenter = fields.One2many('odt.cotizacion.callcenter','cotizacion_callcenter_id')

	total_cliente_callcenter = fields.Float(string='Total Cliente',compute=_callcenter_totales)
	total_gtvo_callcenter = fields.Float(string='Total GTVP',compute=_callcenter_totales)
	total_terceros_callcenter = fields.Float(string='Total Terceros',compute=_callcenter_totales)
	total_interno_callcenter = fields.Float(string='Total Interno',compute=_callcenter_totales)
	total_recuperacion_callcenter = fields.Float(string='Total Recuperacion',compute=_callcenter_totales)
	call_center = fields.Float(related='crm_odt_id.call_center',string='Call Center P. Autorizado')

		#Digital
	dg_web = fields.Boolean(string='Pagina web / micrositio')
	dg_aplications = fields.Boolean(string=' Video Juego / aplicacion')
	dg_social_net = fields.Boolean(string='Redes sociales')
	dg_pautadg = fields.Boolean(string='Pauta digital')
	dg_promoweb = fields.Boolean(string='Promoweb')
	dg_estrategi = fields.Boolean(string='Estratega')
	dg_mantenimiento = fields.Boolean(string='Mantenimiento Mensual')
	dg_galeria = fields.Boolean(string='Galeria de fotos')
	dg_camara = fields.Boolean(string='Camara en vivo')
	dg_calendar = fields.Boolean(string='Calendario')
	dg_otro = fields.Boolean(string='Otro')
	dg_otro_detalle = fields.Text(string='Detallar')
	dg_sistema_votacion = fields.Boolean(string='Sistema de votacion')
	dg_registro = fields.Boolean(string='Registro de participacion')
	dg_newsletter = fields.Boolean(string='Newsletter')
	dg_trivias = fields.Boolean(string='Trivias')
	dg_aplications_realtime = fields.Boolean(string='Aplicacion de reportes en tiempo real')
	dg_descripcion_va = fields.Text(string='Descripcion')
	n_niveles = fields.Integer(string='Numero de niveles')
	dg_opt_1 = fields.Boolean(string='Animacion 2D')
	dg_opt_2 = fields.Boolean(string='Animacion 3D')
	dg_opt_3 = fields.Boolean(string='Plataforma IOS')
	dg_opt_4 = fields.Boolean(string='Plataforma Android')
	dg_opt_5 = fields.Boolean(string='Plataforma Sitio web')
	dg_opt_6 = fields.Boolean(string='Plataforma Facebook')
	dg_opt_7 = fields.Boolean(string='Facebook')
	dg_opt_8 = fields.Boolean(string='Youtube')
	dg_opt_9 = fields.Boolean(string='Linked in')
	dg_opt_10 = fields.Boolean(string='Foursquare')
	dg_opt_11 = fields.Boolean(string='Twitter')
	dg_opt_12 = fields.Boolean(string='Pinterest')
	dg_opt_13 = fields.Boolean(string='Instagram')
	dg_opt_14 = fields.Boolean(string='Otros')
	dg_propuesta = fields.Text(string='Propuestas')
	dg_presupuesto = fields.Char(string='Presupuesto')
	dg_objetivos = fields.Char(string='Objeticos')
	dg_alcance = fields.Char(string='Alcance')
	dg_banner = fields.Char(string='Banners')
	dg_observations = fields.Char(string='Observaciones')
	dg_opt_15 = fields.Boolean(string='Banner Principal')
	dg_opt_16 = fields.Boolean(string='Banner Secundario')
	dg_opt_17 = fields.Boolean(string='Contenidos Editoriales')
	dg_opt_18 = fields.Boolean(string='Promocion')
	dg_opt_19 = fields.Boolean(string='E-mailing')
	dg_opt_20 = fields.Boolean(string='Dominio')
	dg_opt_21 = fields.Boolean(string='Hosting')
	dg_opt_22 = fields.Boolean(string='Otro')
	dg_sub_detalle = fields.Boolean(string='Detalle')
	dg_opt_23 = fields.Boolean(string='Sistema Random')
	dg_opt_24 = fields.Boolean(string='Generacion de codigos Unicos')
	dg_cant_codigos = fields.Integer(string='Cantidad de Codigos')
	dg_cant_digitos = fields.Integer(string='OCantidad de Digitos')
	dg_opt_25 = fields.Boolean(string='Numericos')
	dg_opt_26 = fields.Boolean(string='Alfa numericos')
	dg_otros = fields.Text(string='Otro')
	tabla_cotizacion_digital = fields.One2many('odt.cotizacion.digital','cotizacion_digital_id')
	total_cliente_digital = fields.Float(string='Total Cliente',compute=_digital_totales)
	total_gtvo_digital = fields.Float(string='Total GTVP',compute=_digital_totales)
	total_terceros_digital = fields.Float(string='Total Terceros',compute=_digital_totales)
	total_interno_digital = fields.Float(string='Total Interno',compute=_digital_totales)
	total_recuperacion_digital = fields.Float(string='Total Recuperacion',compute=_digital_totales)
	digital = fields.Float(related='crm_odt_id.digital',string='Digital P. Autorizado')



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
	tipo_material = fields.Char(string='Tipo de Material')
	medidas_formatos = fields.Char(string='Medidas / formatos / duracion')

class MaterialesDiseno(models.Model):
	_name = 'odt.materiales.diseno'

	material_diseno_id = fields.Many2one("odt.crm",ondelete='cascade')
	tipo_material = fields.Char(string='Tipo de Material')
	medidas_formatos = fields.Char(string='Medidas / formatos')

# Cotizaicones
class CotizacionesBTL(models.Model):
	_name = 'odt.cotizacion'
		
	cotizacion_id = fields.Many2one('odt.crm')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')


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

class CotizacionesGestoria(models.Model):
	_name = 'odt.cotizacion.gestoria'
		
	cotizacion_gestoria_id = fields.Many2one('odt.crm', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')

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
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')

class TipoGasto(models.Model):	
	_name = 'odt.tipo.gasto'

	name = fields.Char(string='Tipo de Gasto')

class ColumnasSaleOrder(models.Model):
	_inherit = 'sale.order.line'

	tipo_gasto = fields.Many2one('project.gastos', string='Area de gatos')


class Gastos(models.Model):
	"""docstring for Gastos"""
	_name = 'project.gastos'
	
	_sql_constraints = [('gasto_unique', 'unique (gastos_id,gastos)',     
						'No puedes duplicar el tipo de gasto!')]

	gastos_id = fields.Many2one('project.project')
	gastos = fields.Selection([('1','BTL'),('2','Produccion'),('3','Diseño y Creatividad'),('4','Gestoria y logistica'),('5','Call Center'),('6','Digital'),('7','Medios')], string='Tipo Gasto')
	odt_gastos = fields.Float(string='ODT gasto')
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
	gestoria_logistica = fields.Float(related='ref_project.gestoria_logistica',string='Gestoria y Logistica')
	call_center = fields.Float(related='ref_project.call_center',string='Call Center')
	digital = fields.Float(related='ref_project.digital',string='Digital')
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
			self.u_bruta_p = (self.saldo_autorizado - self.total_pagar)
	


class marca_crm(models.Model):
	"""docstring for marca_crm"""
	_name = 'crm_marca'
	_description = 'Informacion acerca de las marcas o empresas'

	name = fields.Char(string='Nombre')

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

	@api.depends('prove_amount','returned','diferencia','delivery_amount')
	def _total_mejoras(self):
	    self.diferencia = (float(self.delivery_amount)) - (float(self.prove_amount)) - (float(self.returned))
	
class inventory(models.Model):

	_inherit = 'stock.picking'

	return_reason = fields.Char(string='Motivo de la Devolucion')
	receive = fields.Char(string='Quien recibe')
	folio_ganador = fields.Char(string='Folio consecutivo de ganador')
	ejecutivo = fields.Many2one('res.partner', string='Ejecutivo Asignado')
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

