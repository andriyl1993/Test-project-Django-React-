import json

from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from models import status
from wrappers import good_validation, cart_valid
from bl import get_full_cart_info, get_cart, new_cart, all_stringify_goods, get_pay_systems, \
	is_enable_count_goods, get_pay_system
from django.views.decorators.csrf import csrf_exempt

def get_all_goods(request):
	goods = all_stringify_goods()

	if not request.session.get('cart'):
		request.session['cart'] = new_cart().serialize()

	return HttpResponse(json.dumps(goods))

@csrf_exempt
@cart_valid
@good_validation
def cart_add(request):
	good_id = request.POST.get('id')
	good_count = request.POST.get('count')

	cart = get_cart(request.session.get('cart'))
	res = cart.add_good(good_id, good_count)
	if res == status.get('success'):
		cart.save(request)

	return HttpResponse(res)

def cart_get(request):
	cart = get_cart(request.session.get('cart'))
	cart_data = get_full_cart_info(cart)

	return HttpResponse(json.dumps(cart_data))

@csrf_exempt
def cart_remove(request):
	id = request.POST.get('id')

	cart = get_cart(request.session.get('cart'))
	result = cart.remove_good(id)
	cart.save(request)

	return HttpResponse(result)

def pay_systems(request):
	return HttpResponse(json.dumps(get_pay_systems()))

@good_validation
def good_exist(request, id):
	count = request.GET.get('count')

	if is_enable_count_goods(int(id), int(count)):
		return HttpResponse(status.get('success'))
	else:
		return HttpResponse(status.get('error'))

@csrf_exempt
def confirm_pay(request):
	data = request.POST
	pay_system = data.get('pay_system')
	counter = 0

	cart = get_cart(request.session.get('cart'))
	cart.pay_system = pay_system
	cart.save(request)

	while True:
		if data.get("goods[{0}][id]".format(counter)):
			res = cart.add_good(
				good_id = data.get("goods[{0}][id]".format(counter)),
				count = data.get("goods[{0}][count]".format(counter))
			)
			counter += 1

			if res != 1:
				break
		else:
			break

	if res == 1: 
		cart.save(request)

	return HttpResponse(res)

@csrf_exempt
def pay(request):
	card_number = request.POST.get('card_number')
	cart = get_cart(request.session.get('cart'))
	
	res = cart.pay(card_number)
	return HttpResponse(res)
