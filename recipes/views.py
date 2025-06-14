from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from .models import Recipe, Comment
from .forms import RecipeForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    template_name = 'recipes/account_confirm_delete.html'
    success_url = reverse_lazy('home')  # or your landing page
    model = User

    def get_object(self):
        return self.request.user

def home(request):
    return render(request, 'recipes/home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'recipes/logged_out.html')


@login_required
def profile_view(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipes/profile.html', {
        'user': request.user,
        'recipes': recipes
    })

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'recipes/delete_account_confirm.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keeps user logged in
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'recipes/change_password.html', {'form': form})

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
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe-detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Add Recipe'})


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")

    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect('recipe-detail', pk=recipe.pk)
    return render(request, 'recipes/recipe_form.html', {'form': form, 'title': 'Edit Recipe'})


@login_required
@require_POST
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this recipe.")
    recipe.delete()
    return redirect('recipe-list')


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
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})


@login_required
def my_likes(request):
    liked_recipes = request.user.liked_recipes.all()
    return render(request, 'recipes/my_likes.html', {'recipes': liked_recipes})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user or request.user.is_superuser:
        comment.delete()
        return redirect('recipe-detail', pk=comment.recipe.pk)
    else:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully changed!')
            return redirect('profile')  # or your success page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'recipes/change_password.html', {'form': form})






















