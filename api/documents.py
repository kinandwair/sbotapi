# document.py

from django_elasticsearch_dsl import DocType, Index
from .models import Property

# Name of the Elasticsearch index
property_listing = Index('property_sale')
# See Elasticsearch Indices API reference for available settings
property_listing.settings(
    number_of_shards=1,
    number_of_replicas=0,

)


@property_listing.doc_type
class PropertyDocument(DocType):
    class Meta:
        model = Property  # The model associated with this DocType
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'ad_title',
            'city',
            'area',
            'price',
            'posting_date',
            'action',
            'ad_images',
            'ad_link',
            'add_link',
            'didExceptionHappenDuringExtractingItems',
            'bedrooms',
            'amenities',
            'bathrooms',
            'building',
            'category',
            'country',
            "size",
            "creating_date_time",
            # "coordinates",
            "source",
            "trade_name",
            "type",
            "description",
            "master_property_type",
            "phone",
            "ded_license_number",
            "creating_date",
            'furnished',
            "master_furnished",
            "rera_registration_number",
            "subarea",
            "master_payment_type",
            "property_reference",
            "payment_type",
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000
