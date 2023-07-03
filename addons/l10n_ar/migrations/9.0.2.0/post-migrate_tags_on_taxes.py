# -*- coding: utf-8 -*-

import eagle

def migrate(cr, version):
    registry = eagle.registry(cr.dbname)
    from eagle.addons.account.models.chart_template import migrate_tags_on_taxes
    migrate_tags_on_taxes(cr, registry)
