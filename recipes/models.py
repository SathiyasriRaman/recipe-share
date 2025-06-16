from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    steps = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    #image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return self.title

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.recipe.title}'
