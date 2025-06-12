from django.urls import path
from . import views            # Your HTML (template-based) views
from . import api_views        # Your DRF API views

urlpatterns = [
    # --- Template-based Views ---
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),  # or use LogoutView if preferred
    path('recipes/', views.recipe_list, name='recipe-list'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe-detail'),
    path('recipes/add/', views.recipe_add, name='recipe-add'),
    path('recipes/<int:pk>/edit/', views.recipe_edit, name='recipe-edit'),
    path('recipes/<int:pk>/delete/', views.recipe_delete, name='recipe-delete'),
    path('recipes/<int:pk>/like/', views.toggle_like, name='recipe-like'),
    path('my-recipes/', views.my_recipes, name='my-recipes'),
    path('my-likes/', views.my_likes, name='my_likes'),
       # --- API Views ---
    path('api/recipes/', api_views.RecipeListCreateAPIView.as_view(), name='recipe-list-create'),
    path('api/recipes/<int:pk>/', api_views.RecipeRetrieveUpdateDestroyAPIView.as_view(), name='api-recipe-detail'),
]
