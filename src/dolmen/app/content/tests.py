# -*- coding: utf-8 -*-

import unittest
import dolmen.app.content
import zope.component
from zope.component.testlayer import ZCMLFileLayer
from zope.testing import doctest
from zope.component.interfaces import IComponentLookup
from zope.configuration import xmlconfig
from zope.container.interfaces import ISimpleReadContainer
from zope.container.traversal import ContainerTraversable
from zope.interface import Interface
from zope.security.management import newInteraction, endInteraction
from zope.security.testing import Principal, Participation
from zope.site.folder import rootFolder
from zope.site.hooks import getSite
from zope.site.site import LocalSiteManager, SiteManagerAdapter
from zope.testing import module


class DolmenAppContentLayer(ZCMLFileLayer):

    def setUp(self):
        ZCMLFileLayer.setUp(self)
        zope.component.hooks.setHooks()

        # Set up site
        site = rootFolder()
        site.setSiteManager(LocalSiteManager(site))
        zope.component.hooks.setSite(site)

    def tearDown(self):
        zope.component.hooks.resetHooks()
        zope.component.hooks.setSite()
        ZCMLFileLayer.tearDown(self)


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        'README.txt',
        globs={"__name__": "dolmen.app.content"},
        optionflags=(doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))
    readme.layer = DolmenAppContentLayer(dolmen.app.content)
    suite.addTest(readme)
    return suite
