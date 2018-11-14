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


# class confirm_wizard(models.TransientModel):
#     _name = 'crm.lead'

# 	@api.model
# 	def write(self,values):
# 		stage_detect = self.env['crm.lead'].search([('stage_ids')])
# 		if stage_detect:
# 			print 'yes function'

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

	# @api.depends('tabla_cotizacion')
	# def _tot1_concepto(self):
	# 	self.total_g1 = sum(line.sub_total for line in self.option_lines1)
		

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
	area = fields.Selection([('1','BTL')], 'Area')
	status = fields.Selection([('1','Solicitado'),('2','Cotizado'),('3','Aceptado')])
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
	coverage = fields.Char(string='Cobertura')
	promo_type = fields.Char(string='Tipo de Promocion')
	no_raffle = fields.Integer(string='No. Sorteos')
	propiedad = fields.Char(string='PROPIEDAD:')
	tipo_solicitud = fields.Selection([('1','Creatividad 360'),('2','Creatividad'),('3','Master graphic'),('4','Material pop'),('5','Template'),
									  ('7','Diseño'),('8','Concepto'),('9','Banners promoweb'),('10','Otros')], string='Tipo de Solicitud')
	others = fields.Text(string='Otros')
	descrption = fields.Text(string='Descrpicion')
	tabla_material = fields.One2many('odt.materiales', 'material_id')
	tabla_cotizacion = fields.One2many('odt.cotizacion','cotizacion_id')

	# @api.model
	# def _onchange_user_values(self, user_id):
	# 	""" returns new values when user_id has changed """
	# 	if not user_id:
	# 		return {}
	# 	if user_id and self._context.get('team_id'):
	# 		team = self.env['crm.team'].browse(self._context['team_id'])
	# 		if user_id in team.member_ids.ids:
	# 			return {}
	# 	team_id = self.env['crm.team']._get_default_team_id(user_id=user_id)
	# 	return {'team_id': team_id}

	@api.model
	def _read_group_stage_ids(self, stages, domain, order):
		 # retrieve team_id from the context and write the domain
		# - ('id', 'in', stages.ids): add columns that should be present
		# - OR ('fold', '=', False): add default columns that are not folded
		# - OR ('team_ids', '=', team_id), ('fold', '=', False) if team_id: add team columns that are not folded
		team_id = self._context.get('default_team_id')
		if team_id:
			search_domain = ['|', ('id', 'in', stages.ids), '|', ('team_id', '=', False), ('team_id', '=', team_id)]
		else:
			search_domain = ['|', ('id', 'in', stages.ids), ('team_id', '=', False)]

		# perform search
		stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
		return stages.browse(stage_ids)

	# @api.multi
	# def _compute_kanban_state(self):
	# 	today = date.today()
	# 	for lead in self:
	# 		kanban_state = 'grey'
	# 		if lead.activity_date_deadline:
	# 			lead_date = fields.Date.from_string(lead.activity_date_deadline)
	# 			if lead_date >= today:
	# 				kanban_state = 'green'
	# 			else:
	# 				kanban_state = 'red'
	# 		lead.kanban_state = kanban_state

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

class materiales(models.Model):
	_name = 'odt.materiales'

	material_id = fields.Many2one("odt.crm",ondelete='cascade')
	tipo_material = fields.Char(string='Tipo Material')
	medidas_formatos = fields.Char(string='Medidas / formatos')

class cotizaciones(models.Model):
	_name = 'odt.cotizacion'


	# @api.one
	# @api.depends('price_unit', 'qty', 'option')
	# def _conceptos(self):
	# 	self.precio_uni_gtvp = self.cantidad * self.price_unit
	# 	self.costo_cliente = self.cantidad * self.
	# 	self.pago_terceros = self.


	# @api.depends('option_lines1')
	# def _tot1_concepto(self):
	# 	self.precio_uni_cliente = sum(line.sub_total for line in self.option_lines1)
	# 	self.costo_cliente = sum(line.sub_total for line in self.option_lines1)
	# 	self.pago_terceros = sum(line.sub_total for line in self.option_lines1)
		
	cotizacion_id = fields.Many2one('odt.crm', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')

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
											('5','Albañilería'),('6','Pintura'),('7','Pisos')], string='Clasificacion')
	clasi_sistemas = fields.Selection([('1','Hardware'),('2','Software'),('3','Capacitación'),('4','Usuario'),('5','Electricidad'),('6','Internet'),('7','Telefonía'),('8','Antivirus')],string='Clasificacion')
	alias_check = fields.Integer(string='Alias',compute='_alias')	

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

# fecha_ingreso = fields.Date("Fecha de ingreso", default=datetime.today())
# antiguedad = fields.Char("Antiguedad", readonly=True, compute='_compute_ant')
# tipo_de_sangre = fields.Many2one('hr.sangre', "Grupo Sanguineo")
# numero_empleado = fields.Integer('Numero de Empleado')
# fecha_baja =  fields.Date("Fecha de Baja")

