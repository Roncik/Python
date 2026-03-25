from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Word, Definition, Comment

class DictionaryTests(TestCase):
    
    def setUp(self):
        # 1. Set up data that will be run before every single test
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.category = Category.objects.create(name='Noun', description='A person, place, or thing.')
        
        self.word = Word.objects.create(term='Serendipity')
        self.word.categories.add(self.category)
        
        self.definition = Definition.objects.create(
            word=self.word, 
            author=self.user, 
            text='Finding something good without looking for it.'
        )

    # --- MODEL TESTS ---
    def test_word_creation(self):
        self.assertEqual(self.word.term, 'Serendipity')
        self.assertTrue(self.category in self.word.categories.all())

    def test_definition_creation(self):
        self.assertEqual(self.definition.author.username, 'testuser')
        self.assertEqual(self.definition.word.term, 'Serendipity')

    # --- VIEW TESTS (READ) ---
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_word_list_page(self):
        response = self.client.get(reverse('word_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Serendipity') # Checks if our test word is on the page

    def test_word_detail_page(self):
        response = self.client.get(reverse('word_detail', args=[self.word.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Finding something good without looking for it.')

    # --- VIEW TESTS (CREATE / PERMISSIONS) ---
    def test_add_word_redirects_if_logged_out(self):
        # Logged out users should be redirected to the login page (HTTP 302)
        response = self.client.get(reverse('add_word'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('add_word')}")

    def test_add_word_accessible_if_logged_in(self):
        # Logged in users should get a success code (HTTP 200)
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('add_word'))
        self.assertEqual(response.status_code, 200)

    def test_create_word_post_request(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('add_word'), {
            'term': 'Petrichor',
            'categories': [self.category.id],
            'text': 'The smell of rain.'
        })
        
        # Check if the total number of words in the database increased to 2
        self.assertEqual(Word.objects.count(), 2)
        self.assertEqual(Definition.objects.count(), 2)