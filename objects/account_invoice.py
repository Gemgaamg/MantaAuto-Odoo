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
class accountInvoice(models.Model):
    _inherit = 'account.invoice'
    sale_order_id = fields.Many2one('sale.order','Orden de Trabajo', readonly=True, states={'draft': [('readonly', False)]})
    cliente_id = fields.Many2one(related="sale_order_id.cliente_id", string = 'Cliente', readonly=True)
    vehiculo_id = fields.Many2one(related="sale_order_id.vehiculo_id", string = 'Vehiculo', readonly=True)
    sale_order_amount_untaxed = fields.Float(related="sale_order_id.amount_untaxed", string = 'Subtotal', readonly=True)
    sale_order_amount_tax = fields.Float(related="sale_order_id.amount_tax", string = 'Impuesto', readonly=True)
    sale_order_amount_total = fields.Float(related="sale_order_id.amount_total", string = 'Total', readonly=True)
    @api.multi
    def get_order(self):
        #filtra todos los movimientos sean del producto escogido en wl wizard y que se encuentre entre las fechas establecidas
    	order = self.env['sale.order'].search([('invoice_ids', '=', self.id)])
    	#raise osv.except_osv('Error!',order.vehiculo_id)
    	return order

    @api.multi
    def get_totales(self):  
        invoice_line = self.env['account.invoice.line'].search([('invoice_id','=',self.id)],order="category_id asc")
        categoria = ""
        orderList = []
        str_line = ""
        price_subtotal = 0
        for line in invoice_line:

            if line.category_id.name != categoria:
                if str_line!="":
                    print (dict({"esCategoria":False,"detalle":str_line,"precioU":price_subtotal,"subtotal":price_subtotal}))
                    orderList.append(dict({"esCategoria":False,"detalle":str_line,"precioU":price_subtotal,"subtotal":price_subtotal}))
                    str_line=""
                    price_subtotal=0
                categoria = line.category_id.name
                orderList.append(dict({"esCategoria":True,"cat":categoria}))

            str_line+=line.product_id.name+"/"
            price_subtotal+=line.price_subtotal
        if str_line!="":
            orderList.append(dict({"esCategoria":False,"detalle":str_line,"precioU":price_subtotal,"subtotal":price_subtotal}))
            str_line=""
            price_subtotal=0
        #raise osv.except_osv("porra",str(orderList))
        return orderList
class DetalleInvoice(models.Model):
    _inherit = 'account.invoice.line'
    #order_insurance_id = fields.Many2one('sale.order')
    category_id = fields.Many2one('order.line.category', 'Categoria'
        ,ondelete='restrict', index=True)
    '''
    @api.one
    @api.constrains('category_id', 'product_id','invoice_id')
    def _check_description(self):
        if self.name == self.description:
            raise ValidationError("Fields name and description must be different")
    '''
    _sql_constraints = [
        ('category_product_order_unique', 'unique(category_id,product_id,invoice_id)', '¡Ya hay una combinacion de esa categoria con ese producto!'),
    ]

    #anio_id = fields.Many2one(string='Año', related='libro_id.anio_id',store = True )
