'''
gsconfig is a python library for manipulating a GeoServer instance via the GeoServer RESTConfig API.

The project is distributed under a MIT License .
'''

__author__ = "David Winslow"
__copyright__ = "Copyright 2012-2015 Boundless, Copyright 2010-2012 OpenPlans"
__license__ = "MIT"

from geoserver.support import ResourceInfo, xml_property, write_bool, url
from geoserver.style import Style

class _attribution(object):
    def __init__(self, title, width, height, href, url, type):
        self.title = title
        self.width = width
        self.height = height
        self.href = href
        self.url = url
        self.type = type

def _read_attribution(node):
    title = node.find("title")
    width = node.find("logoWidth")
    height = node.find("logoHeight")
    href = node.find("href")
    url = node.find("logoURL")
    type = node.find("logoType")
    
    if title is not None:
        title = title.text
    if width is not None:
        width = width.text
    if height is not None:
        height = height.text
    if href is not None:
        href = href.text
    if url is not None:
        url = url.text
    if type is not None:
        type = type.text    

    return _attribution(title, width, height, href, url, type)

def _write_attribution(builder, attr):
    builder.start("attribution", dict())
    if attr.title is not None:
        builder.start("title", dict())
        builder.data(attr.title)
        builder.end("title")
    if attr.width is not None:
        builder.start("logoWidth", dict())
        builder.data(attr.width)
        builder.end("logoWidth")
    if attr.height is not None:
        builder.start("logoHeight", dict())
        builder.data(attr.height)
        builder.end("logoHeight")
    if attr.href is not None:
        builder.start("href", dict())
        builder.data(attr.href)
        builder.end("href")
    if attr.url is not None:
        builder.start("logoURL", dict())
        builder.data(attr.url)
        builder.end("logoURL")
    if attr.type is not None:
        builder.start("logoType", dict())
        builder.data(attr.type)
        builder.end("logoType")
    builder.end("attribution")

def _write_style_element(builder, name):
    ws, name = name.split(':') if ':' in name else (None, name)
    builder.start("name", dict())
    builder.data(name)
    builder.end("name")
    if ws:
        builder.start("workspace", dict())
        builder.data(ws)
        builder.end("workspace")

def _write_default_style(builder, name):
    builder.start("defaultStyle", dict())
    if name is not None:
        _write_style_element(builder, name)
    builder.end("defaultStyle")


def _write_alternate_styles(builder, styles):
    builder.start("styles", dict())
    for s in styles:
        builder.start("style", dict())
        _write_style_element(builder, getattr(s, 'fqn', s))
        builder.end("style")
    builder.end("styles")


class Layer(ResourceInfo):
    def __init__(self, catalog, name):
        super(Layer, self).__init__()
        self.catalog = catalog
        self.name = name

    resource_type = "layer"
    save_method = "PUT"

    @property
    def href(self):
        return url(self.catalog.service_url, ["layers", self.name + ".xml"])

    @property
    def resource(self):
        if self.dom is None: 
            self.fetch()
        name = self.dom.find("resource/name").text
        return self.catalog.get_resource(name)

    def _get_default_style(self):
        if 'default_style' in self.dirty:
            return self.dirty['default_style']
        if self.dom is None:
            self.fetch()
        element = self.dom.find("defaultStyle")
        # aborted data uploads can result in no default style
        return self._resolve_style(element) if element is not None else None

    def _resolve_style(self, element):
        # instead of using name or the workspace element (which only appears
        # in >=2.4), just use the atom link href attribute
        atom_link = [ n for n in element.getchildren() if 'href' in n.attrib ]
        if atom_link:
            style_workspace_url = atom_link[0].attrib.get("href")
            return self.catalog.get_style_by_url(style_workspace_url)

    def _set_default_style(self, style):
        if isinstance(style, Style):
            style = style.fqn
        self.dirty["default_style"] = style

    def _get_alternate_styles(self):
        if "alternate_styles" in self.dirty:
            return self.dirty["alternate_styles"]
        if self.dom is None:
            self.fetch()
        styles_list = self.dom.findall("styles/style")
        return filter(None, [ self._resolve_style(s) for s in styles_list ])

    def _set_alternate_styles(self, styles):
        self.dirty["alternate_styles"] = styles

    default_style = property(_get_default_style, _set_default_style)
    styles = property(_get_alternate_styles, _set_alternate_styles)

    attribution_object = xml_property("attribution", _read_attribution)
    enabled = xml_property("enabled", lambda x: x.text == "true")
    advertised = xml_property("advertised", lambda x: x.text == "true", default=True)

    def _get_attr_attribution(self):
        return { 'title': self.attribution_object.title, 
                 'width': self.attribution_object.width, 
                 'height': self.attribution_object.height, 
                 'href': self.attribution_object.href, 
                 'url': self.attribution_object.url, 
                 'type': self.attribution_object.type }
     
    def _set_attr_attribution(self, attribution):
        self.dirty["attribution"] = _attribution( attribution['title'],
                                                  attribution['width'],
                                                  attribution['height'],
                                                  attribution['href'],
                                                  attribution['url'],
                                                  attribution['type'] )
                    
        assert self.attribution_object.title == attribution['title']
        assert self.attribution_object.width == attribution['width']
        assert self.attribution_object.height == attribution['height']
        assert self.attribution_object.href == attribution['href']
        assert self.attribution_object.url == attribution['url']
        assert self.attribution_object.type == attribution['type']

    attribution = property(_get_attr_attribution, _set_attr_attribution)

    writers = dict(
            attribution = _write_attribution,
            enabled = write_bool("enabled"),
            advertised = write_bool("advertised"),
            default_style = _write_default_style,
            alternate_styles = _write_alternate_styles
            )
