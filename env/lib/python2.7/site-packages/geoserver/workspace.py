'''
gsconfig is a python library for manipulating a GeoServer instance via the GeoServer RESTConfig API.

The project is distributed under a MIT License .
'''

__author__ = "David Winslow"
__copyright__ = "Copyright 2012-2015 Boundless, Copyright 2010-2012 OpenPlans"
__license__ = "MIT"

from geoserver.support import xml_property, write_bool, ResourceInfo, url

def workspace_from_index(catalog, node):
    name = node.find("name")
    return Workspace(catalog, name.text)

class Workspace(ResourceInfo): 
    resource_type = "workspace"

    def __init__(self, catalog, name):
        super(Workspace, self).__init__()
        self.catalog = catalog
        self.name = name

    @property
    def href(self):
        return url(self.catalog.service_url, ["workspaces", self.name + ".xml"])

    @property
    def coveragestore_url(self):
        return url(self.catalog.service_url, ["workspaces", self.name, "coveragestores.xml"])

    @property
    def datastore_url(self):
        return url(self.catalog.service_url, ["workspaces", self.name, "datastores.xml"])

    @property
    def wmsstore_url(self):
        return "%s/workspaces/%s/wmsstores.xml" % (self.catalog.service_url, self.name)

    enabled = xml_property("enabled", lambda x: x.lower() == 'true')
    writers = dict(
        enabled = write_bool("enabled")
    )

    def __repr__(self):
        return "%s @ %s" % (self.name, self.href)
