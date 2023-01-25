from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', )


admin.site.register(Contact, ContactAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
