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

from plone.directives import form
from z3c.form import button
from plone.dexterity.i18n import MessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.app.container.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class View(grok.View):
    grok.context(IIndicador)
    grok.require('zope2.View')

    index = ViewPageTemplateFile("indicador_templates/indicadorview.pt")

    def render(self):
        # defer to index method, because that's what gets overridden by the template ZCML attribute
        return self.index()

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()

    def getLleisRelacionades(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        dades = []

        lleis = self.context.keywords_llei

        for a in lleis:
            llei = catalog.searchResults(
                    id = a,
                    portal_type='Llei',
                    review_state = 'published',
                    sort_on='sortable_title',
                    sort_order='ascending')
            for i in llei:
                dades.append(dict(titol=i.getObject().title,
                                  text_llei=i.getObject().text_llei.raw,
                                  enllac_BOE=i.getObject().enllac_BOE,
                                  url_llei=i.getObject().absolute_url()
                                 )
                            )

        return dades

    def getEnllacosRelacionats(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        path = '/'.join(self.context.getPhysicalPath())

        enllacosRelacionats = catalog.searchResults(portal_type='Link',
                                                    review_state = 'published',
                                                    path=path,
                                                    sort_on='sortable_title',
                                                    sort_order='ascending')
        dades = [dict(id=a.id,
                     url=a.getObject().remoteUrl,
                     title=a.getObject().title_or_id()
                     ) for a in enllacosRelacionats]
        return dades

    def getFitxersRelacionats(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        path = '/'.join(self.context.getPhysicalPath())

        fitxersRelacionats = catalog.searchResults(portal_type='File',
                                                   path=path,
                                                   sort_on='sortable_title',
                                                   sort_order='ascending')
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

    # def getTornar(self):
    #     parent = aq_parent(self.context)
    #     return parent.absolute_url()


    def getAgregat(self):
        context = self.context
        valor = context.resultat_agregat
        result = []
        clase = ''

        if valor >= 0 and valor <=2:
          clase = 'fa fa-thumbs-o-down'
        elif valor > 2 and valor <=4:
          clase = 'fa fa-thumbs-o-down'
        elif valor > 4 and valor <=6:
          clase = 'fa fa-eye'
        elif valor > 6 and valor <=8:
          clase = 'fa fa-thumbs-o-up'
        elif valor > 8 and valor <=10:
          clase = 'fa fa-exclamation'

        result.append(dict(valor=valor,
                           clase=clase)
                     )
        return result

@grok.subscribe(IIndicador, IObjectAddedEvent)
def add_indicador(indicador, event):
  ponderat_publicat = (indicador.valoracio_publicat * 80) / 100
  ponderat_comprensio = (indicador.valoracio_comprensio * 20) / 100
  resultat_agregat = ponderat_publicat + ponderat_comprensio
  indicador.resultat_agregat = resultat_agregat
  indicador.reindexObject()

@grok.subscribe(IIndicador, IObjectModifiedEvent)
def edit_indicador(indicador, event):
  ponderat_publicat = (indicador.valoracio_publicat * 80) / 100
  ponderat_comprensio = (indicador.valoracio_comprensio * 20) / 100
  resultat_agregat = ponderat_publicat + ponderat_comprensio
  indicador.resultat_agregat = resultat_agregat
  indicador.reindexObject()
