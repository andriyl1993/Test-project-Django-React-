def is_int(val):
	try:
		return isinstance(int(val), int)
	except:
		return False

def gt_zero(val):
	if is_int(val):
		return int(val) > 0
	else:
		return False

def gt_eq_zero(val):
	if is_int(val):
		return int(val) >= 0
	else:
		return False