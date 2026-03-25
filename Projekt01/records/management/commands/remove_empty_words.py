from django.core.management.base import BaseCommand
from records.models import Word

class Command(BaseCommand):
    help = 'Removes words that have no definitions associated with them'

    def handle(self, *args, **kwargs):
        # Find words where the related 'definitions' mapping is empty
        empty_words = Word.objects.filter(definitions__isnull=True)
        count = empty_words.count()
        
        if count > 0:
            empty_words.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} empty words.'))
        else:
            self.stdout.write(self.style.SUCCESS('Database is clean. No empty words found.'))