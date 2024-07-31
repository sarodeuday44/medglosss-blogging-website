from django.test import Client, RequestFactory, TestCase
from blog.models import Article, Category, Tag
from django.contrib.auth import get_user_model
from Medgloss.utils import delete_view_cache, delete_sidebar_cache
from accounts.models import BlogUser
from django.urls import reverse
from Medgloss.utils import *
from django.conf import settings
from django.utils import timezone


# Create your tests here.

class AccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_validate_account(self):
        site = get_current_site().domain
        user = BlogUser.objects.create_superuser(
            email="medgloss@gmail.com",
            username="Deepak",
            password="r b s k d ")
        testuser = BlogUser.objects.get(username='Deepak')

        loginresult = self.client.login(
            username='Deepak',
            password='r b s k d ')
        self.assertEqual(loginresult, True)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        category = Category()
        category.name = "Test name"
        category.created_time = timezone.now()
        category.last_mod_time = timezone.now()
        category.save()

        article = Article()
        article.title = "Test Title"
        article.body = "Test Body"
        article.author = user
        article.category = category
        article.type = 'a'
        article.status = 'p'
        article.save()

        response = self.client.get(article.get_admin_url())
        self.assertEqual(response.status_code, 200)

    def test_validate_register(self):
        self.assertEquals(
            0, len(
                BlogUser.objects.filter(
                    email='user123@user.com')))
        response = self.client.post(reverse('account:register'), {
            'username': 'user1233',
            'email': 'user123@user.com',
            'password1': 'r b s k d ',
            'password2': 'r b s k d ',
        })
        self.assertEquals(
            1, len(
                BlogUser.objects.filter(
                    email='test123@user.com')))
        user = BlogUser.objects.filter(email='test123@user.com')[0]
        sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))
        path = reverse('accounts:result')
        url = '{path}?type=validation&id={id}&sign={sign}'.format(
            path=path, id=user.id, sign=sign)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username='test1233', password='r b s k d ')
        user = BlogUser.objects.filter(email='user123@user.com')[0]
        user.is_superuser = True
        user.is_staff = True
        user.save()
        delete_sidebar_cache(user.username)
        category = Category()
        category.name = "Test Category"
        category.created_time = timezone.now()
        category.last_mod_time = timezone.now()
        category.save()

        article = Article()
        article.category = category
        article.title = "Test Title"
        article.body = "Test Content"
        article.author = user

        article.type = 'a'
        article.status = 'p'
        article.save()

        response = self.client.get(article.get_admin_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('account:logout'))
        self.assertIn(response.status_code, [301, 302, 200])

        response = self.client.get(article.get_admin_url())
        self.assertIn(response.status_code, [301, 302, 200])

        response = self.client.post(reverse('account:login'), {
            'username': 'user1233',
            'password': 'password123'
        })
        self.assertIn(response.status_code, [301, 302, 200])

        response = self.client.get(article.get_admin_url())
        self.assertIn(response.status_code, [301, 302, 200])
