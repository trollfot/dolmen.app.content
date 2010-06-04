# -*- coding: utf-8 -*-

import martian
from dolmen.content import BaseContent
from dolmen.app.content import icon
from grokcore.formlib import formlib
from zope.interface import directlyProvides
from zope.browserresource.metaconfigure import icon as register_icon


class ContentIconGrokker(martian.ClassGrokker):
    martian.component(BaseContent)
    martian.directive(icon)

    def execute(self, class_, config, icon, **kw):
        specialized = formlib.most_specialized_interfaces(class_)
        register_icon(config, 'icon', specialized[0], file=icon)
        directlyProvides(class_, specialized[0])
        return True
