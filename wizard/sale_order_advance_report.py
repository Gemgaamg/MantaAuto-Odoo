# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import osv
from openerp import fields, api, models
from openerp.tools.translate import _
from openerp.exceptions import Warning
#from datetime import  date, timedelta
from datetime import datetime , timedelta



class hrz_kardex_report(models.Model):
    _name = "sale.order.advance.report"
    _description = u"Por fechas, Por vehículo, Por dueños, Por deudas"


    cliente_id = fields.Many2one('res.partner','Cliente',
        domain = [('is_insurance','=',False), ('customer','=',True)])
    seguro_id = fields.Many2one('res.partner','Aseguradora',
        domain = [('is_insurance','=',True), ('customer','=',True)])
    vehiculo_id = fields.Many2one('vehicle','Vehiculo')
    date_from = fields.Date("Fecha inicio")
    date_to = fields.Date("Fecha Fin")

    entregado = fields.Boolean('Entregado')
    sin_entregar = fields.Boolean('Sin entregar')
    ordenes = []
    
    def _print_report(self, cr, uid, ids, data, context=None):
        raise (_('Error!'), _('Not implemented.'))
    def get_total(self):
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        sumTotal=0.0
        sumAbono=0.0
        sumSaldo=0.0
        if self.ordenes == []:
            self.ordenes = self.get_orders() 
        for line in self.ordenes:
            sumTotal+=line.amount_total
            sumAbono+=line.abono
            sumSaldo+=line.saldo
        return dict({"sumTotal":sumTotal,"sumAbono":sumAbono,"sumSaldo":sumSaldo})
    def get_orders(self):
        #filtra todos los movimientos sean del producto escogido en wl wizard y que se encuentre entre las fechas establecidas
        #movimientos = self.env['sale.order'].search([('cliente_id', '=', self.cliente_id),('seguro_id', '=', self.seguro_id),('create_date', '<', (datetime.strptime(self.date_to, '%Y-%m-%d')+ timedelta(days=1)).strftime('%Y-%m-%d'))])
        #filtros
        print "**********************************************************************"
        orden = None
        if self.ordenes == []:
            filtro = []
            if self.cliente_id:
                filtro.append(('cliente_id', '=', self.cliente_id.id))
            if self.seguro_id:
                filtro.append(('partner_id', '=', self.seguro_id.id))
            if self.vehiculo_id:
                filtro.append(('vehiculo_id', '=', self.vehiculo_id.id))###########33aqui me quede

            if self.date_from:
                filtro.append(('date_order', '>=', self.date_from))
            if self.date_to:
                filtro.append(('date_order', '<', (datetime.strptime(self.date_to, '%Y-%m-%d')+ timedelta(days=1)).strftime('%Y-%m-%d')))

            if self.entregado:
                filtro.append(('state', '=', ('done')))

            if self.sin_entregar:
                filtro.append(('state', 'in',('insurance_setting',
                                                'no_insurance_setting',
                                                'waiting_date',
                                                'progress',
                                                'manual',
                                                'shipping_except',
                                                'invoice_except',)))
                

            #('create_date', '>=', self.date_from),
            #('create_date', '<', (datetime.strptime(self.date_to, '%Y-%m-%d')+ timedelta(days=1)).strftime('%Y-%m-%d'))]
            #raise osv.except_osv('1',filtro)

            orden = self.env['sale.order'].search(filtro,order="partner_id asc, cliente_id asc")
            self.ordenes = orden
        return self.ordenes


    @api.multi
    def check_report(self):
        #raise osv.except_osv('Error!',str(self.get_total()))
        #data = {}
        #data['form']['landscape'] = True
        return self.env['report'].get_action(self, 'manta_auto_personalizacion.report_sale_order_advance')
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
