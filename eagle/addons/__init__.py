# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

""" Addons module.

This module serves to contain all Eagle addons, across all configured addons
paths. For the code to manage those addons, see eagle.modules.

Addons are made available under `eagle.addons` after
eagle.tools.config.parse_config() is called (so that the addons paths are
known).

This module also conveniently reexports some symbols from eagle.modules.
Importing them from here is deprecated.

"""
# make eagle.addons a namespace package, while keeping this __init__.py
# present, for python 2 compatibility
# https://packaging.python.org/guides/packaging-namespace-packages/
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
