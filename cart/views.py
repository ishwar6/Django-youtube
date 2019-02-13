from django.shortcuts import render
from django.shortcuts import redirect

from cart.models import Cart, CartNew
from product.models import Product


def cart_update(request):
    product_id = request.POST.get('product_id', '')
    if product_id:
        try:
            product_obj = Product.objects.filter(id=product_id)
        except Product.DoesNotExist:
            return redirect("product:show")

        cart_obj, new_obj = Cart.objects.new_or_get(reuqest)
        if product_obj in cart_obj.product.all():
            cart_obj.product.remove(product_obj)
            if cart_obj.product.count() == 0:
                cart_obj.delete()
                del request.session['cart_id']
                empty = True
            added = False

        else:
            cart_obj.product.add(product_obj)
            added = True
        if not empty:
            request.session['cart_items'] = cart_obj.product.count()

            return True


def cart_add(request):
    user = request.user
    if user.is_authenticated:

        prod_id = request.POST.get('product_id')
        prod_obj = Product.objects.filter(id=prod_id).first()
        print(prod_obj)

        cart_obj = CartNew.objects.filter(user=user)
        if cart_obj.exists():
            cart_obj = cart_obj.first()
            if prod_obj in cart_obj.product.all():
                cart_obj.product.remove(prod_obj)
                return redirect('product:list')
            else:
                cart_obj.product.add(prod_obj)
                return redirect('product:list')

        else:
            cart_obj = CartNew.objects.create(user=user)

        cart_obj.product.add(prod_obj)
        return redirect('product:list')
