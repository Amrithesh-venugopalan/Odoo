# -*- coding: utf-8 -*-

from odoo import models, fields


class PropertyManagementTags(models.Model):
    """class for defining different tags for properties"""

    _name = 'property.management.tags'
    _description = 'Property Characteristics'

    name = fields.Char(string="Property Tag")
