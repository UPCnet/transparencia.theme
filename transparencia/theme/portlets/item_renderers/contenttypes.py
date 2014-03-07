# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from vilaix.theme.portlets.item_renderers.interfaces import IPortletItemRenderer
from vilaix.theme.portlets.item_renderers.renderer import PortletItemRenderer
from Products.CMFCore.utils import getToolByName

from five.grok import adapter
from five.grok import implementer

from Products.CMFCore.interfaces import IContentish
from DateTime.DateTime import DateTime
from Acquisition import aq_inner

from genweb.core import GenwebMessageFactory as TAM

from transparencia.core.interfaces import IApartat

from zope.i18nmessageid import MessageFactory
PLMF = MessageFactory('plonelocales')


@adapter(IApartat)
@implementer(IPortletItemRenderer)
class TramitPortletItemRenderer(PortletItemRenderer):
    template = ViewPageTemplateFile('apartat.pt')
    css_class = 'apartat clearfix'    

    def getTarget(self):
        obj = self.item.getObject()
        if obj.new_window:
            result = '_blank'
        else:
            result = ''
        return result