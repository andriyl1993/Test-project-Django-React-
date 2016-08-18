import json

from models import Good, PaySystem, Cart, deserialize, Liqpay, Privat, PayPal

def get_full_cart_info(cart):
	objs = Good.objects.filter(id__in = cart.goods.keys())
	goods = list(objs.values('id', 'photo', 'name', 'price'))

	for k, good in enumerate(goods):
		good['count'] = cart.goods[str(good.get('id'))]
		good['exists'] = objs[k].is_enable_count(int(cart.goods[str(good.get('id'))]))

	pay_system_obj = PaySystem.get_pay_class(int(cart.pay_system))()
	return { 'goods': goods, 'payment_system': pay_system_obj.serialize()}

def get_cart(data):
	return deserialize(Cart, json.loads(data))

def new_cart():
	return Cart()

def all_stringify_goods():
	return list(Good.objects.all().values())

def get_pay_systems():
	liqpay = Liqpay()
	privat = Privat()
	paypal = PayPal()
	
	return {
		liqpay.id: liqpay.name,
		privat.id: privat.name,
		paypal.id: paypal.name,
	}

def is_enable_count_goods(id, count):
	good = Good.objects.get(id = id)
	return good.is_enable_count(count)

def get_pay_system(id):
	return PaySystem.get_pay_class(id)