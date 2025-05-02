from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

"""
    CASCADE: deletes the object containing the ForeignKey
    PROTECT: Prevent deletion of the referenced object.
    RESTRICT: Prevent deletion of the referenced object by raising RestrictedError

"""
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)
    category = models.ForeignKey(Category, related_name='menu_items', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(db_index=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('menuitem', 'user')

    def __str__(self):
        return f"{self.quantity} x {self.menuitem.title} for {self.user.username}"

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1.")

    def save(self, *args, **kwargs):
        self.unit_price = self.menuitem.price
        self.price = self.unit_price * self.quantity
        self.full_clean()
        super().save(*args, **kwargs)
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    date = models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')

    def __str__(self):
        return f"{self.quantity} x {self.menuitem.title} (Order #{self.order.id})"