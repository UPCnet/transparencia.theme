# -*- coding: utf-8 -*-
from zope.interface import Interface

from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('transparencia')

from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from zope.component import getMultiAdapter


class IApartatPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)

    count = schema.Int(title=_(u'Number of apartats to display'),
                       description=_(u'How many apartats to list.'),
                       required=True,
                       default=6)

    state = schema.Tuple(title=_(u"Workflow state"),
                         description=_(u"Items in which workflow state to show."),
                         default=('published', ),
                         required=True,
                         value_type=schema.Choice(
                             vocabulary="plone.app.vocabularies.WorkflowStates")
                         )

    etiqueta = schema.TextLine(
        title=_(u"Etiqueta"),
        description=_(u"Nom de l'etiqueta"),
        required=True,
        default=_(u"principal"),
    )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IApartatPortlet)
    content = None

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self, count=6, state=('published', ), content=None, etiqueta='principal'):
        self.count = count
        self.state = state
        self.content = content
        self.etiqueta = etiqueta

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Apartats")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('templates/apartat.pt')


    def getApartats(self):
        nElements = 3
        apartats =  self._data()
        llistaElementsApartats = []

        if len(apartats) > 0:
            #Retorna una llista amb els apartats en blocs de 3 elements
            llistaElementsApartats=[apartats[i:i+nElements] for i in range(0,len(apartats),nElements)]

        return llistaElementsApartats

    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = self.data.count
        state = self.data.state
        etiqueta = self.data.etiqueta
        portal_state = getMultiAdapter((context, self.request),
            name='plone_portal_state')
        path = portal_state.navigation_root_path()
        return catalog(portal_type='Apartat',
                       review_state=state,
                       Subject=etiqueta,
                       sort_on='getObjPositionInParent',
                       sort_limit=limit)[:limit]

    def getBlocs(self):
        llistaElementsApartats = self.getApartats()
        return len(llistaElementsApartats)

    def test(self, value, trueVal, falseVal):
        """
            helper method, mainly for setting html attributes.
        """
        if value:
            return trueVal
        else:
            return falseVal

    def getAltAndTitle(self, altortitle):
        """Funcio que extreu idioma actiu i afegeix al alt i al title de les imatges del banner
           el literal Obriu l'enllac en una finestra nova
        """
        lt = getToolByName(self, 'portal_languages')
        idioma = lt.getPreferredLanguage()
        str = ''
        if idioma == 'ca':
            str = "(obriu en una finestra nova)"
        if idioma == 'es':
            str = "(abre en ventana nueva)"
        if idioma == 'en':
            str = "(open in new window)"
        if str == '':
            str = "(obriu en una finestra nova)"
        return altortitle + ', ' + str



# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IApartatPortlet)
    label = _(u"Add apartats portlet")
    description = _(u"This portlet displays the site apartats.")
    #form_fields['content'].custom_widget = UberSelectionWidget

    def create(self, data):
        return Assignment(count=data.get('count', 6), state=data.get('state', ('published',)), etiqueta=data.get('etiqueta', 'principal'))


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IApartatPortlet)
    label = _(u"Edit apartats portlet")
    description = _(u"This portlet displays the site apartats.")
    #form_fields['content'].custom_widget = UberSelectionWidget
