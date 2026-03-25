from django.core.management.base import BaseCommand
from records.models import Category

class Command(BaseCommand):
    help = 'Seeds the database with default dictionary categories'

    def handle(self, *args, **kwargs):
        categories = ['Noun', 'Verb', 'Adjective', 'Adverb', 'Slang', 'Idiom', 'Proverb']
        
        count = 0
        for cat_name in categories:
            # get_or_create prevents duplicates if you run the command twice
            obj, created = Category.objects.get_or_create(
                name=cat_name, 
                defaults={'description': f'Standard dictionary category: {cat_name}'}
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} new categories.'))