from django.db import models
import uuid

# Create your models here.


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    zimmer_cust_no = models.PositiveIntegerField()
    name = models.CharField(max_length=60)

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    cat_name = models.CharField(max_length=30)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    sku_id = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    inv_no = models.PositiveIntegerField()
    billed_on = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    product_on_inv = models.ManyToManyField(Product, through='InvoiceProduct')

    def total(self):
        return int(sum([ip.extended_price for ip in self.invoiceproduct_set.all()]))

    def __str__(self):
        return f"{self.inv_no} ({self.customer.name})"

class InvoiceProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    qty = models.IntegerField()
    commission_rate = models.IntegerField()
    extended_price = models.FloatField()
    commission = models.FloatField()

    def save(self, *args, **kwargs):
        self.extended_price = float(self.price) * float(self.qty)
        self.commission = float(self.extended_price) * float(self.commission_rate) / 100
        super().save(*args, **kwargs)

# if i wanted to include customer_po, i would need to creat a new table. it would be a one to many field. 
# one po can have multiple invoices, but one invoice will never have multiple POs 