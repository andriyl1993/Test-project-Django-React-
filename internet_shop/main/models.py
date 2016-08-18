import json

from django.db import models
from pay_methods import liqpay, privat, paypal


status = {
	'error': 0,
	'success': 1,
	'exist_count_error': 2,
	'method_error': 3,
}

class Good(models.Model):
	name = models.CharField(max_length = 255)
	price = models.FloatField(default = 0)
	photo = models.ImageField(upload_to='')
	count = models.IntegerField(default = 0)

	def is_enable_count(self, count):
		if self.count >= count:
			return True
		else:
			return False

class PaySystem(object):

	def __init__(self):
		self.id = 0
		self.name = ""

	@staticmethod
	def get_pay_class(id):
		if id == 1:
			return Liqpay
		elif id == 2:
			return Privat
		elif id == 3:
			return PayPal
		else:
			return None

	def serialize(self):
		return {
			"id": self.id,
			"name": self.name,
		}


class Liqpay(PaySystem):

	def __init__(self):
		self.id = 1
		self.name = "liqpay"

	@staticmethod
	def pay(cart_number, sum):
		if liqpay(cart_number, sum):
			return status['success']
		else:
			return status['error']


class Privat(PaySystem):

	def __init__(self):
		self.id = 2
		self.name = "privat24"

	@staticmethod
	def pay(cart_number, sum):
		if privat(cart_number, sum):
			return status['success']
		else:
			return status['error']


class PayPal(PaySystem):

	def __init__(self):
		self.id = 3
		self.name = "paypal"

	@staticmethod
	def pay(cart_number, sum):
		if paypal(cart_number, sum):
			return status['success']
		else:
			return status['error']


class Cart(object):

	def __init__(self, goods = {}, pay_system = 1):
		self.goods = goods
		self.pay_system = pay_system

	def serialize(self):
		return json.dumps({
			"goods": self.goods, 
			"pay_system": self.pay_system,
		})

	def add_good(self, good_id, count):
		try:
			good = Good.objects.get(id = good_id)
		except:
			return status['error']

		if int(count) > 0 and good.is_enable_count(int(count)):
			self.goods[good_id] = count
			return status['success']
		else:
			return status['exist_count_error']

	def remove_good(self, good_id):
		if good_id in self.goods.keys():
			del self.goods[good_id]
			return status['success']
		else:
			return status['error']

	def debit(self):
		objs = self.goods_as_objs()

		for obj in objs:
			obj.count -= int(self.goods[str(obj.id)])
			if obj.count >= 0:
				obj.save()
			else:
				return status['exist_count_error']

		return status['success']

	def flush(self):
		self.goods = {};

	def goods_as_objs(self):
		arr = []
		for key, value in self.goods.iteritems():
			arr.append(key)
		
		if arr:
			return Good.objects.filter(id__in = arr)
		else:
			return []

	##  method - Class of using method
	def pay(self, cart_number):
		all_sum = 0
		method = PaySystem.get_pay_class(self.pay_system)

		if not method:
			return status['method_error']

		good_objs = self.goods_as_objs()
		for obj in good_objs:
			if not obj.is_enable_count(int(self.goods[str(obj.id)])):
				return status['exist_count_error']
			else:
				all_sum += obj.price * int(self.goods[str(obj.id)])

		if method.pay(cart_number, all_sum):
			self.debit()
			self.flush()
			return status['success']
		else:
			return  status['error']

	def save(self, request):
		json_cart = self.serialize()
		request.session['cart'] = json_cart


def deserialize(cls, data):
	obj = cls()
	for key, val in vars(obj).iteritems():
		setattr(obj, key, data.get(key))

	return obj