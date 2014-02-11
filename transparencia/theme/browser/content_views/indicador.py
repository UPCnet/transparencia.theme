# -*- coding: utf-8 -*-
from five import grok
from plone.memoize.view import memoize_contextless
from zope.component.hooks import getSite
from transparencia.core.interfaces import IIndicador
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize

from plone.app.contenttypes.interfaces import IFile
from plone.app.contenttypes.browser.utils import IUtils

from Acquisition import aq_inner, aq_base, aq_parent

class View(grok.View):
    grok.context(IIndicador)
    grok.require('zope2.View')

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()

    # def getImage(self):
    #     catalog = getToolByName(self.context, 'portal_catalog')
    #     utool = getToolByName(self.context, 'portal_url')
        
    #     url = self.request.getURL()

    #     if self.context.image:           
    #         url_imatge = '%s/++widget++form.widgets.image/@@download/%s' % (url.replace("view", "@@edit"), self.context.image.filename)
    #     else:
    #         url_imatge = ''
      
    #     return url_imatge
    
    # def getFitxer(self):
    #     catalog = getToolByName(self.context, 'portal_catalog')
    #     utool = getToolByName(self.context, 'portal_url')

    #     url = self.request.getURL()
        
    #     if self.context.fitxer_inici:           
    #         url_fitxer = '%s/++widget++form.widgets.fitxer_inici/@@download/%s' % (url.replace("view", "@@edit"), self.context.fitxer_inici.filename)
    #     else:
    #         url_fitxer = ''
      
    #     return url_fitxer

    def getLleisRelacionades(self):
        catalog = getToolByName(self.context, 'portal_catalog')       
        dades = []

        lleis = self.context.keywords_llei

        for a in lleis:
            llei = catalog.searchResults(
                    id = a,
                    portal_type='Llei',
                    review_state = 'published')  
            for i in llei: 
                dades.append(dict(titol=i.getObject().title,
                                  text_llei=i.getObject().text_llei.raw,
                                  enllac_BOE=i.getObject().enllac_BOE
                                 )
                            )          
             
        return dades

    def getEnllacosRelacionats(self):
        catalog = getToolByName(self.context, 'portal_catalog')     
    
        path = '/'.join(self.context.getPhysicalPath())               

        enllacosRelacionats = catalog.searchResults(portal_type='Link',
                                                    review_state = 'published',
                                                    path=path)
        dades = [dict(id=a.id,  
                     url=a.getObject().remoteUrl,                     
                     title=a.getObject().title_or_id()
                     ) for a in enllacosRelacionats] 
        return dades

    def getFitxersRelacionats(self):
        catalog = getToolByName(self.context, 'portal_catalog')     
    
        path = '/'.join(self.context.getPhysicalPath())               

        fitxersRelacionats = catalog.searchResults(portal_type='File',                                                   
                                                   path=path)
        dades = []

        for a in fitxersRelacionats:
            obj = a.getObject()

            dades.append(dict(id=obj.id,  
                              descripcio=obj.Description,                     
                              title=obj.title_or_id(),                    
                              absolute_url=self.context.absolute_url() + '/' + obj.id,
                              filename=obj.file.filename,
                              size=obj.file.getSize(),
                              data=str(obj.creation_date.day()) + '/' + str(obj.creation_date.month()) + '/' + str(obj.creation_date.year()),
                              tipus=obj.file.contentType.replace('application/', '')
                             )
                        )
        return dades

    def getTornar(self):
        parent = aq_parent(self.context)  
        return parent.absolute_url()

