# -*- coding: utf-8 -*-

import grokcore.view as grok
from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory

from dolmen.content import IContainer
from dolmen.app.layout import models
from dolmen.app.layout import ContentActions, menuitem, ISortable
from megrok.z3ctable import NameColumn, LinkColumn, ModifiedColumn

_ = MessageFactory("dolmen")


class FolderListing(models.TablePage):
    grok.name('base_view')
    grok.title(_(u"Content"))
    grok.context(IContainer)
    grok.require('dolmen.content.List')
    grok.implements(ISortable)
    menuitem(ContentActions, order=10)

    batchSize = 20
    startBatchingAt = 20
    cssClasses = {'table': 'listing'}
    cssClassEven = u'even'
    cssClassOdd = u'odd'
    sortOn = None
    
    @property
    def values(self):
        return self.context.values()

    
    def render(self):
        return self.renderTable()


class Title(LinkColumn):
    """Display the name of the content item
    """
    grok.name('folderlisting.title')
    grok.adapts(None, None, FolderListing)
    header = _(u"Title")

    def renderCell(self, item):
        icon = getMultiAdapter((item, self.table.request),
                               name = "contenttype_icon")
        return "%s&nbsp;%s" % (icon(),
                               LinkColumn.renderCell(self, item))
        

class ModificationDate(ModifiedColumn):
    """Display the name of the content item
    """
    grok.name('folderlisting.modified')
    grok.adapts(None, None, FolderListing)
    weight = 1
    header = _(u"Modified")
