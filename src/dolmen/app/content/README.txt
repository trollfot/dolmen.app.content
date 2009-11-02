==================
dolmen.app.content
==================

`dolmen.app.content` provides out-of-the-box utilities for Dolmen
applications content.

Getting started
===============

We import Grok and grok the package::

  >>> import grok
  >>> grok.testing.grok('dolmen.app.content')

We create a `dolmen.content` content::

  >>> import dolmen.content
  >>> class Mammoth(dolmen.content.Content):
  ...    grok.name('A furry thing')
  >>> manfred = Mammoth()
  >>> manfred.title = u'A nice mammoth'

Indexes
=======

`dolmen.app.content` registers two indexes to catalog the
`dolmen.content.IBaseContent` created inside a Dolmen application::

  >>> from dolmen.app.content import indexes


Base indexes
------------

The `dolmen.app.content.indexes.BaseIndexes` handles the title and the content type of an IBaseContent content::

  >>> indexes.BaseIndexes.__grok_indexes__
  {'content_type': <grok.index.Field object at ...>, 'title': <grok.index.Text object at ...>}

  >>> indexes.BaseIndexes.__grok_indexes__['content_type']._attribute
  '__content_type__'


Searchable text
---------------

`dolmen.app.content` provides a simple 'ISearchableText'
implementation, allowing full text searches. It comes in two parts::

The index::

  >>> indexes.SearchableIndex.__grok_indexes__
  {'searchabletext': <grok.index.Text object at ...>}

The adapter::

  >>> from zope.index.text.interfaces import ISearchableText
  >>> adapter = ISearchableText(manfred)
  >>> adapter.getSearchableText()
  u'A nice mammoth'


Thumbnailing
============

Thanks to `dolmen.thumbnailer`, `dolmen.app.content` provides a base
thumbnailing policy, using ZODB blobs as storage and introducing a new
scale.

Scales
------

Let's introspect our Miniaturized component::

  >>> from dolmen.app.content import thumbnails

  >>> thumbnails.BlobMiniaturizer.factory
  <class 'dolmen.blob.file.BlobFile'>

  >>> print thumbnails.BlobMiniaturizer.scales
  {'mini': (250, 250), 'square': (80, 80), 'thumb': (150, 150), 'large': (700, 700), 'small': (128, 128), 'preview': (400, 400)}

The new scale, 'square', scales down and crops the original image to
provide a square thumbnail. This is down using a IThumbnailer adapter.

  >>> from dolmen.thumbnailer import IThumbnailer	
  >>> thumbnails.SquareThumbnailer
  <class 'dolmen.app.content.thumbnails.SquareThumbnailer'>
  >>> IThumbnailer.implementedBy(thumbnails.SquareThumbnailer)
  True
