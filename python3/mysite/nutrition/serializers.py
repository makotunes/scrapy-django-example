from rest_framework import serializers
from nutrition.models import *
from django.contrib.auth.models import User

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id',
                  'product_name',
                  'product_url',
                  'company',
                  'capsule_type',
                  'rating_count',
                  'rating',
                  'price',
                  'product_code',
                  'serving_size',
                  'composition',
                 )
