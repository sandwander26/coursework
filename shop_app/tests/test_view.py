from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from shop_app.models import FlowerList, Order, Cart

class StatusCodeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', email='admin@example.com', password='password')
        self.client.login(username='admin', password='password')

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

    def test_homepage_page_view(self):
        url = reverse('shop_app:shop_app')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'shop_app/base.html')
        self.assertTemplateUsed(response, 'shop_app/color_shop.html')

    def test_cart_page_view(self):
        url = reverse('shop_app:cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'shop_app/base.html')
        self.assertTemplateUsed(response, 'shop_app/cart_details.html')

    def test_details_page_view(self):
        url = ('/details/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse('shop_app:details', args=[self.flower.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'shop_app/base.html')
        self.assertTemplateUsed(response, 'shop_app/flower_details.html')

    def test_search_page_view(self):
        search_query = "search"
        url = reverse('shop_app:search')
        response = self.client.get(url, {'search': search_query})
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'shop_app/base.html')
        self.assertTemplateUsed(response, 'shop_app/search_view.html')

    def test_order_details_page_view(self):
        order = Order.objects.create(
            delivery_adress='Moscow',
            phone='799999999',
            promocode='skidka15',
            user=self.user,
            final_sum=1500
        )

        order.products.add(self.flower)

        url = reverse('shop_app:order_details', args=[order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'shop_app/base.html')
        self.assertTemplateUsed(response, 'shop_app/order_details.html')

class SearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', email='admin@example.com', password='password')
        self.client.login(username='admin', password='password')

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

        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.flower = FlowerList.objects.create(
            image=self.image,
            name="Random Name",
            description="Test description",
            price=10.00,
            category='bouquet',
            archived=False,
            number_of_uses=0
        )

    def test_search_page(self):
        search_query = "Test Flower"
        url = reverse('shop_app:search')
        response = self.client.get(url, {'search': search_query})
        self.assertEqual(response.context['flowers_list'][0].name, search_query)

class OrderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', email='admin@example.com', password='password')
        self.client.login(username='admin', password='password')

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

        self.order = Order.objects.create(
            delivery_adress='Moscow',
            phone='799999999',
            promocode='skidka15',
            user=self.user,
            final_sum=1500
        )

        self.order.products.add(self.flower)

    def test_permission_page(self):
        '''Проверка отказа в доступе аккаунту, который не совершал данный заказ'''
        url = reverse('shop_app:order_details', args=[self.order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.user = User.objects.create_user(username='Johny', email='Johny@example.com', password='password')
        self.client.login(username='Johny', password='password')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

class AddAndDeleteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', email='admin@example.com', password='password')
        self.client.login(username='admin', password='password')

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

    def test_add_detele_to_cart_page_view(self):
        test_flower = FlowerList.objects.create(
            image=self.image,
            name="Test Flower",
            description="Test description",
            price=10.00,
            category='bouquet',
            archived=False,
            number_of_uses=0,
        )

        url = reverse('shop_app:add_to_cart', args=[test_flower.pk])
        response = self.client.post(url)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(test_flower, cart.products.first())

        url = reverse('shop_app:delete_from_cart', args=[test_flower.pk])
        response = self.client.post(url)
        self.assertNotEqual(test_flower, cart.products.first())

class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', email='admin@example.com', password='password')
        self.client.login(username='admin', password='password')

        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.flower_test = FlowerList.objects.create(
            image=self.image,
            name="Test Flower",
            description="Test description",
            price=10.00,
            category='bouquet',
            archived=False,
            number_of_uses=0
        )

    def test_post_request(self):
        cart = Cart.objects.create(user=self.user)
        cart.products.add(self.flower_test)


        form_data = {
            'delivery_adress': 'Moscow',
            'promocode': 'skidka15',
            'phone': '799999999'
        }

        url = reverse('shop_app:cart')
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.all().count(), 1)

        order = Order.objects.first()

        self.assertEqual(order.delivery_adress, form_data['delivery_adress'])
        self.assertEqual(order.promocode, form_data['promocode'])
        self.assertEqual(order.phone, int(form_data['phone']))

        self.assertEqual(order.products.count(), 1)

        self.assertEqual(FlowerList.objects.get(pk=self.flower_test.pk).number_of_uses, 1)