from django.contrib import admin
from .models import Category, Product,Department,Course,Profile
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',) }


admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

admin.site.register(Product, ProductAdmin)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','name','dob','user','age','gender','phone','mailid','address','department','purpose', 'created', 'updated']
    list_per_page = 20

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Department)
admin.site.register(Course)
