# entries/admin.py
from django.contrib import admin
from .models import Category, Word, Definition, Comment, Vote

admin.site.register(Category)
admin.site.register(Word)
admin.site.register(Definition)
admin.site.register(Comment)
admin.site.register(Vote)