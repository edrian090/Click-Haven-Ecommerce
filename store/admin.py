from django.contrib import admin
from .models import Category,Customer, Product, Order, Profile 
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

#Mix profile information with user information in the admin panel
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

#Extend the User model to include the Profile model in the admin panel
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email", "password"]
    inlines = [ProfileInline]

#Unregister the default User model and register the new UserAdmin model
admin.site.unregister(User)

#Register the new User model with the ProfileInline
admin.site.register(User, UserAdmin)

