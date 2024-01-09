from django.contrib import admin
from .models import Post, Category, Tag, Like

admin.site.register(Post)  

admin.site.register(Like)  

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Tag, TagAdmin)