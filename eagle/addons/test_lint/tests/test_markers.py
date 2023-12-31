# -*- coding: utf-8 -*-
# Part of Odoo, Eagle ERP See LICENSE file for full copyright and licensing details.

import logging
import os
import eagle
from eagle.tests.common import TransactionCase
from eagle.modules.module import ad_paths

_logger = logging.getLogger(__name__)
MARKERS = [b'<' * 7, b'>' * 7]
EXTENSIONS = ('.py', '.js', '.xml', '.less', '.sass')


class TestConflictMarkers(TransactionCase):

    def check_file(self, fullpath_name):

        with open(fullpath_name, 'rb') as f:
            content = f.read()
            self.assertFalse(any([m in content for m in MARKERS]), 'Conflict markers found in %s' % fullpath_name)

    def test_conflict_markers(self):
        """ Test that there are no conflict markers left in Eagle files """

        counter = 0

        eagle_path = os.path.abspath(os.path.dirname(eagle.__file__))
        paths = ad_paths + [eagle_path]
        paths.remove(os.path.join(eagle_path, 'addons'))  # avoid checking eagle/addons twice

        for p in paths:
            for dp, _, file_names in os.walk(p):
                for fn in file_names:
                    if fn.endswith(EXTENSIONS):
                        self.check_file(os.path.join(dp, fn))
                        counter += 1
        _logger.info('%s files tested', counter)
