import grok
from grok import index
from dolmen.app.site import IDolmen
from dolmen.content import IBaseContent
from zope.component import getUtility, getSiteManager
from zope.app.intid.interfaces import IIntIds
from zope.index.text.interfaces import ISearchableText


class BaseObjectIndexes(grok.Indexes):
    grok.site(IDolmen)
    grok.context(IBaseContent)
    
    title = index.Text()


class SearchableIndexes(grok.Indexes):
    grok.site(IDolmen)
    grok.context(ISearchableText)
    
    searchabletext = index.Text(attribute="getSearchableText")


class BaseSearchable(grok.Adapter):
    grok.implements(ISearchableText)
    grok.context(IBaseContent)

    def getSearchableText(self):
         return self.context.title
