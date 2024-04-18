from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    role = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100,default="")
    phone_number = models.CharField(max_length=15,default="")
   





    #user_type = models.CharField(max_length=20)  # Add any additional fields you need

    def _str_(self):
        return self.username
    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default= 0.0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=(("active", "Active"), ("inactive", "Inactive")))
    product_image = models.ImageField(upload_to='product_images/')
    
    def save(self, *args, **kwargs):
    # Convert self.discount to a float and then calculate the sale price
     self.discount = float(self.discount)
     self.sale_price = self.price - (self.price * (self.discount / 100))
     super(Product, self).save(*args, **kwargs)

    def _str_(self):
        return self.product_name
    

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def get_cart_total(self):
        return sum(item.get_item_total() for item in self.cartitem_set.all())

    def _str_(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_item_total(self):
        return self.product.sale_price * self.quantity

    def _str_(self):
        return f"{self.quantity} x {self.product.product_name} in {self.cart}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)

    def _str_(self):
        return self.username
    


class CartItem1(models.Model):
    cart = models.ForeignKey('Cart1', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def _str_(self):
        return f"{self.quantity} x {self.product.name}"

class Cart1(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem1')

    def _str_(self):
        return f"Cart for {self.user.username}"
    
class Order(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='PENDING')

    
    def _str_(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.id}"
    
# models.py


class JobApplication(models.Model):
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    VEHICLE_TYPE_CHOICES = [
        ('bike', 'Bike'),
        ('car', 'Car'),
    ]

    EDUCATION_CHOICES = [
        ('10th', '10th Level'),
        ('12th', '12th Level'),
        ('degree', 'Degree'),
    ]

    EXPERIENCE_CHOICES = [
        ('0', '0'),
        ('1-2', '1-2'),
        ('2-3', '2-3'),
        ('3-5', '3-5'),
        ('more', 'More than 5'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    full_address = models.TextField()
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)
    vehicle_number = models.CharField(max_length=20)
    license = models.FileField(upload_to='licenses/')
    highest_education = models.CharField(max_length=10, choices=EDUCATION_CHOICES)
    languages_known = models.CharField(max_length=255)
    years_of_experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    resume = models.FileField(upload_to='resumes/')

from django.db import models

class ServiceRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    service_required = models.CharField(max_length=100)
    description = models.TextField()
    select_date = models.DateField()

    def _str_(self):
        return self.name

# models.py


class PlumberAvailability(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    availability_date = models.DateField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.user.username} - {self.availability_date}"

from django.core.validators import MaxLengthValidator

class Availability(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    available_date = models.DateField()
    cities = models.TextField(validators=[MaxLengthValidator(1000)])  # Maximum length of 1000 characters
    district = models.CharField(max_length=100)

    def _str_(self):
        return f"Availability for {self.district} on {self.available_date}"


from django.utils import timezone

class CustomerServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    service_required = models.CharField(max_length=100)
    description = models.TextField()
    select_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    work_status = models.CharField(max_length=20, default='Not Completed')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


# models.py

from django.db import models
from .models import CustomerServiceRequest  # Import the CustomerServiceRequest model


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    service_request = models.ForeignKey(CustomerServiceRequest, on_delete=models.CASCADE)

    
class PlumberJob(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    full_address = models.TextField()
    highest_education = models.CharField(max_length=10)
    languages_known = models.CharField(max_length=255)
    years_of_experience = models.CharField(max_length=10)
    resume = models.FileField(upload_to='resumes/')

    def _str_(self):
        return self.full_name
    

# models.py

from django.db import models


class ServiceType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

