from zope.configuration import xmlconfig

from plone.testing.z2 import ZSERVER_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class TransparenciaTheme(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import genweb.theme
        import transparencia.theme
        import genweb.core
        xmlconfig.file('configure.zcml',
                       genweb.theme,
                       context=configurationContext)

        xmlconfig.file('configure.zcml',
                       transparencia.theme,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'genweb.theme:default')
        applyProfile(portal, 'genweb.controlpanel:default')
        applyProfile(portal, 'transparencia.theme:default')


TransparenciaTheme_FIXTURE = TransparenciaTheme()
TransparenciaTheme_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TransparenciaTheme_FIXTURE,),
    name="TransparenciaTheme:Integration")
TransparenciaTheme_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TransparenciaTheme_FIXTURE,),
    name="TransparenciaTheme:Functional")
TransparenciaTheme_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(TransparenciaTheme_FIXTURE, ZSERVER_FIXTURE),
    name="TransparenciaTheme:Acceptance")
