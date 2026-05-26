import unittest
from app import create_app, db
from app.models import User, Post

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('sqlite:///:memory:')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EBoard', response.data)

    def test_user_registration(self):
        response = self.client.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='password123',
            confirm_password='password123'
        ), follow_redirects=True)
        self.assertIn(b'Your account has been created', response.data)

    def test_user_login(self):
        with self.app.app_context():
            from app import bcrypt
            hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
            user = User(username='testuser', email='test@example.com', password=hashed_password)
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertIn(b'Logout', response.data)

    def test_create_post(self):
        # Create and login user
        self.test_user_login()
        
        # Create post
        response = self.client.post('/post/new', data=dict(
            title='Test Post',
            location='Warsaw',
            event_time='18:00',
            organizer='Jan Pythonowski',
            description='This is a test post.'
        ), follow_redirects=True)
        self.assertIn(b'Your post has been created', response.data)
        self.assertIn(b'Test Post', response.data)

if __name__ == '__main__':
    unittest.main()