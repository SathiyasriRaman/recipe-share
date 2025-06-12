from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Recipe
from .forms import RecipeForm, CommentForm 
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'recipes/home.html')  # adjust path if template is in app

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})  # adjust path if needed

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/login.html', {'form': form})  # adjust path if needed

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'recipes/logged_out.html')  # adjust path if needed

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.recipe = recipe
            new_comment.user = request.user
            new_comment.save()
            return redirect('recipe-detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'form': form,
        'comments': comments,
    })
@login_required
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipe-list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Add Recipe'})
@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect('recipe-detail', pk=recipe.pk)
    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Edit Recipe'})
@login_required
@require_POST
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return redirect('recipe-list')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Recipe

@login_required
def toggle_like(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    if user in recipe.likes.all():
        recipe.likes.remove(user)
    else:
        recipe.likes.add(user)

    return redirect('recipe-detail', pk=pk)

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})
@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # ✅ THIS LINE
            recipe.save()
            return redirect('recipe-detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})

@login_required
def my_likes(request):
    liked_recipes = request.user.liked_recipes.all()
    return render(request, 'recipes/my_likes.html', {'recipes': liked_recipes})






