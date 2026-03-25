from django.db import models
from django.contrib.auth.models import User

# 1. Category Model
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# 2. Word Model (Many-to-Many with Category)
class Word(models.Model):
    term = models.CharField(max_length=100, unique=True)
    categories = models.ManyToManyField(Category, related_name='words')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term

# 3. Definition Model (One-to-Many with Word and User)
class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='definitions')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.word.term} - {self.text[:20]}..."
    
    @property
    def score(self):
        upvotes = self.votes.filter(is_upvote=True).count()
        downvotes = self.votes.filter(is_upvote=False).count()
        return upvotes - downvotes

# 4. Comment Model (One-to-Many with Word and User)
class Comment(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.word.term}"

# 5. Vote Model (One-to-Many with Definition and User)
class Vote(models.Model):
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_upvote = models.BooleanField(default=True)

    class Meta:
        # A user can only vote once per definition
        unique_together = ('definition', 'user')

    def __str__(self):
        vote_type = "+1" if self.is_upvote else "-1"
        return f"{self.user.username} voted {vote_type} on {self.definition.id}"