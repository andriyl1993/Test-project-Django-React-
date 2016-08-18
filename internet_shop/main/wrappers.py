from validators import is_int, gt_zero, gt_eq_zero
from models import status, deserialize
from django.http import HttpResponse
from bl import new_cart

def good_validation(fn):
	def wrapper(request, id = 0):
		data = request.POST if request.POST else request.GET
		good_id = id if id else gt_zero(data.get('id'))

		if good_id and gt_eq_zero(data.get('count')):
			if id:
				return fn(request, id)
			else:
				return fn(request)
		else:
			return HttpResponse(status.get('error'))
	return wrapper

def cart_valid(fn):
	def wrapper(request):
		if not request.session.get('cart'):
			cart = new_cart()
			cart.save(request)

		return fn(request)
	return wrapper