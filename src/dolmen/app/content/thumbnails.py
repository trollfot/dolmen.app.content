# -*- coding: utf-8 -*-

import grokcore.component as grok

from PIL import Image
from cStringIO import StringIO
from dolmen.blob import BlobFile
from dolmen.content import IBaseContent
from dolmen.thumbnailer import Miniaturizer, IThumbnailer


class BlobMiniaturizer(Miniaturizer):
    """A thumbnailer made for the Dolmen CMS.
    It adds a 64*64 scale and it stores the thumbnails in blobs.
    """
    grok.context(IBaseContent)

    # We store in blob
    factory = BlobFile

    # We add a new size
    scales = {'large'  : (700, 700),
              'preview': (400, 400),
              'mini'   : (250, 250),
              'thumb'  : (150, 150),
              'small'  : (128, 128),
              'square' : ( 64,  64),
              }


class SquareThumbnailer(grok.Adapter):
    """A named thumbnailer that will crop images to the given size.
    """
    grok.name('square')
    grok.context(IBaseContent)
    grok.implements(IThumbnailer)
    
    def scale(self, original, size):
        image = original.copy()

        width, height = image.size

        if width > height:
            delta = width - height
            left = int(delta/2)
            upper = 0
            right = height + left
            lower = height
        else:
            delta = height - width
            left = 0
            upper = int(delta/2)
            right = width
            lower = width + upper

        image = image.crop((left, upper, right, lower))
        image.thumbnail(size, Image.ANTIALIAS)
        thumbnailIO = StringIO()
        image.save(thumbnailIO, original.format, quality=90)
        thumbnailIO.seek(0)        
        return thumbnailIO
