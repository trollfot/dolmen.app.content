# -*- coding: utf-8 -*-

import grok
import zope.dublincore.interfaces as dc
from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory

import dolmen.forms.crud as crud
from dolmen.forms.composed import ComposedForm
from dolmen.content import IContainer, IContent
from dolmen.app.layout import models
from dolmen.app.layout import ContentActions, menuitem, ISortable

from z3c.form import field
from megrok.z3ctable import NameColumn, LinkColumn, ModifiedColumn

_ = MessageFactory("dolmen")


class Metadata(ComposedForm, models.TabView):
    grok.name('metadata')
    grok.title(_(u"Metadata"))
    grok.context(IContent)
    grok.require('dolmen.content.Edit')

    label = 'Metadata Editing'
    form_name = 'Edit the general dublincore metadata'


class DescriptionMetadata(models.SubForm, crud.Edit):
    grok.view(Metadata)
    grok.context(IContent)
    grok.name('metadata.description')
    grok.order(10)

    label = "Content description"
    form_name = "Content description"
    fields = field.Fields(dc.IDCDescriptiveProperties)
    

class PublishingMetadata(models.SubForm, crud.Edit):
    grok.view(Metadata)
    grok.context(IContent)
    grok.name('metadata.publishing')
    grok.order(20)

    label = "Publishing informations"
    form_name = "Publishing informations"
    fields = field.Fields(dc.IDCPublishing)


class ExtendedMetadata(models.SubForm, crud.Edit):
    grok.view(Metadata)
    grok.context(IContent)
    grok.name('metadata.extended')
    grok.order(30)

    label = "Extended metadata"
    form_name = "Extended metadata"
    fields = field.Fields(dc.IDCExtended)


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
