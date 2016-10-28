# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module is Copyright (c) 2009-2013 General Solutions (http://gscom.vn) All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : "MantaAuto",
    "version" : "1.0",
    "author" : "RubikSoft",
    'website': 'http://www.facebook.com/RubikSoft15',
    "description": """
Personalizacion para empresa MantaAuto
==============================

Gestiona:

    * Hojas de Ingreso de vehiculos
    * Aseguradoras
    * Vehiculos
    * Repuestos

    """,

    "depends" : [
            "sale",
            #"web_slider_widget",
            "web_tree_image",
            "web_widget_multi_image"
            ],
    
    'js': [],
    'qweb': [], 
    "data" : [
        'objects/replacement_view.xml',
        'objects/vehicle_view.xml',
        'objects/vehicle_marca_view.xml',
        'objects/sale_order_view.xml',
        'objects/partner_view.xml',
        'objects/account_invoice_view.xml',
        'objects/sale_order_workflow.xml',
        'objects/sale_order_images_view.xml',
        'views/menu_manta_auto.xml',
        'reports/proforma.xml',
        'reports/lista_repuesto.xml',
        'reports/hoja_ingreso.xml',
        'reports/prefactura.xml',
        'reports/factura.xml',
        'reports/factura_seguro.xml',

        'wizard/sale_order_advance_report.xml',
        'wizard/sale_order_advance_report_wizard_view.xml',
        
        #'opc_opc_view.xml',
    ],
    "demo" : [],
    "active":True,
    "installable": True,
    "certificate":"",
}

