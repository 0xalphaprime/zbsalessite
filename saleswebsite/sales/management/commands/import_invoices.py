import csv
from datetime import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import invoices from a CSV file'

    def handle(self, *args, **options):
        from sales.models import Customer, Category, Product, Invoice, InvoiceProduct
        with open('/Users/alphaprime/Documents/alphaprime/zbsalessite/saleswebsite/sales/zb_sales_data.csv') as file:
            reader = csv.reader(file)
            next(reader) # skip the header row

            for row in reader:
                # Convert date format to expected format
                billed_on = datetime.strptime(row[1], '%m/%d/%y').strftime('%Y-%m-%d %H:%M:%S')
                # Get or create the customer and category
                customer, _ = Customer.objects.get_or_create(zimmer_cust_no=row[2], name=row[3])
                category, _ = Category.objects.get_or_create(cat_name=row[6])

                # Get or create the product
                product, _ = Product.objects.get_or_create(sku_id=row[4], description=row[5], category=category)

                # Get or create the invoice
                invoice, _ = Invoice.objects.get_or_create(
                    inv_no=row[0],
                    billed_on=billed_on,
                    customer=customer
                )

                # Create the invoice product
                InvoiceProduct.objects.create(
                    invoice=invoice,
                    product=product,
                    price=row[9],
                    qty=float(row[8]),
                    commission_rate=row[11]
                )
                