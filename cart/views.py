from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages



# View for displaying the cart summary
def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods()
	quantities = cart.get_quants()
	totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})



# View for adding a product to the cart
def cart_add(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))
		product = get_object_or_404(Product, id=product_id)

		cart.add(product,product_qty)
		quantity = cart.__len__()
		response = JsonResponse({'qty': quantity})
		#messages.success(request, ("Product Added To Cart..."))
		return response


def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		#return redirect('cart_summary')
		messages.success(request, ("Your Cart Has Been Updated..."))
		return response

def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
		cart.delete(product=product_id)
		response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response