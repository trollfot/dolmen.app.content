#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok
import dolmen.content as dolmen
from dolmen.app.layout import master, IDisplayView
from dolmen.app.content import IDynamicLayout
from zope.interface import Interface
from zope.component import getUtility, getUtilitiesFor, getMultiAdapter
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.container.constraints import checkFactory
from zope.security.management import checkPermission


class ContentActions(grok.Viewlet):
    grok.context(dolmen.IBaseContent)
    grok.viewletmanager(master.DolmenTop)
    grok.require("dolmen.content.View")
    grok.order(50)

    menuname = u'tabs'

    def _get_actions(self):
        menu = getUtility(IBrowserMenu, self.menuname)
        actions = menu.getMenuItems(self.context, self.request)
        if len(actions) <= 1:
            return []
        return actions

    def update(self):
        """Gets the actions and determines which is the selected one.
        """
        self.actions = self._get_actions()
        if self.actions:
            self.contexturl = str(getMultiAdapter(
                (self.context, self.request), name=u"absolute_url")
                )
            self.selected = getattr(self.view, '__name__', None)
            if IDynamicLayout.providedBy(self.context):
                if self.selected == self.context.layout:
                    self.selected = 'index'


class AddMenu(grok.Viewlet):
    grok.context(dolmen.IContainer)
    grok.viewletmanager(master.DolmenTop)
    grok.view(IDisplayView)
    grok.require("dolmen.content.Add")
    grok.order(60)

    def checkFactory(self, name, factory):
        if not checkFactory(self.context, name, factory):
            return False

        permission = dolmen.require.bind().get(factory.factory)
        return checkPermission(permission, self.context)

        
    def update(self):
        self.factories = []
        self.contexturl = str(getMultiAdapter((self.context, self.request),
                                              name=u"absolute_url"))

        for name, factory in getUtilitiesFor(dolmen.IFactory):
            if self.checkFactory(name, factory):
                factory_class = factory.factory
                icon_view = getMultiAdapter((factory_class, self.request),
                                            Interface, 'contenttype_icon')
                
                self.factories.append(dict(
                    name = name,
                    icon = icon_view(),
                    url = '%s/++add++%s' % (self.contexturl, name),
                    title = factory_class.__content_type__,
                    description = (factory.description or
                                   factory_class.__doc__),
                    ))
