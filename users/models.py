from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager



class CustomUserManager(BaseUserManager):


    def create_user(self,name,email=None,password=None):
        'create user helps create our custom user and returns it'

        user = self.model(name=name,email=email)
        "the code below is just filling the data passed to the model Colomn"
        "if u dont know set password helps to set/hash the password"
        user.set_password(password)
        user.save()
    # else:
        return user

    def create_superuser(self,name,email=None,password=None):
        "self.create_user will create a user and returns it"
        if password is None:
            raise ValueError('Password is Requeird')
        # print(password)
        user = self.create_user(name,email=email,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active=True
        user.save()

        return user






class CustomUser(PermissionsMixin,AbstractBaseUser):
    "this is the Custom User Django Will Work With"
    name   = models.CharField(max_length=300)
    email   = models.EmailField(blank=True,null=True,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_live = models.BooleanField(default=True,blank=True)


    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    "check the  CustomUserManager() th code is above"
    objects = CustomUserManager()


    def __str__(self):
        return f'{self.name} '