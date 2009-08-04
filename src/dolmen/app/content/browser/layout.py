# -*- coding: utf-8 -*-

import grok
from megrok.menu import menuitem
from dolmen.app.layout import Page 
from dolmen.app.layout.master import DolmenTop
from zope.schema import TextLine
from zope.interface import Interface
from zope.publisher.publish import mapply
from zope.component import getMultiAdapter, getUtility
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.app.publisher.interfaces.browser import IBrowserMenu


class IDynamicLayout(Interface):
    layout = TextLine(
        title = u"Layout",
        default = u"base_view",
        required = True
        )


class DynamicLayoutView(Page):
    grok.name("index")
    grok.context(IDynamicLayout)
    grok.require("dolmen.content.View")

    def render(self):
        rendering = getMultiAdapter((self.context, self.request),
                                    name = self.context.layout)
        rendering.update()
        return rendering.render()


class ApplyLayout(grok.View):
    grok.name('dolmen.layout')
    grok.context(IDynamicLayout)
    grok.require("dolmen.content.Edit")

    def render(self):
        layout = self.request.form.get('layout')
        self.context.layout = layout
        self.flash('layout changed to %r' % layout)
        return self.response.redirect(
            absoluteURL(self.context, self.request)
            )


class DisplayOptions(grok.Viewlet):
    grok.context(IDynamicLayout)
    grok.viewletmanager(DolmenTop)
    grok.require("dolmen.content.Edit")
    grok.order(80)

    def update(self):
        self.contexturl = absoluteURL(self.context, self.request)
        menu = getUtility(IBrowserMenu, 'display')
        self.actions = menu.getMenuItems(self.context, self.request)
        self.selected = self.context.layout
        if (len(self.actions) == 1 and
            self.actions[0]['action'] == self.selected):
            self.actions = None
