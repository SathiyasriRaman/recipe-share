from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Show these columns in admin list
    search_fields = ('title', 'ingredients')  # Add search bar
    list_filter = ('created_at',)  # Add filtering
