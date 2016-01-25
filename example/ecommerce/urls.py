
from django.conf.urls import url
# import our created api getinterndata
from ecommerce.views import getListOfProducts,getProductFullDetails,productComments,userRatings,getSpecification

urlpatterns = [
       url(r'^getListOfProducts/$',getListOfProducts),
       url(r'^getProductFullDetails/$',getProductFullDetails),
       url(r'^productComments/$',productComments),
       url(r'^userRatings/$',userRatings),
       url(r'^getSpecification/$',getSpecification)
]
