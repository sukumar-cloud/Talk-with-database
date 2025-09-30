"""
Complete 15-Collection MongoDB Database Population
Collections: users, departments, employees, categories, products, customers,
suppliers, orders, order_items, payments, shipments, reviews, inventory,
sales, promotions
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['mydb']

print("Creating 15-Collection MongoDB Database...")
print("="*80)

# Drop existing collections
for col in ['users','departments','employees','categories','products','customers',
            'suppliers','orders','order_items','payments','shipments','reviews',
            'inventory','sales','promotions']:
    db[col].drop()

# COLLECTION 1: USERS
print("\n1/15 Creating users...")
users = []
for i in range(1, 501):
    users.append({
        "user_id": i,
        "username": f"user{i}",
        "email": f"user{i}@test.com",
        "full_name": f"User {i}",
        "phone": f"+1-555-{random.randint(1000,9999)}",
        "status": random.choice(["active","inactive"]),
        "created_at": datetime.now() - timedelta(days=random.randint(1,365))
    })
db.users.insert_many(users)
print(f"   Inserted {len(users)} users")

# COLLECTION 2: DEPARTMENTS
print("\n2/15 Creating departments...")
depts = []
dept_data = [("Engineering","ENG","Building A",1000000),("Sales","SAL","Building B",500000),
             ("Marketing","MKT","Building B",300000),("HR","HR","Building C",200000),
             ("Finance","FIN","Building C",400000),("Operations","OPS","Building D",600000),
             ("Support","SUP","Building E",250000),("R&D","RD","Building A",800000),
             ("Legal","LEG","Building C",350000),("IT","IT","Building A",700000)]
for idx, d in enumerate(dept_data, 1):
    depts.append({
        "department_id": idx,
        "name": d[0],
        "code": d[1],
        "location": d[2],
        "budget": d[3]
    })
db.departments.insert_many(depts)
print(f"   Inserted {len(depts)} departments")

# COLLECTION 3: EMPLOYEES
print("\n3/15 Creating employees...")
employees = []
positions = ["Manager","Developer","Designer","Analyst","Engineer","Specialist"]
for i in range(1, 301):
    employees.append({
        "employee_id": i,
        "employee_number": f"EMP{i:05d}",
        "first_name": f"First{i}",
        "last_name": f"Last{i}",
        "email": f"emp{i}@company.com",
        "phone": f"+1-555-{random.randint(1000,9999)}",
        "position": random.choice(positions),
        "department_id": random.randint(1,10),
        "salary": random.randint(40000,120000),
        "hire_date": (datetime.now()-timedelta(days=random.randint(30,1000))).isoformat(),
        "is_active": random.choice([True,False])
    })
db.employees.insert_many(employees)
print(f"   Inserted {len(employees)} employees")

# COLLECTION 4: CATEGORIES
print("\n4/15 Creating categories...")
cats = []
cat_data = [("Electronics","Devices"),("Clothing","Apparel"),("Food","Groceries"),
            ("Books","Literature"),("Toys","Games"),("Sports","Equipment"),
            ("Home","Furniture"),("Beauty","Cosmetics"),("Auto","Parts"),("Health","Wellness")]
for idx, c in enumerate(cat_data, 1):
    cats.append({
        "category_id": idx,
        "name": c[0],
        "description": c[1]
    })
db.categories.insert_many(cats)
print(f"   Inserted {len(cats)} categories")

# COLLECTION 5: PRODUCTS
print("\n5/15 Creating products...")
products = []
for i in range(1, 801):
    products.append({
        "product_id": i,
        "name": f"Product {i}",
        "sku": f"SKU{i:05d}",
        "category_id": random.randint(1,10),
        "price": round(random.uniform(10,500),2),
        "cost": round(random.uniform(5,250),2),
        "stock_quantity": random.randint(0,200),
        "weight": round(random.uniform(0.1,20),2),
        "is_active": random.choice([True,False]),
        "rating": round(random.uniform(1,5),1)
    })
db.products.insert_many(products)
print(f"   Inserted {len(products)} products")

# COLLECTION 6: CUSTOMERS
print("\n6/15 Creating customers...")
customers = []
for i in range(1, 601):
    customers.append({
        "customer_id": i,
        "name": f"Customer {i}",
        "email": f"cust{i}@test.com",
        "phone": f"+1-555-{random.randint(1000,9999)}",
        "address": f"{random.randint(100,999)} St",
        "city": random.choice(["NYC","LA","Chicago"]),
        "state": random.choice(["NY","CA","IL"]),
        "zip_code": f"{random.randint(10000,99999)}",
        "customer_type": random.choice(["retail","wholesale"]),
        "total_orders": random.randint(0,50),
        "total_spent": round(random.uniform(0,10000),2)
    })
db.customers.insert_many(customers)
print(f"   Inserted {len(customers)} customers")

# COLLECTION 7: SUPPLIERS
print("\n7/15 Creating suppliers...")
suppliers = []
for i in range(1, 51):
    suppliers.append({
        "supplier_id": i,
        "company_name": f"Supplier Co {i}",
        "contact_name": f"Contact {i}",
        "email": f"supplier{i}@company.com",
        "phone": f"+1-555-{random.randint(1000,9999)}",
        "address": f"{random.randint(100,999)} Ave",
        "city": random.choice(["Seattle","Boston","Miami"]),
        "country": "USA",
        "rating": round(random.uniform(3,5),1)
    })
db.suppliers.insert_many(suppliers)
print(f"   Inserted {len(suppliers)} suppliers")

# COLLECTION 8: ORDERS
print("\n8/15 Creating orders...")
orders = []
for i in range(1, 1001):
    subtotal = round(random.uniform(50,2000),2)
    tax = round(subtotal*0.08,2)
    shipping = round(random.uniform(5,30),2)
    orders.append({
        "order_id": i,
        "order_number": f"ORD{i:06d}",
        "customer_id": random.randint(1,600),
        "employee_id": random.randint(1,300),
        "order_date": (datetime.now()-timedelta(days=random.randint(1,180))).isoformat(),
        "status": random.choice(["pending","shipped","delivered","cancelled"]),
        "subtotal": subtotal,
        "tax_amount": tax,
        "shipping_cost": shipping,
        "total_amount": subtotal+tax+shipping
    })
db.orders.insert_many(orders)
print(f"   Inserted {len(orders)} orders")

# COLLECTION 9: ORDER_ITEMS
print("\n9/15 Creating order_items...")
order_items = []
for i in range(1, 2001):
    qty = random.randint(1,5)
    price = round(random.uniform(10,200),2)
    order_items.append({
        "order_item_id": i,
        "order_id": random.randint(1,1000),
        "product_id": random.randint(1,800),
        "quantity": qty,
        "unit_price": price,
        "subtotal": round(qty*price,2)
    })
db.order_items.insert_many(order_items)
print(f"   Inserted {len(order_items)} order items")

# COLLECTION 10: PAYMENTS
print("\n10/15 Creating payments...")
payments = []
for i in range(1, 1001):
    payments.append({
        "payment_id": i,
        "order_id": i,
        "payment_date": (datetime.now()-timedelta(days=random.randint(1,180))).isoformat(),
        "amount": round(random.uniform(50,2000),2),
        "payment_method": random.choice(["Credit Card","PayPal","Cash","Bank Transfer"]),
        "transaction_id": f"TXN{i:010d}",
        "status": random.choice(["completed","pending","failed"])
    })
db.payments.insert_many(payments)
print(f"   Inserted {len(payments)} payments")

# COLLECTION 11: SHIPMENTS
print("\n11/15 Creating shipments...")
shipments = []
for i in range(1, 801):
    ship_date = datetime.now()-timedelta(days=random.randint(1,150))
    shipments.append({
        "shipment_id": i,
        "order_id": random.randint(1,1000),
        "tracking_number": f"TRACK{i:010d}",
        "carrier": random.choice(["FedEx","UPS","DHL","USPS"]),
        "shipped_date": ship_date.isoformat(),
        "delivery_date": (ship_date+timedelta(days=random.randint(2,7))).isoformat() if random.choice([True,False]) else None,
        "status": random.choice(["in_transit","delivered","returned"])
    })
db.shipments.insert_many(shipments)
print(f"   Inserted {len(shipments)} shipments")

# COLLECTION 12: REVIEWS
print("\n12/15 Creating reviews...")
reviews = []
for i in range(1, 1201):
    reviews.append({
        "review_id": i,
        "product_id": random.randint(1,800),
        "customer_id": random.randint(1,600),
        "rating": random.randint(1,5),
        "title": f"Review Title {i}",
        "comment": f"This is review comment {i}",
        "review_date": (datetime.now()-timedelta(days=random.randint(1,365))).isoformat(),
        "helpful_count": random.randint(0,100)
    })
db.reviews.insert_many(reviews)
print(f"   Inserted {len(reviews)} reviews")

# COLLECTION 13: INVENTORY
print("\n13/15 Creating inventory...")
inventory = []
for i in range(1, 801):
    inventory.append({
        "inventory_id": i,
        "product_id": i,
        "warehouse_location": random.choice(["Warehouse A","Warehouse B","Warehouse C"]),
        "quantity_available": random.randint(0,500),
        "quantity_reserved": random.randint(0,50),
        "reorder_level": 50,
        "last_stock_date": (datetime.now()-timedelta(days=random.randint(1,90))).isoformat()
    })
db.inventory.insert_many(inventory)
print(f"   Inserted {len(inventory)} inventory records")

# COLLECTION 14: SALES
print("\n14/15 Creating sales...")
sales = []
for i in range(1, 1001):
    amount = round(random.uniform(100,3000),2)
    sales.append({
        "sale_id": i,
        "order_id": i,
        "employee_id": random.randint(1,300),
        "customer_id": random.randint(1,600),
        "sale_date": (datetime.now()-timedelta(days=random.randint(1,180))).isoformat(),
        "amount": amount,
        "commission": round(amount*0.05,2),
        "region": random.choice(["North","South","East","West"])
    })
db.sales.insert_many(sales)
print(f"   Inserted {len(sales)} sales records")

# COLLECTION 15: PROMOTIONS
print("\n15/15 Creating promotions...")
promotions = []
for i in range(1, 51):
    start = datetime.now()-timedelta(days=random.randint(0,90))
    promotions.append({
        "promotion_id": i,
        "code": f"PROMO{i:03d}",
        "description": f"Promotion {i} description",
        "discount_type": random.choice(["percentage","fixed"]),
        "discount_value": round(random.uniform(5,50),2),
        "start_date": start.isoformat(),
        "end_date": (start+timedelta(days=random.randint(30,90))).isoformat(),
        "max_uses": random.randint(100,1000),
        "times_used": random.randint(0,500),
        "is_active": random.choice([True,False])
    })
db.promotions.insert_many(promotions)
print(f"   Inserted {len(promotions)} promotions")

print("\n" + "="*80)
print("COMPLETE! 15 MongoDB Collections Created:")
print("="*80)
print("  1. users (500 documents)")
print("  2. departments (10 documents)")
print("  3. employees (300 documents)")
print("  4. categories (10 documents)")
print("  5. products (800 documents)")
print("  6. customers (600 documents)")
print("  7. suppliers (50 documents)")
print("  8. orders (1000 documents)")
print("  9. order_items (2000 documents)")
print("  10. payments (1000 documents)")
print("  11. shipments (800 documents)")
print("  12. reviews (1200 documents)")
print("  13. inventory (800 documents)")
print("  14. sales (1000 documents)")
print("  15. promotions (50 documents)")
print("\nTotal Documents: 9,120")
print("="*80)

client.close()
