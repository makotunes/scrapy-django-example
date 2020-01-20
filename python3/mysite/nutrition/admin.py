from django.contrib import admin

from nutrition.models import Item, Composition, Nutrition

class ItemAdmin(admin.ModelAdmin):
    list_display_links = ('id',
                          'product_name',
                          'product_url',
                          'company',
                          'amount',
                          'capsule_type',
                          'rating_count',
                          'rating',
                          'price',
                          'product_code',
                          'serving_size',
                          'get_name_cid',
                          'create_date_time',
                         )
    list_display =       ('id',
                          'product_name',
                          'product_url',
                          'company',
                          'amount',
                          'capsule_type',
                          'rating_count',
                          'rating',
                          'price',
                          'product_code',
                          'serving_size',
                          'get_name_cid',
                          'create_date_time',
                         )
    search_field =       ('id',
                          'product_name',
                          'product_url',
                          'company',
                          'amount',
                          'capsule_type',
                          'rating_count',
                          'rating',
                          'price',
                          'product_code',
                          'serving_size',
                          'get_name_cid',
                          'create_date_time',
                         )
    def get_name_cid(self, obj):
        return obj.composition
    get_name_cid.admin_order_field  = 'Composition'
    get_name_cid.short_description = 'Composition Name'
admin.site.register(Item, ItemAdmin)

class CompositionAdmin(admin.ModelAdmin):
    list_display_links = ('id',
                          'get_name_nid',
                          'amount',
                          'unit',
                          'create_date_time',
                         )
    list_display =       ('id',
                          'get_name_nid',
                          'amount',
                          'unit',
                          'create_date_time',
                         )
    search_field =       ('id',
                          'get_name_nid',
                          'amount',
                          'unit',
                          'create_date_time',
                         )
    def get_name_nid(self, obj):
        return obj.name
    get_name_nid.admin_order_field  = 'Nutrition'
    get_name_nid.short_description = 'Nutrition Name'
admin.site.register(Composition, CompositionAdmin)

class NutritionAdmin(admin.ModelAdmin):
    list_display_links = ('id',
                          'name',
                          'create_date_time',
                         )
    list_display =       ('id',
                          'name',
                          'create_date_time',
                         )
    search_field =       ('id',
                          'name',
                          'create_date_time',
                         )
admin.site.register(Nutrition, NutritionAdmin)
