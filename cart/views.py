from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.contrib import messages
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()  # <-- add parentheses to call the method

    # Sort by product ID descending
    cart_products = sorted(cart_products, key=lambda p: p.id, reverse=True)

    quantities = cart.get_quants  # (if get_quants is a property, leave as is; if it's a method, use get_quants())
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals
    })

def cart_add(request):
    #Get the cart
    cart = Cart(request)
    #Test for post
    if request.POST.get('action') == 'post':
        
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #Lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        #Save to session
        cart.add(product=product, quantity=product_qty)

        #Get cart quantity
        cart_quantity = cart.__len__()

        #Return a response
        #responce = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ('Item added to cart.'))
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request, ('Cart has been updated.'))
        return response
        #return redirect('cart_summary')

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        #Call delete function in cart
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request, ('Item delete from your cart.'))
        return response

