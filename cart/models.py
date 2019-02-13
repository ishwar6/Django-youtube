from django.db import models

from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from product.models import Product

from django.contrib.auth import get_user_model
User = get_user_model()


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(
        default=0.00, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=8, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    @property
    def is_digital(self):
        qs = self.product.all()
        new_qs = qs.filter(is_digital=False)
        if new_qs.exists():
            return False
        return True


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        product = instance.product.all()
        total = Decimal(0.00)
        for x in product:
            total = Decimal(total) + Decimal(x.price)
        instance.total = total
        instance.save()
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.product.through)


class CartNew(models.Model):
    product = models.ManyToManyField(Product, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(
        blank=True, null=True, max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    subtotal = models.DecimalField(
        blank=True, null=True, max_digits=6, decimal_places=2)


def total_saver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_clear' or action == 'post_remove':
        product = instance.product.all()
        print(product)
        print(instance)
        total = Decimal(0.0)
        for p in product:
            total = total + p.price
        print(total)

        instance.subtotal = total
        total = total + total * Decimal(0.1)
        instance.total = total
        instance.save()


m2m_changed.connect(total_saver, sender=CartNew.product.through)
