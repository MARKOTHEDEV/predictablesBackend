from rest_framework import serializers
from django.contrib.auth import get_user_model
from utils.custom_exception_classes import CustomError
from rest_framework import status



class RegisterViewSerializers(serializers.ModelSerializer):
    
    """
    {
        name:'',
        "password":'',
        'email':'',
    }
    """
    def create(self, validated_data):
        name = validated_data.get('name',None)
        email = validated_data.get('email',None)
        password = validated_data.get('password',None)
        
        if name =='' or name  is None:
            raise CustomError(message='Name Is Required!',status_code=status.HTTP_400_BAD_REQUEST)
        if password =='' or password  is None:
            raise CustomError(message='Password Is Required!',status_code=status.HTTP_400_BAD_REQUEST)
        
        if email== '' or email is None:
            raise CustomError(message='Email Is Required!',status_code=status.HTTP_400_BAD_REQUEST)

        if get_user_model().objects.filter(email=email).exists():
            raise CustomError(message='This email Exists',status_code=status.HTTP_400_BAD_REQUEST)
        
        user =  get_user_model().objects.create_user(name=name,email=email,password=password)
        user.save()

        return user

    


    class Meta:
        model =get_user_model()
        fields = ['name','email','password']
        """
            Note the extra_kwargs i removed the validator and said the allow_blank to be true you may ask why is that
        the answer is django rest has a custom validator that retuns a custom response which i dont want so that why i wrote my own
        validations and raised my own error in the create method above...
        """
        extra_kwargs = {
            # the name and phone_number field i disable all the defualt exception so i could write my own
                'name': {'validators': [],'required':False,'allow_blank':True},
                'email': {'validators': [],'required':False,'allow_blank':True}, 
                'password': {'validators': [],'required':False,'allow_blank':True},
                } 








class ObtainUserTokenViewSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=True,validators=[])
    password = serializers.CharField(allow_blank=True,validators=[])



    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')


        if password == "":
            "it the person sends an empty token"
            raise CustomError(message='Enter a password',status_code=status.HTTP_400_BAD_REQUEST)

        if email == "":
            "If the Person sends a Empty String"
            raise CustomError(message='Enter Email',status_code=status.HTTP_400_BAD_REQUEST)



        if not get_user_model().objects.filter(email=email).exists():
            "If the Person Enters a number that Doest Exists "
            raise CustomError(message='Email does not exits!',status_code=status.HTTP_400_BAD_REQUEST)
        else:
            "this means the user exits so Now We check For his password"
            user = get_user_model().objects.get(email=email)
            if not user.check_password(password):
                "so if it not true Raise Error"
                raise CustomError(message='Wrong Password',status_code=status.HTTP_400_BAD_REQUEST)

        return attrs