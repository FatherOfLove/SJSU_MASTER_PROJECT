from django.test import SimpleTestCase
from django.urls import reverse, resolve
from piz.views import home,signup, access_code,logout_view, user_management, user_info_setting,user_result_view, consumer_data
class TestUrls(SimpleTestCase):

    def test_home_urls_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home)

    def test_signup_is_resolved(self):
        url = reverse('signup')
        print(resolve(url))
        self.assertEquals(resolve(url).func, signup)

    def test_access_code_is_resolved(self):
        url = reverse('access_code')
        print(resolve(url))
        self.assertEquals(resolve(url).func, access_code)

    def test_logout_urls_is_resolved(self):
        url = reverse('logout_view')
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout_view)

    def test_user_management_is_resolved(self):
        url = reverse('user_management')
        print(resolve(url))
        self.assertEquals(resolve(url).func, user_management)

    def test_user_info_setting_is_resolved(self):
        url = reverse('user_info_setting')
        print(resolve(url))
        self.assertEquals(resolve(url).func, user_info_setting)

    def test_user_info_setting_is_resolved(self):
        url = reverse('user_result_view', args=['1234'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, user_result_view)

    def test_user_info_setting_is_resolved(self):
        url = reverse('consumer_data')
        print(resolve(url))
        self.assertEquals(resolve(url).func, consumer_data)
