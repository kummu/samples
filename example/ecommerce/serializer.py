from rest_framework import serializers
from debian.changelog import comments


# -------------------fifth api
class SpecResponseObject(object):
    def __init__(self,specType,specValue):
        self.specType=specType
        self.specValue=specValue

class SpecResponseSerializer(serializers.Serializer):
    specType = serializers.CharField()
    specValue = serializers.CharField()
    
    def create(self, validated_data):
        return SpecResponseObject(**validated_data)

# ----------------------first api
class Products_ResponseObject(object):
    def __init__(self,productName,productId, productDescription, price, rating, thumbUrl):
#     def __init__(self,productName,productId, productDescription,  rating, thumbUrl):
        self.productName = productName
        self.productId = productId
        self.productDescription = productDescription
        self.price = price
        self.rating=rating
        self.thumbUrl = thumbUrl

class Products_ResponseSerializer(serializers.Serializer):
    productName = serializers.CharField()
    productId = serializers.IntegerField()
    productDescription = serializers.CharField()
    price = serializers.IntegerField()
    rating = serializers.FloatField()
    thumbUrl = serializers.URLField()
    

    def create(self,validated_data):
        return Products_ResponseObject(**validated_data)
        
# --------------------second api
class Product_RequestObject(object):
    def __init__(self,productId):
        self.productId=productId

class Product_RequestSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    
    def create(self,validated_data):
        return Product_RequestObject(**validated_data)
    
class Product_ResponseObject(object):
    def __init__(self,comments,productName,productId, productDescription, price, rating, bigUrl,productSpecifications):
        self.productName = productName
        self.productId = productId
        self.productDescription = productDescription
        self.price = price
        self.rating=rating
        self.bigUrl = bigUrl
        self.comments=comments
#         self.specType=specType
#         self.specValue=specValue
        self.productSpecifications = productSpecifications
       

class Product_ResponseSerializer(serializers.Serializer):
    productName = serializers.CharField()
    productId = serializers.IntegerField()
    productDescription = serializers.CharField()
    price = serializers.IntegerField()
    rating = serializers.FloatField()
    bigUrl = serializers.URLField()
    comments = serializers.ListField(child = serializers.CharField())
#     specType = serializers.ListField(child = serializers.CharField())
#     specValue = serializers.ListField(child = serializers.CharField())
    productSpecifications = SpecResponseSerializer(many=True)
    
    def create(self,validated_data):
        specsList = validated_data.pop('productSpecifications')
        psList = []
        print specsList
        for eachSpec in specsList:
            psObject = SpecResponseObject(**eachSpec)
            psList.append(psObject)
        return Product_ResponseObject(productSpecifications=psList,**validated_data)   

# -------------------------third api
class ProductComments_RequestObject(object):
    def __init__(self,productId,userName,comments):
        self.productId=productId
        self.userName = userName
        self.comments=comments

class ProductComments_RequestSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    userName = serializers.CharField()
    comments=serializers.CharField()
    
    def create(self,validated_data):
        return ProductComments_RequestObject(**validated_data)

# -------------------fourth api
class ProductRatings_RequestObject(object):
    def __init__(self,productId,userName,rating):
        self.productId=productId
        self.userName = userName
        self.rating=rating

class ProductRatings_RequestSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    userName = serializers.CharField()
    rating=serializers.FloatField()
    
    def create(self,validated_data):
        return ProductRatings_RequestObject(**validated_data)
    
