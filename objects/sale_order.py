# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields as field
from openerp import pooler, fields, api, models
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
class SaleOrderReplacement(models.Model):
    _inherit = 'sale.order'
    vehiculo_id = fields.Many2one('vehicle','Vehiculo',
        readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required = True)
    is_insurance = fields.Boolean(related='partner_id.is_insurance')
    cliente_id = fields.Many2one('res.partner','Cliente del seguro',
        readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain = [('is_insurance','=',False), ('customer','=',True)], required = True)
    date_order_end = fields.Datetime('Fecha de entrega')

    #accesorios

    moqueta = fields.Integer('Moquetas')
    tapacubo = fields.Integer('Tapacubos')
    herramientas = fields.Integer('Herramientas')
    espejo = fields.Integer('Espejos')
    seguro_aros= fields.Integer('Seguro de aros')
    pluma = fields.Integer('Plumas')
    llanta= fields.Integer('Llantas')
    
    
    encendedor = fields.Integer('Encendedor')
    memoria_radio = fields.Integer('Memoria Radio')
    cds = fields.Integer('CDS')
    extintor = fields.Integer('Extintor')
    gata = fields.Integer('Gata')
    emblema = fields.Integer('Emblema')
    triangulo = fields.Integer('Triangulo')
    llave_ruedas = fields.Integer('Llave Ruedas')
    botiquin = fields.Integer('Botiquin')
    antena = fields.Integer('Antena')
    tapagas = fields.Integer('Tapagas')

    kilometraje = fields.Char('Kilometraje')
    nivel_gasolina = fields.Char('Nivel de Gasolina')
    order_line = fields.One2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'insurance_setting': [('readonly', False)], 'no_insurance_setting': [('readonly', False)], 'manual': [('readonly', False)]}, copy=True)
    
    
    '''
    ('draft', 'Draft Quotation'),
    ('sent', 'Quotation Sent'),
    ('cancel', 'Cancelled'),
    ('waiting_date', 'Waiting Schedule'),
    ('progress', 'Sales Order'),
    ('manual', 'Sale to Invoice'),
    ('shipping_except', 'Shipping Exception'),
    ('invoice_except', 'Invoice Exception'),
    ('done', 'Done'),
    '''

    state = fields.Selection([
            ('draft', 'Ingreso de vehiculo'),
            ('sent', 'Presupuesto de Ingreso enviado'),
            ('insurance_setting', 'Esperando Ajuste'),
            ('no_insurance_setting', 'Esperando confirmacion'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Esperando Validacion de Factura'),
            ('manual', 'Orden de trabajo en progreso'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ], 'Status', readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
              \nThe exception status is automatically set when a cancel operation occurs \
              in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               but waiting for the scheduler to run on the order date.", select=True)

    order_line_replacement = fields.One2many(
            'sale.order.line.replacement',# modelo relacionado
            'order_id',
            'Lineas de Repuestos para el pedido'
    )
    
    task_line = fields.One2many(
            'task.line',# modelo relacionado
            'order_id',
            'Tareas a Realizar',
    )
    state_line = fields.One2many(
            'state.line',# modelo relacionado
            'order_id',
            'Estado del vehiculo',
    )
    scope_line = fields.One2many(
            'scope.line',# modelo relacionado
            'order_id',
            'Trabajos Adicionales',
    )
    saldo = fields.Float(compute='get_saldo', string='Saldo')
    abono = fields.Float(compute='get_saldo', string='Abono')

    @api.one
    def get_saldo(self):
        #filtra todos los movimientos sean del producto escogido en wl wizard y que se encuentre entre las fechas establecidas
        saldo = 0.0
        abono = 0.0

        for line in self.invoice_ids:
            if line.state in ('open','paid'):
                saldo+=line.residual
                abono+=(line.amount_total-line.residual)
        if saldo == abono == 0:
            saldo = self.amount_total

        self.saldo = saldo
        self.abono = abono

        #raise osv.except_osv('Error!',order.vehiculo_id)
        return True


    def get_line_1(self):  
        order_line = self.env['sale.order.line'].search([('order_id','=',self.id)],order="category_id asc")
        categoria = ""
        orderList = []
        for line in order_line:
            if line.category_id.name != categoria:
                categoria = line.category_id.name
                orderList.append(dict({"product_id":False,"cat":categoria}))
            orderList.append(line)
        return orderList
    def get_line_2(self):  
        order_line = self.env['sale.order.line'].search([('order_id','=',self.id)],order="category_id asc")
        categoria = ""
        orderList = []
        str_line = ""
        price_subtotal = 0
        for line in order_line:
            if line.category_id.name != categoria:
                if str_line!="":
                    orderList.append((str_line,price_subtotal))
                    str_line=""
                    price_subtotal=0
                categoria = line.category_id.name
                orderList.append(categoria)

            str_line+=line.product_id.name+"/"
            price_subtotal+=line.price_subtotal
        if str_line!="":
            orderList.append((str_line,price_subtotal))
            str_line=""
            price_subtotal=0
        return orderList
    

   

   
    @api.one
    def _multi_images_count(self):
        self.multi_images_count = len(self.multi_images)
        return True
    multi_images = fields.One2many('multi.images.sale.order','order_id','Multi Imagenes')
    multi_images_count = fields.Integer(compute='_multi_images_count', string='# de imagenes')
    attachments =  fields.Many2many('ir.attachment',string="Attachments")


    @api.one
    @api.onchange('partner_id')
    def oncha_parter_id(self):
        datos = super(SaleOrderReplacement,self).onchange_partner_id(self.partner_id.id,context = None)['value']
        self.partner_invoice_id =datos['partner_invoice_id']
        self.user_id            = self.partner_id.user_id and self.partner_id.user_id.id or self._uid
        self.partner_shipping_id=datos['partner_shipping_id']
        self.payment_term       =datos['payment_term']
        try:
            self.pricelist_id       =datos['pricelist_id']
        except:
            pass
        try:
            self.section_id         =datos['section_id']
        except:
            pass

        if self.is_insurance:
            self.cliente_id = None
        else:
            self.cliente_id = self.partner_id
        
        return True

    def action_wait_insurance_setting(self, cr, uid, ids, context=None):
        #raise osv.except_osv('1','asdscasdasd')
        #raise osv.except_osv('1',self.browse(cr, uid, ids).is_insurance)
        if self.browse(cr, uid, ids).is_insurance:
            self.write(cr, uid, ids, {'state': 'insurance_setting'})
        else:
            #self.write(cr, uid, ids, {'state': 'router'})
            self.write(cr, uid, ids, {'state': 'no_insurance_setting'})
        return True

    def action_button_confirm_insurance_setting(self, cr, uid, ids, context=None):
        self.signal_workflow(cr, uid, ids, 'order_confirm_insurance_setting')
        return True
    def action_button_confirm_no_insurance_setting(self, cr, uid, ids, context=None):
        self.signal_workflow(cr, uid, ids, 'order_confirm_insurance_setting')
        return True






class sale_advance_payment_inv(osv.osv_memory):
    _inherit = "sale.advance.payment.inv"
    def create_invoices(self, cr, uid, ids, context=None):
        """ create invoices for the active sales orders """
        sale_obj = self.pool.get('sale.order')
        act_window = self.pool.get('ir.actions.act_window')
        wizard = self.browse(cr, uid, ids[0], context)
        sale_ids = context.get('active_ids', [])
        #raise osv.except_osv('1',sale_ids)
        sale_obj.action_wait(cr, uid, sale_ids,context = None)
        return super(sale_advance_payment_inv,self).create_invoices(cr, uid, ids, context)
        

class multi_images_sale_order(osv.osv):
    _name = "multi.images.sale.order"
    
    image = fields.Binary('Imagen')
    description = fields.Char('Descripcion')
    title = fields.Char('Titulo')
    order_id = fields.Many2one('sale.order','Pedido')
    name = fields.Char('Descripcion', compute="get_name")
    @api.one
    def get_name(self):
        self.name = self.title
        return True

class DetalleSaleOrder(models.Model):
    _inherit = 'sale.order.line'
    #order_insurance_id = fields.Many2one('sale.order')
    category_id = fields.Many2one('order.line.category', 'Categoria', required=True,readonly=True, states={'draft': [('readonly', False)]})
    _sql_constraints = [
        ('category_product_order_order_unique', 'unique(category_id,product_id,order_id)', '¡Ya hay una combinacion de esa categoria con ese producto!'),
    ]

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        """Prepare the dict of values to create the new invoice line for a
           sales order line. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record line: sale.order.line record to invoice
           :param int account_id: optional ID of a G/L account to force
               (this is used for returning products including service)
           :return: dict of values to create() the invoice line
        """
        res = {}
        if not line.invoiced:
            if not account_id:
                if line.product_id:
                    account_id = line.product_id.property_account_income.id
                    if not account_id:
                        account_id = line.product_id.categ_id.property_account_income_categ.id
                    if not account_id:
                        raise osv.except_osv(_('Error!'),
                                _('Please define income account for this product: "%s" (id:%d).') % \
                                    (line.product_id.name, line.product_id.id,))
                else:
                    prop = self.pool.get('ir.property').get(cr, uid,
                            'property_account_income_categ', 'product.category',
                            context=context)
                    account_id = prop and prop.id or False
            uosqty = self._get_line_qty(cr, uid, line, context=context)
            uos_id = self._get_line_uom(cr, uid, line, context=context)
            pu = 0.0
            if uosqty:
                pu = round(line.price_unit * line.product_uom_qty / uosqty,
                        self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Price'))
            fpos = line.order_id.fiscal_position or False
            account_id = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, account_id)
            if not account_id:
                raise osv.except_osv(_('Error!'),
                            _('There is no Fiscal Position defined or Income category account defined for default properties of Product categories.'))
            res = {
                'name': line.name,
                'sequence': line.sequence,
                'origin': line.order_id.name,
                'account_id': account_id,
                'price_unit': pu,
                'quantity': uosqty,
                'discount': line.discount,
                'category_id': line.category_id.id,
                'uos_id': uos_id,
                'product_id': line.product_id.id or False,
                'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
                'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
            }

        return res
class Category(models.Model):
    _name = 'order.line.category'
    _description = "Categoria de pedido"
    name = fields.Char("Categoria",required = True)
    _sql_constraints = [
        ('name_category_unique', 'unique(name)', '¡Esta categoria ya esta creada!'),
    ]

class DetalleSaleOrderReplacement(models.Model):
    _name = 'sale.order.line.replacement'
    _description = "Lineas de repuestos para autos"
    product_id = fields.Many2one('product.product',string="Repuesto", ondelete='restrict',required = True)
    qty = fields.Integer('Cantidad',required = True)
    order_id = fields.Many2one('sale.order')

class TaskLine(models.Model):
    _name = 'task.line'
    _description = "Tareas"
    tarea_id = fields.Many2one('task',"Tarea",required = True)
    order_id = fields.Many2one('sale.order')
class StateLine(models.Model):
    _name = 'state.line'
    _description = "Estado"
    name = fields.Char('Estado',required = True)
    order_id = fields.Many2one('sale.order')

class Task(models.Model):
    _name = 'task'
    _description = "Tarea"
    name = fields.Char("Tarea",required = True)
    _sql_constraints = [
        ('name_task_unique', 'unique(name)', '¡Esta tarea ya esta creada!'),
    ]

class ScopeLine(models.Model):
    _name = 'scope.line'
    _description = "Alcance"
    name = fields.Char("Tarea Adicional",required = True)
    date = fields.Datetime("Fecha",required = True)
    order_id = fields.Many2one('sale.order')
    _defaults = {
        'date': field.datetime.now,
        }
        