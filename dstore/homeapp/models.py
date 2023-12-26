from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description =models.TextField(blank=True)
    image = models.ImageField(upload_to='category',blank=True)

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('homeapp:Products_of_Category',kwargs={"c_slug": self.slug})

    def __str__(self):
        return  '{}'.format(self.name)

class Product(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description =models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product',blank=True)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('homeapp:get_product_details', kwargs={"c_slug": self.category.slug,"p_slug":self.slug})

    def __str__(self):
        return '{}'.format(self.name)

class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Profile(models.Model):

    Purpose = (
        ('enquiry', "Enquiry"),
        ('placeorder', "Place order"),
        ('return', "Return")
    )

    name=models.CharField(max_length=100)
    dob=models.DateField(auto_now_add=False,auto_now=False)
    age=models.PositiveIntegerField(default=False,
        validators=[MaxValueValidator(60), MinValueValidator(10)])
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Gender = (('Male', 'Male'), ('Female', 'Female'))
    gender = models.CharField(max_length=100, choices=Gender, blank=False, default=None)
    phone = models.PositiveBigIntegerField()
    mailid = models.EmailField(max_length=100)
    address = models.CharField(max_length=500)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    purpose = models.CharField(max_length=100,choices=Purpose)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'


    def __str__(self):
        return '{}'.format(self.name)