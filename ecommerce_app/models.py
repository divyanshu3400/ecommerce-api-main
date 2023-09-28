from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class NavbarCat(models.Model):
    nav_id = models.AutoField(primary_key=True)
    nav_name = models.CharField(max_length=200, blank=False, null=False)
    nav_logo = models.ImageField(upload_to='media/navbar_logos/', null=False, default='images')
    nav_status = models.BooleanField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'navbar_cat'
        verbose_name = 'Navbar Category'
        verbose_name_plural = 'Navbar Categories'

    def __str__(self):
        return self.nav_name


class ParentCategory(models.Model):
    nav = models.ForeignKey(NavbarCat, on_delete=models.CASCADE)
    pcat_id = models.AutoField(primary_key=True)
    pcat_name = models.CharField(max_length=200, blank=False, null=False)
    pcat_logos = models.ImageField(upload_to="media/parent_cat_logo/", null=False, default='images')
    pcat_status = models.BooleanField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'parent_categories'
        verbose_name = 'Parent Category'
        verbose_name_plural = 'Parent Categories'

    def __str__(self):
        return f"{self.pcat_name} ({self.nav.nav_name})"


class ChildCategory(models.Model):
    pcat = models.ForeignKey(ParentCategory, on_delete=models.CASCADE)
    child_cat_id = models.AutoField(primary_key=True)
    child_cat_name = models.CharField(max_length=200, blank=False, null=False)
    child_cat_status = models.BooleanField()
    child_cat_meta_name = models.TextField()
    child_cat_meta_desc = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'child_categories'
        verbose_name = 'Child Category'
        verbose_name_plural = 'Child Categories'

    def __str__(self):
        return f"{self.child_cat_name} - {self.pcat.pcat_name} ({self.pcat.nav.nav_name})"


class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    color_name = models.CharField(max_length=200, blank=False, null=False)
    color_hex = models.CharField(max_length=100)

    class Meta:
        db_table = 'color'
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return self.color_name.upper()

    def get_color_html(self):
        html = f'<div style="width: 20px; height: 20px; background-color: {self.color_hex};border-radius: 100%;"></div>'
        return mark_safe(html)

    get_color_html.short_description = 'Color Preview'


User = get_user_model()


class Logo(models.Model):
    image = models.ImageField(upload_to='images/')

    class Meta:
        db_table = 'educart_logo'
        managed = True
        verbose_name = 'Logo'
        verbose_name_plural = 'Logoes'


class OTPToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'otp_token'
        managed = True
        verbose_name = 'OTP Token'
        verbose_name_plural = 'OTP Tokens'

    def __str__(self):
        return self.token


class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'email_confirmation'
        managed = True
        verbose_name = 'Email Confirmation'
        verbose_name_plural = 'Email Confirmations'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    age = models.IntegerField(null=True, default=0)
    gender = models.CharField(max_length=200, default="NA", null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    class Meta:
        db_table = 'user_profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username


class State(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'state_list'
        managed = True
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cities_list'
        managed = True
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='addresses', blank=True, null=True)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        db_table = 'user_address'
        managed = True
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.address_line_1


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Address)
def associate_address_with_profile(sender, instance, created, **kwargs):
    if created and instance.profile is None:
        profile = Profile.objects.get(user=instance.user)
        instance.profile = profile
        instance.save()


class PaymentMethod(models.Model):
    method = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.method


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey("Brand", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(ChildCategory, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200, blank=False, null=False)
    discount_available = models.BooleanField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    meta_title = models.SlugField(max_length=200, unique=True, blank=True)
    product_description = models.TextField()
    product_available = models.BooleanField()
    units_in_stock = models.IntegerField()
    meta_description = models.TextField()
    created_at = models.DateTimeField()
    category_name = models.CharField(max_length=50, editable=False)

    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = slugify(self.product_name)

        if self.discount_available and self.discount_price is not None:
            self.new_price = self.calculate_new_price()
            self.discount_percent = self.calculate_discount_percent()

        if self.units_in_stock is None or self.units_in_stock < 0:
            self.units_in_stock = 0

        self.category_name = self.__class__.__name__
        super(Product, self).save(*args, **kwargs)

    def calculate_new_price(self):
        if self.discount_available and self.discount_price is not None:
            return self.product_price - self.discount_price
        else:
            return self.product_price

    def calculate_discount_percent(self):
        if self.product_price > 0:
            discount_percent = 100 - (((self.product_price - self.discount_price) / self.product_price) * 100)
            return round(discount_percent, 2)
        else:
            return 0

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/product_images/')

    class Meta:
        db_table = 'product_image'
        managed = True


class Brand(models.Model):
    parent = models.ForeignKey(ParentCategory, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.SlugField(max_length=200, unique=True, blank=True)
    meta_description = models.SlugField(max_length=200, unique=True, blank=True)
    status = models.BooleanField()
    brand_image = models.ImageField(upload_to='media/brand_logos')

    class Meta:
        db_table = 'products_brand'
        managed = True
        verbose_name = 'Product Brand'
        verbose_name_plural = 'Product Brands'

    
    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = slugify(self.brand_name)

        if not self.meta_description:
            self.meta_description = slugify(self.description)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.brand_name


class ElectronicProduct(Product):
    colors = models.ManyToManyField(Color, blank=True, default=None)
    model_number = models.CharField(max_length=50)
    display_size = models.CharField(max_length=20)
    resolution = models.CharField(max_length=20)
    processor = models.CharField(max_length=100)
    cellular_technology = models.CharField(max_length=20)
    memory = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    battery_life = models.CharField(max_length=50)
    operating_system = models.CharField(max_length=100)
    connectivity = models.CharField(max_length=100)
    warranty = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        db_table = 'electronic_product'
        verbose_name = 'Electronic Product'
        verbose_name_plural = 'Electronic Products'

    def __str__(self):
        return f"{self.product_name} -{self.memory}/{self.storage}"


class ProductSizes(models.Model):
    product_type = models.ManyToManyField(ParentCategory, related_name="product_sizes")
    product_size = models.CharField(max_length=20)

    class Meta:
        db_table = 'product_size'
        managed = True
        verbose_name = 'Product Size'
        verbose_name_plural = 'Product Sizes'

    def __str__(self):
        return f"{self.product_size}"


class BookProduct(Product):
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    publisher = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)
    genre = models.CharField(max_length=100)
    book_class = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    class Meta:
        db_table = 'book_product'
        managed = True
        verbose_name = 'Book Product'
        verbose_name_plural = 'Book Products'

    def __str__(self):
        return f"{self.title} by {self.author}"


class FashionProduct(Product):
    colors = models.ManyToManyField(Color, blank=True)
    sizes = models.ManyToManyField(ProductSizes, blank=True)
    material = models.CharField(max_length=100)

    class Meta:
        db_table = 'fashion_product'
        managed = True
        verbose_name = 'Fashion Product'
        verbose_name_plural = 'Fashion Products'

    def __str__(self):
        return f"{self.product_name}"
        # return f"{self.product_name} - {', '.join([str(color) for color in self.colors.all()])}, {', '.join([str(size) for size in self.sizes.all()])}"


class ProductInventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'product_inventory'
        managed = True
        verbose_name = 'Product Inventory'
        verbose_name_plural = 'Product Inventories'

    def __str__(self):
        return f"{self.product.product_name} - Quantity: {self.quantity}"


@receiver(post_save, sender=ProductInventory)
def update_product_quantity(sender, instance, **kwargs):
    previous_quantity = instance.product.quantity
    current_quantity = instance.quantity

    if previous_quantity < current_quantity:
        quantity_diff = current_quantity - previous_quantity
        instance.product.quantity += quantity_diff
    elif previous_quantity > current_quantity:
        quantity_diff = previous_quantity - current_quantity
        instance.product.quantity -= quantity_diff

    instance.product.save()


ORDER_STATUS_CHOICES = [('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'),
                        ('delivered', 'Delivered'), ('cancelled', 'Cancelled'), ]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    ordered_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'user_order'
        managed = True
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"OrderId #{self.id}-{self.user.first_name}"

    def get_product_count(self):
        return self.products.count()

    def get_total_quantity(self):
        order_items = OrderItem.objects.filter(order=self)
        total_quantity = sum(order_item.quantity for order_item in order_items)
        return total_quantity

    def get_ordered_products(self):
        return self.products.all()

    def get_order_total(self):
        return self.total_price

    def get_payment_methods(self):
        return self.payments.values_list('payment_method', flat=True)

    def is_fully_paid(self):
        total_paid = self.payments.aggregate(total_paid=models.Sum('amount')).get('total_paid', 0)
        return total_paid >= self.total_price

    def update_status(self, new_status):
        if new_status not in [choice[0] for choice in ORDER_STATUS_CHOICES]:
            raise ValueError("Invalid status value")
        self.status = new_status
        self.save()

    def place_order(self):
        order_items = self.orderitem_set.all()
        for order_item in order_items:
            product = order_item.product
            product.units_in_stock -= order_item.quantity
            product.save()

    def cancel_order(self):
        order_items = self.orderitem_set.all()
        for order_item in order_items:
            product = order_item.product
            product.units_in_stock += order_item.quantity
            product.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'order_item'
        managed = True
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.product_name}"

    def save(self, *args, **kwargs):
        if self.pk:
            previous_order_item = OrderItem.objects.get(pk=self.pk)
            quantity_change = self.quantity - previous_order_item.quantity
        else:
            quantity_change = self.quantity
        product = self.product
        product.units_in_stock -= quantity_change
        product.save()

        super(OrderItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        product = self.product
        product.units_in_stock += self.quantity
        product.save()

        super(OrderItem, self).delete(*args, **kwargs)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    status = models.BooleanField()

    class Meta:
        db_table = 'user_payment'
        managed = True
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment #{self.id} for Order #{self.order.id}"


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField()

    def get_star_rating(self):
        full_stars = int(self.rating)
        half_stars = 1 if (self.rating - full_stars) >= 0.5 else 0
        empty_stars = 5 - full_stars - half_stars

        return {
            'full_stars': full_stars,
            'half_stars': half_stars,
            'empty_stars': empty_stars}

    # def __str__(self):
    #     return f"Rating: {self.rating} - Product: {self.product.name}"

    class Meta:
        db_table = 'user_feedback'
        managed = True
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        return f"Rating: {self.rating} - User: {self.user.username}"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f'{self.user.username} - {self.product.product_name}'

    def clean(self):
        # Ensure a user cannot add the same product to their wishlist multiple times
        existing_wishlist_item = WishlistItem.objects.filter(user=self.user, product=self.product)
        if self.pk is None and existing_wishlist_item.exists():
            raise ValidationError("This product is already in your wishlist.")


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, through='CartItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0) 

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def grand_total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.subtotal()
        return total
    
    def clear_cart(self):
        CartItem.objects.filter(cart=self).delete()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_total_price() 

    def update_total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.subtotal()
        self.total_price = total

    class Meta:
        db_table = 'user_cart'
        managed = True
        verbose_name = 'User Cart'
        verbose_name_plural = 'User Carts'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} =  {self.subtotal()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_total_price()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.update_total_price()

    class Meta:
        db_table = 'car_item'
        managed = True
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
