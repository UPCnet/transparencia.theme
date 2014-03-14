# -*- coding: utf-8 -*-
from five import grok
from plone.memoize.view import memoize_contextless
from zope.component.hooks import getSite
from transparencia.core.interfaces import ILlei
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


class View(grok.View):
    grok.context(ILlei)
    grok.require('zope2.View')

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()