from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ecommerce.serializer import *
from ecommerce.admin import ProductDetails
from django.http.response import HttpResponse
# Create your views here.

# function to get all comments of a particular product
def allPrices(productId):
    from ecommerce.models import ProdcutDetials
    pricesList = []
    countryList = []
    
    db = ProdcutDetials.objects.get(pk=productId)
   
    productsSpecifications = db.price.all()
    
    for specs in productsSpecifications:
        pricesList.append(specs.price)
        countryList.append(specs.country)
        
    return pricesList,countryList

def allSpecs(productId):
    from ecommerce.models import ProdcutDetials
    
    specificationList = []
        
    db = ProdcutDetials.objects.get(pk=productId)
       
    productsSpecifications = db.specifications.all()
        
    for specs in productsSpecifications:
        specType = specs.specType
        specValue = specs.specValue
        responseObject = SpecResponseObject(specType=specType,specValue=specValue)
        specificationList.append(responseObject)
        
    return specificationList     
#     specTypeList = []
#     specValueList = []
#     
#     db = ProdcutDetials.objects.get(pk=productId)
#    
#     productsSpecifications = db.specifications.all()
#     
#     for specs in productsSpecifications:
#         specTypeList.append(specs.specType)
#         specValueList.append(specs.specValue)
#     
#     return specTypeList,specValueList

def allComments(productId):
    from ecommerce.models import UserProductComments
    
    commentsList = []
    # accessing a foregin key refrenece field here product has foregin key of another model
    # use double underscorll to get particular field in foreign key model
    result = UserProductComments.objects.filter(product__productId=productId)
    for eachRow in result:
        commentsList.append(eachRow.comments)
    return commentsList

@api_view(['GET'])
def getListOfProducts(request):
    from ecommerce.models import ProdcutDetials
    
    productsList = []
    
    db = ProdcutDetials.objects
    productsData = db.all()
    
    for eachProduct in productsData:
        name = eachProduct.productName
        p_id = eachProduct.productId
        description = eachProduct.productDescription
#         price = eachProduct.price
        priceList,countryList = allPrices(p_id)
        price = 50
        rating = eachProduct.rating
        thumbUrl = eachProduct.thumbUrl
        responseObject = Products_ResponseObject(productName=name,productId=p_id,productDescription=description,price=price,rating=rating,thumbUrl=thumbUrl)
        
#         responseObject = Products_ResponseObject(productName=name,productId=p_id,productDescription=description,rating=rating,thumbUrl=thumbUrl)
        productsList.append(responseObject)
    
    responseSerializer  = Products_ResponseSerializer(productsList,many=True)
    return Response(data = responseSerializer.data,status = status.HTTP_200_OK)

# ------------------second api
@api_view(['POST'])
def getProductFullDetails(request):
    from ecommerce.models import ProdcutDetials
    
    requestSerializer  = Product_RequestSerializer(data=request.data)
    
    if requestSerializer.is_valid():
        requestObject = requestSerializer.save()
        productId = requestObject.productId
        
        productsList = []
    
        db = ProdcutDetials.objects
        eachProduct = db.get(productId=productId)
        
        name = eachProduct.productName
        p_id = eachProduct.productId
        description = eachProduct.productDescription
        price = 40
        rating = eachProduct.rating
        bigUrl = eachProduct.bigUrl
#         specType,specValue = allSpecs(p_id)
        comments = allComments(p_id)
        productSpecs = allSpecs(productId)
        print productSpecs

        responseObject = Product_ResponseObject(comments=comments,productName=name,
                productId=p_id,productDescription=description,price=price,rating=rating,
                bigUrl=bigUrl,
#                 specType=specType,specValue=specValue,
                productSpecifications=productSpecs)
        
        responseSerializer  = Product_ResponseSerializer(responseObject)
        print responseSerializer.data
        return Response(data = responseSerializer.data,status = status.HTTP_200_OK)
    
    else:
        return Response(requestSerializer.error_messages,status=status.HTTP_400_BAD_REQUEST)

# ------------------third api
@api_view(['POST'])
def productComments(request):
    from ecommerce.models import UserProductComments,UserProfile,ProdcutDetials
    
    requestSerializer = ProductComments_RequestSerializer(data=request.data)
    if requestSerializer.is_valid():
        print requestSerializer,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        requestObject = requestSerializer.save()
        productId = requestObject.productId
        userName = requestObject.userName
        comments = requestObject.comments
        
        from django.core.exceptions import ObjectDoesNotExist
        
        try: 
            user = UserProfile.objects.get(name=userName)
        except ObjectDoesNotExist:
            content = {'user Id': 'given user id is not found'}
            return Response(content, status=status.HTTP_417_EXPECTATION_FAILED)
        try:
            product = ProdcutDetials.objects.get(productId=productId)
        except ObjectDoesNotExist:
            content = {'product Id': 'given product id is not found'}
            return Response(content, status=status.HTTP_417_EXPECTATION_FAILED)

        upc = UserProductComments(user=user,product=product,comments=comments)
        upc.save()
        content = {'Comment': 'successfully commented'}
        return Response(data=content,status=status.HTTP_200_OK)

# --------------fourth api to write Ratings
@api_view(['POST'])
def userRatings(request):
    from ecommerce.models import Ratings,UserProfile,ProdcutDetials
    
    requestSerializer = ProductRatings_RequestSerializer(data=request.data)
    
    if requestSerializer.is_valid():
        requestObject = requestSerializer.save()
        productId = requestObject.productId
        userName = requestObject.userName
        rating = requestObject.rating
        
        from django.core.exceptions import ObjectDoesNotExist
        
        try: 
            user = UserProfile.objects.get(name=userName)
        except ObjectDoesNotExist:
            content = {'user Id': 'given user id is not found'}
            return Response(content, status=status.HTTP_417_EXPECTATION_FAILED)
        try:
            product = ProdcutDetials.objects.get(productId=productId)
        except ObjectDoesNotExist:
            content = {'product Id': 'given product id is not found'}
            return Response(content, status=status.HTTP_417_EXPECTATION_FAILED)
        try:
            ratingsObject = Ratings.objects.get(user=user,product=product)
            ratingsObject.ratings = rating
            ratingsObject.save()
            content = {'Ratings': 'successfully updated'}
        except:
            db_insert = Ratings(user=user,product=product,ratings=rating)
            db_insert.save()
            content = {'Ratings': 'successfully added'}
        return Response(data=content,status=status.HTTP_200_OK)

# --------------fifth api to retrive all product specifications
@api_view(['POST'])
def getSpecification(request):
    from ecommerce.models import ProdcutDetials
    requestSerializer  = Product_RequestSerializer(data=request.data)
    
    if requestSerializer.is_valid():
        requestObject = requestSerializer.save()
        productId = requestObject.productId
        
        specificationList = allSpecs(productId)
        
    responseSerializer  = SpecResponseSerializer(specificationList,many=True)
    return Response(data = responseSerializer.data,status = status.HTTP_200_OK)
        
