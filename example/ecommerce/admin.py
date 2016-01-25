from django.contrib import admin

from ecommerce.models import UserProfile
from ecommerce.models import ProdcutDetials
from ecommerce.models import UserProductComments
from ecommerce.models import ProductSpecifications
from ecommerce.models import SpecificationDetails
from ecommerce.models import PricesCountry
from ecommerce.models import PriceSpecification
from ecommerce.models import Ratings

#from gluon.contrib.pyrtf.Elements import Inline
# Register your models here.

@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display=['name','email','mobileNumber']

class PriceSpecification_inline(admin.StackedInline):
    model = PriceSpecification
    extra = 1

class ProductSpecifications_inline(admin.StackedInline):
    model = ProductSpecifications
    extra = 1

@admin.register(ProdcutDetials) 
class ProductDetails(admin.ModelAdmin):
    list_display=["productName","productId", "productDescription", "rating", "thumbUrl", "bigUrl"]
    inlines = [ProductSpecifications_inline,PriceSpecification_inline]
#   write inlines with , separated otherwise overriden
    
@admin.register(UserProductComments)
class UserProductComments(admin.ModelAdmin):
    list_display=["user","product","comments","ratings"]
    
@admin.register(SpecificationDetails)
class SpecificationDetails(admin.ModelAdmin):
    list_display = ["specType","specValue"]

@admin.register(PricesCountry)
class PriceCountry(admin.ModelAdmin):
    list_display = ["price","country"]
    
@admin.register(Ratings)
class Ratings(admin.ModelAdmin):
    list_display = ["user","product","ratings"]