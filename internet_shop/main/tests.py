import json

from django.test.client import Client
import unittest2

from models import Good

class GoodsTest(unittest2.TestCase):
	def setUp(self):
		for i in range(10):
			good = Good()
			good.name = "good{0}".format(i)
			good.price = 10
			good.photo = "/media/good2.png"
			good.count = 10 * i
			good.save()
		return True

	def test_get_goods(self):
		client = Client()
		response = client.get('/good/all/')

		try:
			arr = json.loads(response.content)
		except:
			arr = []

		return self.assertGreaterEqual(len(arr), 10)

	def test_good_not_exist(self):
		client = Client()

		good = Good.objects.create(name="good1", price=1000, photo="/media/good1.png", count=0)
		response = client.get('/good/exist/{0}/'.format(good.id))
		return self.assertEqual(int(response.content), 0)

	def test_good_exist(self):
		client = Client()

		good = Good.objects.create(name="good_exist", price=1000, photo="/media/good1.png", count=10)
		response = client.get('/good/exist/{0}/?count={1}'.format(good.id, 4))
		return self.assertEqual(int(response.content), 1)

class CartTest(unittest2.TestCase):
	def setUp(self):
		for i in range(10):
			good = Good()
			good.name = "good{0}".format(i)
			good.price = 10
			good.photo = "/media/good2.png"
			good.count = 10 * i
			good.save()
		return True

	def test_add(self):
		client = Client()

		good = Good.objects.filter(count__gt = 1).last()
		response = client.post('/cart/add/', {'id': good.id, 'count': good.count - 1})
		return self.assertEqual(int(response.content),1)

if __name__ == "__main__":
	unittest2.main()