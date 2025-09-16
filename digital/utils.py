from .models import Profile, Product, Order, OrderProduct


class CartForAuthenticatedUser:
    def __init__(self, request, slug=None, action=None):
        self.user = request.user

        if slug and action:
            self.add_or_delete(slug, action)


    def get_cart_info(self):
        customer = Profile.objects.get(user=self.user)

        order, created = Order.objects.get_or_create(customer=customer, payment=False)
        order_products = order.orderproduct_set.all()

        order_total_price = order.get_order_total_price
        order_total_quantity = order.get_order_total_quantity

        return {
            'order': order,
            'order_products': order_products,
            'order_total_price': order_total_price,
            'order_total_quantity': order_total_quantity
        }

    def add_or_delete(self, slug, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(slug=slug)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity > 0 and product.quantity > order_product.quantity:
            order_product.quantity += 1
        elif action == 'delete':
            order_product.quantity -= 1

        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    # def finish_order(self):
    #     order = self.get_cart_info()['order']
    #     order_products = order.orderproduct_set.all()
    #     for order_product in order_products:
    #         item = Product.objects.get(pk=order_product.product.pk)
    #         item.quantity -= order_product.quantity
    #
    #     order.payment = True
    #     order.save()

    def finish_order(self):
        print("Функция finish_order вызвана")
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for order_product in order_products:
            item = Product.objects.get(pk=order_product.product.pk)
            print(f"До: {item.title} - {item.quantity}")
            item.quantity -= order_product.quantity
            item.save()
            print(f"После: {item.title} - {item.quantity}")

        order.payment = True
        order.save()


def get_cart_data(request):
    order = CartForAuthenticatedUser(request)
    order_info = order.get_cart_info()
    return order_info

