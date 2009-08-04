# -*- coding: utf-8 -*-

import grok
from dolmen.blob import BlobFile
from dolmen.content import IBaseContent
from dolmen.imaging import AnnotationThumbnailer


class BlobAnnotationThumbnails(AnnotationThumbnailer):
    grok.context(IBaseContent)
    storage_class = BlobFile
