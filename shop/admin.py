from django.contrib import admin

from .models import Item, CartItem, Cart, SubCategory, Category


class ItemAdmin(admin.TabularInline):
    fields = ['title', 'description', 'price', 'sub_category', 'slug']
    model = Item
    prepopulated_fields = {'slug': ('title',)}
    extra = 1
    list_display = ('title', 'price', 'sub_category')  
    list_filter = ['sub_category', 'price', 'title']
    search_fields = ['sub_category', 'price', 'title']


class SubCategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'category']
    model = SubCategory
    prepopulated_fields = {'slug': ('title',)}
    extra = 1 
    inlines = [ItemAdmin]
    list_display = ('title', 'category')
    list_filter = ['category', 'title']
    search_fields = ['category', 'title']


class SubCategoryInline(admin.TabularInline):
    fields = ['title', 'slug', 'category']
    model = SubCategory
    prepopulated_fields = {'slug': ('title',)}
    extra = 1 
    inlines = [ItemAdmin]
    list_display = ('title', 'category')
    list_filter = ['category', 'title']
    search_fields = ['category', 'title']


class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'slug']
    model = Category
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)
    list_filter = ['title']
    search_fields = ['title']
    inlines = [SubCategoryInline]


admin.site.register(Item)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
# admin.site.register(Item)
# admin.site.register(SubCategory)
# admin.site.register(Category)


