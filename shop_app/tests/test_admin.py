import io
from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from shop_app.admin import OrderAdmin
from shop_app.models import FlowerList, Order
from django.contrib.auth.models import User


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
        self.client.login(username='admin', password='admin')

class FlowerAdminTest(AdminTestCase):
    def test_flower_admin_page_loads(self):
        response = self.client.get(reverse('admin:shop_app_flowerlist_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_flower_admin_search(self):
        response = self.client.get(reverse('admin:shop_app_flowerlist_changelist') + '?q=test')
        self.assertEqual(response.status_code, 200)

class CartAdminTest(AdminTestCase):
    def test_cart_admin_page_loads(self):
        response = self.client.get(reverse('admin:shop_app_cart_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_export_csv(self):
        # Создаем несколько заказов для теста
        Order.objects.create(id=1, delivery_adress="Address 1", promocode="code1", phone="123456", user_id=self.admin_user.id, final_sum=100)
        Order.objects.create(id=2, delivery_adress="Address 2", promocode="code2", phone="654321", user_id=self.admin_user.id, final_sum=200)

        admin_site = AdminSite()
        order_admin = OrderAdmin(Order, admin_site)
        export_url = reverse('admin:export_products_csv')  # Используйте имя URL 'export_csv'
        response = self.client.get(export_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, b'')

    def test_import_csv(self):
        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.flower = FlowerList.objects.create(
            image=self.image,
            name="Test Flower",
            description="Test description",
            price=10.00,
            category='bouquet',
            archived=False,
            number_of_uses=0
        )

        csv_content = "ID,DelAdr,Promocode,Phone,User_ID,ID_Products,Final_Sum\n1,123,skidka15,123,1,1,2500\n2,123,skidka15,123,1,1,2500"
        csv_file = io.StringIO(csv_content)
        csv_file.name = 'test.csv'

        admin_site = AdminSite()
        order_admin = OrderAdmin(Order, admin_site)
        import_url = reverse('admin:import_products_csv')
        response = self.client.post(import_url, {'csv_file': csv_file})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 2)


class OrderAdminTest(AdminTestCase):
    def test_order_admin_page_loads(self):
        response = self.client.get(reverse('admin:shop_app_order_changelist'))
        self.assertEqual(response.status_code, 200)

class CustomUserAdminTest(AdminTestCase):
    def test_custom_user_admin_page_loads(self):
        response = self.client.get(reverse('admin:auth_user_changelist'))
        self.assertEqual(response.status_code, 200)

class PromocodeAdminTest(AdminTestCase):
    def test_promocode_admin_page_loads(self):
        response = self.client.get(reverse('admin:shop_app_promocode_changelist'))
        self.assertEqual(response.status_code, 200)