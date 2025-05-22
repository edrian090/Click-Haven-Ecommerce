from .cart import Cart

#Create context processor so our cart can work on all pages of the sites
def cart(request):
    #Return the default data from the Cart
    return {'cart': Cart(request)}