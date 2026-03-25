import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from records.models import Word, Definition

class Command(BaseCommand):
    help = 'Imports words and definitions from a CSV file'

    def add_arguments(self, parser):
        # This allows the command to accept a file path as an argument
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        # We need an author for the definitions. Let's get or create a system user.
        user, _ = User.objects.get_or_create(username='SystemImporter')

        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                count = 0
                for row in reader:
                    term = row.get('term')
                    text = row.get('definition')
                    
                    if term and text:
                        word, _ = Word.objects.get_or_create(term=term)
                        Definition.objects.create(word=word, text=text, author=user)
                        count += 1
                        
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} words from {csv_file}.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: File "{csv_file}" does not exist.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))