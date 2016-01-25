from __future__ import unicode_literals

from django.db import models
#from gluon.contrib.pymysql.constants.FLAG import AUTO_INCREMENT
from django.template.defaultfilters import default

# Create your models here.

class UserProfile(models.Model):
    name=models.CharField(max_length=120,default='')
    email = models.CharField(max_length=120,default='')
    mobileNumber = models.IntegerField(default=96428)
    
    def __unicode__(self):
        return unicode(self.name)

class SpecificationDetails(models.Model):
    specType=models.CharField(max_length=200,default='')
    specValue=models.CharField(max_length=200,default='')
    
    def __unicode__(self):
        return unicode(self.specType+":"+self.specValue)
    
class PricesCountry(models.Model):
    price = models.IntegerField()
    country = models.CharField(max_length=200,default='')
    
    def __unicode__(self):
        return unicode(str(self.price)+":"+self.country)
    
class ProdcutDetials(models.Model):
    productName = models.CharField(max_length=120,default='')
    productId=models.AutoField(primary_key=True)
    productDescription=models.CharField(max_length=1200,default='')
    price=models.ManyToManyField(PricesCountry,through="PriceSpecification")
    rating=models.CharField(max_length=120,default='')
    thumbUrl=models.CharField(max_length=240,default='')
    bigUrl=models.CharField(max_length=240,default='')
#     specType=models.CharField(max_length=500,default='')
#     specValue=models.CharField(max_length=1500,default='')
    specifications=models.ManyToManyField(SpecificationDetails,through="ProductSpecifications")

    def __unicode__(self):
        return unicode(str(self.productId)+" : "+self.productName)
    
class UserProductComments(models.Model):
    user = models.ForeignKey(UserProfile)
    product = models.ForeignKey(ProdcutDetials)
    comments=models.CharField(max_length=1900,default='')
    ratings=models.FloatField(default=2.5)

class ProductSpecifications(models.Model):
    spec = models.ForeignKey(SpecificationDetails)
    product = models.ForeignKey(ProdcutDetials)
    
class PriceSpecification(models.Model):
    price = models.ForeignKey(PricesCountry) 
    Product = models.ForeignKey(ProdcutDetials)

class Ratings(models.Model):
    user = models.ForeignKey(UserProfile)
    product = models.ForeignKey(ProdcutDetials)
    ratings=models.FloatField(default=2)
    
    class Meta:
        unique_together = (("user", "product"))