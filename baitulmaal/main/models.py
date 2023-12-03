from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

PHONE_REGEX = RegexValidator(r'^\+?1?\d{9,15}$', "Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")


class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given username, email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        
        user.save(using=self._db)     
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):

    USERNAME_FIELD = 'email'
    username        = None
    email           = models.EmailField(max_length=50, unique=True)
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)
    address         =  models.TextField(blank=True)
    phone           = models.CharField(max_length=15, blank=True,validators=[PHONE_REGEX])
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=True)


    objects = MyUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'All Users'


class Members(models.Model):

    first_name      = models.CharField(max_length=20,blank=False,null=True)
    middle_name     = models.CharField(max_length=20,blank=True,null=True)
    last_name       = models.CharField(max_length=20,blank=False,null=True)
    phone           = models.CharField(max_length=15, blank=True,validators=[PHONE_REGEX])
    balance         = models.IntegerField(default=0)
    is_under_loan   = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'All Members'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Contribution(models.Model):

    member      = models.ForeignKey(Members,on_delete=models.CASCADE,related_name="fk_member_contribution")
    amount      = models.IntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contribution'
        verbose_name_plural = 'All Contribution'

    def __str__(self):
        return self.member.last_name


class Loan(models.Model):

    member      = models.ForeignKey(Members,on_delete=models.CASCADE,related_name="fk_loan_member")
    balance     = models.IntegerField(default=0)
    loan_amount      = models.IntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Loans'
        verbose_name_plural = 'All Loans'

    def __str__(self):
        return self.member.last_name