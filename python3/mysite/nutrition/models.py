from django.db import models

class Nutrition(models.Model):
    id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Name', max_length=255, blank=True, null=True)
    description = models.TextField('Description', blank=True, null=True)
    create_date_time = models.DateTimeField('Date', auto_now=True)

    def __str__(self):
        return str(self.name)

class Composition(models.Model):
    id = models.AutoField('ID', primary_key=True)
    name = models.ForeignKey('Nutrition', related_name='composition_nutrition_id')
    amount = models.IntegerField('Amount', default=0, blank=False, null=False)
    unit = models.CharField('Unit', max_length=20,blank=True, null=True)
    create_date_time = models.DateTimeField('Date', auto_now=True)

    def __str__(self):
        return str(self.name) + ':' + str(self.amount) + ' ' + str(self.unit)

class Item(models.Model):
    id = models.AutoField('ID', primary_key=True)

    product_name = models.CharField('Name', max_length=100,blank=True, null=True)
    product_url = models.CharField('Product URL', max_length=999,blank=True, null=True)
    company = models.CharField('Company', max_length=100,blank=True, null=True)
    amount = models.IntegerField('Amount', default=0, blank=False, null=True)
    capsule_type = models.CharField('Capsule Type', max_length=20,blank=True, null=True)
    rating_count = models.IntegerField('Rating Count', default=0, blank=False, null=False)
    rating = models.DecimalField('Rating', max_digits=32, decimal_places=16, default=0.0)
    price = models.IntegerField('Price', default=0, blank=False, null=True)
    product_code = models.CharField('Product Code', max_length=100,blank=True, null=True)
    serving_size = models.IntegerField('Serving Size', default=1, blank=False, null=True)
    composition = models.ManyToManyField(Composition)
    create_date_time =  models.DateTimeField('Date', auto_now=True)
    
    def __str__(self):
        return str(self.product_name)


