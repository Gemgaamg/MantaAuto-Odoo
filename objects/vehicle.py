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

from openerp.osv import osv
from openerp import pooler, fields, api, models
from openerp.tools.translate import _
class Vehicle(models.Model):
    _name = 'vehicle'
    _description = "Vehiculo"
    name = fields.Char('Descripcion',compute = "get_name" , store = True)
    placa = fields.Char('Placa',size = 9 , required=True)
    
    marca_id = fields.Many2one('vehicle.marca',string='Marca', required=True)
    modelo_id = fields.Many2one('vehicle.modelo',string='Modelo' , required=True)
    chasis = fields.Char('Chasis', required=True)
    motor = fields.Char('Nº Motor', required=True)
    partner_id = fields.Many2one('res.partner',"Dueño del Vehiculo", required=True)
    insurance_id = fields.Many2one('res.partner',"Asegurado por", domain = [('is_insurance','=',True)])
    image = fields.Binary('Imagen')
    color_id = fields.Many2one('color','Color', required=True)
    anio_id = fields.Many2one('vehicle.anio','Año', required=True)
    tipo = fields.Selection([
        ('automovil','Automovil'),
        ('bus','Bus'),
        ('buseta','Buseta'),
        ('camion','Camion'),
        ('camioneta','Camioneta'),
        ('campero','Campero'),
        ('microbus','Microbus'),
        ('tractocamion','Tractocamion'),
        ('motocicleta','Motocicleta'),
        ('motocarro','Motocarro'),
        ('mototriciclo','Mototriciclo'),
        ('cuatrimoto','Cuatrimoto'),
        ('volqueta','Volqueta'),
        ('otro','Otro'),
        ], 
        string = 'Tipo')
   
    _sql_constraints = [
        ('name_vehicle_unique', 'unique(name)', '¡Ya hay un vehiculo con esa descripcion!'),
    ]
    @api.one
    @api.depends('marca_id','modelo_id','placa')
    def get_name(self):
        try:
            self.name = self.marca_id.name +" "+ self.modelo_id.name + " ( "+self.placa+" )"
        except:
            
            pass
        return True

    @api.one
    @api.onchange('marca_id')
    def onchange_marca(self):
        try:
            self.modelo_id = None
        except:
            pass
        return True

class Marca(models.Model):
    _name = 'vehicle.marca'
    _description = "Marca"
    name = fields.Char('Marca')
    modelo_ids = fields.One2many(
            'vehicle.modelo',# modelo relacionado
            'marca_id',
            'Lineas de modelos Disponibles'
    )
    _sql_constraints = [
        ('name_marca_unique', 'unique(name)', '¡Ya exite esa marca de vehiculo!'),
    ]
class Anio(models.Model):
    _name = 'vehicle.anio'
    _description = u"Año"
    _order = 'name'
    name = fields.Char('Año')
    _sql_constraints = [
        ('name_anio_unique', 'unique(name)', '¡Ese año ya esta creado!'),
    ]
class Modelo(models.Model):
    _name = 'vehicle.modelo'
    _description = "Modelo"
    name = fields.Char('Modelo')
    marca_id = fields.Many2one('vehicle.marca', string="Marca", required=True)
    _sql_constraints = [
        ('name_modelo_unique', 'unique(name,marca_id)', '¡Ya exite ese modelo de vehiculo!'),
    ]
class Color(models.Model):
    _name = 'color'
    _description = "Color"
    name = fields.Char('Color')
    _sql_constraints = [
        ('name_color_unique', 'unique(name)', '¡Ya exite ese color!'),
    ]

