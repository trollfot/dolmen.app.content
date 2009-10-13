#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok
from grok import index
from dolmen.app.site import IDolmen
from dolmen.content import IBaseContent
from zope.index.text.interfaces import ISearchableText


class BaseIndexes(grok.Indexes):
    grok.site(IDolmen)
    grok.context(IBaseContent)
    
    title = index.Text()
    content_type = index.Field(attribute='__content_type__')


class SearchableIndex(grok.Indexes):
    grok.site(IDolmen)
    grok.context(ISearchableText)
    
    searchabletext = index.Text(attribute="getSearchableText")


class BaseSearchable(grok.Adapter):
    grok.implements(ISearchableText)
    grok.context(IBaseContent)

    def getSearchableText(self):
        return self.context.title
