from django.shortcuts import render
from django.shortcuts import redirect

from cart.models import Cart, CartNew
from product.models import Product


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


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "cart/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    empty = False

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.product.all():
            cart_obj.product.remove(product_obj)
            if cart_obj.product.count() == 0:

                cart_obj.delete()
                del request.session['cart_id']
                empty = True

            added = False
        else:
            # cart_obj.product.add(product_id)
            cart_obj.product.add(product_obj)
            added = True
        if not empty:
            request.session['cart_items'] = cart_obj.product.count()
        # return redirect(product_obj.get_absolute_url())
        if request.is_ajax():  # Asynchronous JavaScript And XML / JSON
            print("Ajax request")
            if not empty:
                json_data = {
                    "added": added,
                    "removed": not added,
                    "cartItemCount": cart_obj.product.count()
                }
            else:
                json_data = {
                    "added": added,
                    "removed": not added,
                    "cartItemCount": 0,
                }
            return JsonResponse(json_data)
    return redirect("cart:home")
