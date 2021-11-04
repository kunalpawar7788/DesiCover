
from store.models import *;

class ProductsResource(resources.ModelResource):
     class Meta(object):
     model = Products
     import_id_fields = ('<your key field here>',)