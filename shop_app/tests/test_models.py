from django.test import TestCase
from shop_app.models import FlowerList, Cart, Order, Promocode
from django.contrib.auth.models import User

class FlowerListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='test@example.com', password='password')
        self.client.login(username='admin', password='password')
        self.flower = FlowerList.objects.create(
            name="Test Flower",
            description="Test description",
            price=10.00,
            category='bouquet',
            archived=False,
            number_of_uses=0
        )

    def test_flower_list_creation(self):
        flower = FlowerList.objects.get(name="Test Flower")
        self.assertEqual(flower.price, 10.00)

    def test_str_method(self):
        flower = FlowerList.objects.get(name="Test Flower")
        self.assertEqual(str(flower), "Test Flower, ID = 1")

class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='test@example.com', password='password')
        self.client.login(username='admin', password='password')
        self.flower = FlowerList.objects.create(
            name="Test Flower",
            description="Test description",
            price=10.00,
            category='bouquet',
            archived=False,
            number_of_uses=0
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart.products.add(self.flower)

    def test_cart_creation(self):
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.products.count(), 1)

    def test_str_method(self):
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(str(cart), "ID = 1, автор = admin")

class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', email='test@example.com', password='password')
        self.client.login(username='admin', password='password')
        self.flower = FlowerList.objects.create(
            name="Test Flower",
            description="Test description",
            price=10.00,
            category='bouquet',
            archived=False,
            number_of_uses=0
        )

    def test_order_creation(self):
        order = Order.objects.create(
            delivery_adress='Moscow',
            phone='799999999',
            promocode='skidka15',
            user=self.user,
            final_sum=1500
        )
        order.products.add(self.flower)
        self.assertEqual(order.user.username, 'admin')
        product_names = [product.name for product in order.products.all()]
        self.assertIn('Test Flower', product_names)

class PromocodeTestCase(TestCase):
    def setUp(self):
        self.promocode = Promocode.objects.create(
            text='skidka15',
            count=15
        )

    def test_promocode_creation(self):
        promocode = Promocode.objects.get(text='skidka15')
        self.assertEqual(promocode.count, 15)
