from django.test import TestCase
from django.contrib.auth.models import User
from todo.models import TODO

class TodoAppTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='securepassword')
    
    def test_signup(self):
        response = self.client.post('/signup', {
            'fnm': 'newuser',
            'email': 'newuser@example.com',
            'pwd': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to /login
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post('/login', {
            'fnm': 'testuser',
            'pwd': 'securepassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to /todopage

    def test_create_todo(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.post('/todopage', {
            'title': 'Test TODO'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(TODO.objects.filter(title='Test TODO').exists())

    def test_edit_todo(self):
        self.client.login(username='testuser', password='securepassword')
        todo = TODO.objects.create(title='Initial Title', user=self.user)
        response = self.client.post(f'/edit_todo/{todo.srno}', {
            'title': 'Updated Title'
        })
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'Updated Title')

    def test_delete_todo(self):
        self.client.login(username='testuser', password='securepassword')
        todo = TODO.objects.create(title='To be deleted', user=self.user)
        response = self.client.post(f'/delete_todo/{todo.srno}')
        self.assertFalse(TODO.objects.filter(srno=todo.srno).exists())
