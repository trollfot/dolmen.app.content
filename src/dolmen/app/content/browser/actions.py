# -*- coding: utf-8 -*-

import grok
import megrok.menu
import dolmen.content as content

from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory
from zope.traversing.browser import AbsoluteURL

from megrok.z3cform.base import button
from dolmen.app.layout import ContentActions, ApplicationAwareView, Form

_ = MessageFactory("dolmen")


class Delete(Form):
    grok.title(_(u"Delete"))
    megrok.menu.menuitem(ContentActions, order=80)
    grok.context(content.IBaseContent)
    grok.require('dolmen.content.Delete')

    label = _(u"Confirm deletion")
    form_name = _(u"Are you really sure ?")
    fields = {}

    @button.buttonAndHandler(_('Confirm'), name='confirm')
    def handleConfirm(self, action):
        container = self.context.__parent__
        name = self.context.__name__
        if name in container:
            try:
                del container[name]
            except ValueError, e:
                self.redirect(AbsoluteURL(self.context, self.request))

        self.flash("Object %s has been deleted." % name)
        self.redirect(AbsoluteURL(container, self.request))
