#!/bin/bash

py manage.py shell <<EOF
from datetime import date, datetime
from crm.models import Customer

customers = Customer.objects.all()
count = 0

for customer in customers:
    latest_order = customer.orders.all().last()
    if latest_order:
        order_date = latest_order.order_date        
        diff = date.today() - order_date
        
        if diff.days > 365:
            customer.delete()
            count += 1
            continue
print(f'Removed ${count} customers - ${datetime.now}')

with open('/tmp/customer_cleanup_log.txt') as f:
    f.write(f'Removed ${count} customers - ${datetime.now}')
EOF
