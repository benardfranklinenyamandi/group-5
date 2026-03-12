from django.contrib import admin
from .models import PasswordReset
from .models import Category, Product, ProductImage

# Register your models here.
admin.site.register(PasswordReset)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    list_display        = ['name', 'category', 'price', 'stock', 'available']
    list_filter         = ['available', 'category']
    list_editable       = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines             = [ProductImageInline]

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)