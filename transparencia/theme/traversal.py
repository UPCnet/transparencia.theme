from plone.resource.traversal import ResourceTraverser


class TransparenciaThemeTraverser(ResourceTraverser):
    """The transparencia theme traverser.

    Allows traversal to /++TransparenciaTheme++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """

    name = 'transparencia'
