from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .forms import CategoryForm

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(GalleryProduct)
# admin.site.register(Brand)
admin.site.register(Profile)
admin.site.register(FavoriteProduct)

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(Region)
admin.site.register(City)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'parent', 'get_icon_category')
    prepopulated_fields = {'slug': ('title',)}
    form = CategoryForm
    list_display_links = ('pk', 'title')

    def get_icon_category(self, obj):
        if obj.icon:
            try:
                return mark_safe(f'<img src="{obj.icon.url}" width=25>')
            except:
                return '-'
        else:
            return '-'

    get_icon_category.short_description = 'Иконка'


class GalleryInline(admin.TabularInline):
    model = GalleryProduct
    fk_name = 'product'
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'quantity', 'category', 'brand', 'get_photo')
    list_display_links = ('pk', 'title')
    inlines = [GalleryInline]
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'quantity', 'category', 'brand')
    list_filter = ('price', 'quantity', 'category', 'brand')

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.first().image.url}" width=50>')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Фото'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
