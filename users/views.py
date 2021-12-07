from django.shortcuts import render
from rest_framework import viewsets,mixins,status
from . import serializer as user_serializer
from rest_framework.decorators import action, api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from utils.custom_exception_classes import CustomError
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, get_user_model

def ReturnUserData(user,get_authToken=False):
    "this return a dictionary of data of the user"
    data = {
    'name':user.name,'email':user.email}
    if get_authToken:
        "basically it means if u want auth token makem get_authToken true "
        token, created = Token.objects.get_or_create(user=user)
        "add authtoken to the response if the user needs it"
        data['authtoken'] =token.key
    "first of all fill the data with the Main Data"



    return data




@api_view(['POST'])
def signup(request):
    "this view handles createing of the User who is a Buyer"
    register_serializer = user_serializer.RegisterViewSerializers(data=request.data)
    
    if register_serializer.is_valid():
        # returns a new user instance so we going to levrage that to send our otp
        new_user = register_serializer.save()
        
        # send_otp(new_user)
        return Response(data={
        'success':True,
        "data":ReturnUserData(new_user),
        'message':"Created Successfully",'status_code':status.HTTP_201_CREATED},status=status.HTTP_201_CREATED)


    raise CustomError(message='Wrong Credentials Please Enter Correct Info',status_code=status.HTTP_400_BAD_REQUEST)

   



class Login(ObtainAuthToken):
    "in this view we accept a post request of data containing OTP Code We will use that to authenticate"
    serializer_class = user_serializer.ObtainUserTokenViewSerializer
    


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        "OTP_CODE is what the user entered"
        if serializer.is_valid():
                
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(username=email,password=password)
            # print(user)
            if user is None:
                "this will throw error only if the user credentials are none"
                raise CustomError(message='Wrong credentials',status_code=status.HTTP_400_BAD_REQUEST)         
            token, created = Token.objects.get_or_create(user=user)
            data = ReturnUserData(user,True)
        # send_otp(new_user)
            return Response(data={
            'success':True,
            "data":data,
            'message':"Login Successfully",'status_code':status.HTTP_201_CREATED},status=status.HTTP_201_CREATED)

        else:
            raise CustomError(message='Wrong Credentials',status_code=status.HTTP_400_BAD_REQUEST)