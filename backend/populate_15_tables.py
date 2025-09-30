"""
Complete 15-Table MySQL Database Population
Tables: users, departments, employees, categories, products, customers, 
suppliers, orders, order_items, payments, shipments, reviews, inventory, 
sales, promotions
"""

from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()
db_uri = os.getenv("DB_URI")
engine = create_engine(db_uri)

print("Creating 15-Table MySQL Database...")
print("="*80)

with engine.connect() as conn:
    conn.execute(text("DROP DATABASE IF EXISTS mydb"))
    conn.execute(text("CREATE DATABASE mydb"))
    conn.execute(text("USE mydb"))
    conn.commit()
    
    # TABLE 1: USERS
    print("\n1/15 Creating USERS...")
    conn.execute(text("""
        CREATE TABLE users (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE,
            email VARCHAR(100) UNIQUE,
            full_name VARCHAR(100),
            phone VARCHAR(20),
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    for i in range(1, 501):
        conn.execute(text("INSERT INTO users (username, email, full_name, phone, status) VALUES (:u, :e, :f, :p, :s)"),
                    {"u": f"user{i}", "e": f"user{i}@test.com", "f": f"User {i}", 
                     "p": f"+1-555-{random.randint(1000,9999)}", "s": random.choice(["active","inactive"])})
    conn.commit()
    print("   Inserted 500 users")
    
    # TABLE 2: DEPARTMENTS
    print("\n2/15 Creating DEPARTMENTS...")
    conn.execute(text("""
        CREATE TABLE departments (
            department_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            code VARCHAR(20),
            location VARCHAR(100),
            budget DECIMAL(12,2)
        )
    """))
    depts = [("Engineering","ENG","Building A",1000000), ("Sales","SAL","Building B",500000),
             ("Marketing","MKT","Building B",300000), ("HR","HR","Building C",200000),
             ("Finance","FIN","Building C",400000), ("Operations","OPS","Building D",600000),
             ("Support","SUP","Building E",250000), ("R&D","RD","Building A",800000),
             ("Legal","LEG","Building C",350000), ("IT","IT","Building A",700000)]
    for d in depts:
        conn.execute(text("INSERT INTO departments (name,code,location,budget) VALUES (:n,:c,:l,:b)"),
                    {"n":d[0],"c":d[1],"l":d[2],"b":d[3]})
    conn.commit()
    print("   Inserted 10 departments")
    
    # TABLE 3: EMPLOYEES
    print("\n3/15 Creating EMPLOYEES...")
    conn.execute(text("""
        CREATE TABLE employees (
            employee_id INT PRIMARY KEY AUTO_INCREMENT,
            employee_number VARCHAR(20),
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100),
            phone VARCHAR(20),
            position VARCHAR(100),
            department_id INT,
            salary DECIMAL(10,2),
            hire_date DATE,
            is_active BOOLEAN,
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
        )
    """))
    positions = ["Manager","Developer","Designer","Analyst","Engineer","Specialist"]
    for i in range(1, 301):
        conn.execute(text("""INSERT INTO employees (employee_number,first_name,last_name,email,phone,position,
                         department_id,salary,hire_date,is_active) VALUES (:en,:fn,:ln,:e,:p,:pos,:d,:s,:h,:a)"""),
                    {"en":f"EMP{i:05d}", "fn":f"First{i}", "ln":f"Last{i}", "e":f"emp{i}@company.com",
                     "p":f"+1-555-{random.randint(1000,9999)}", "pos":random.choice(positions),
                     "d":random.randint(1,10), "s":random.randint(40000,120000),
                     "h":(datetime.now()-timedelta(days=random.randint(30,1000))).date(),
                     "a":random.choice([True,False])})
    conn.commit()
    print("   Inserted 300 employees")
    
    # TABLE 4: CATEGORIES
    print("\n4/15 Creating CATEGORIES...")
    conn.execute(text("""
        CREATE TABLE categories (
            category_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            description TEXT
        )
    """))
    cats = [("Electronics","Devices"),("Clothing","Apparel"),("Food","Groceries"),
            ("Books","Literature"),("Toys","Games"),("Sports","Equipment"),
            ("Home","Furniture"),("Beauty","Cosmetics"),("Auto","Parts"),("Health","Wellness")]
    for c in cats:
        conn.execute(text("INSERT INTO categories (name,description) VALUES (:n,:d)"),{"n":c[0],"d":c[1]})
    conn.commit()
    print("   Inserted 10 categories")
    
    # TABLE 5: PRODUCTS
    print("\n5/15 Creating PRODUCTS...")
    conn.execute(text("""
        CREATE TABLE products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(200),
            sku VARCHAR(50),
            category_id INT,
            price DECIMAL(10,2),
            cost DECIMAL(10,2),
            stock_quantity INT,
            weight DECIMAL(10,2),
            is_active BOOLEAN,
            rating DECIMAL(3,1),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """))
    for i in range(1, 801):
        conn.execute(text("""INSERT INTO products (name,sku,category_id,price,cost,stock_quantity,weight,is_active,rating)
                         VALUES (:n,:s,:c,:p,:co,:st,:w,:a,:r)"""),
                    {"n":f"Product {i}", "s":f"SKU{i:05d}", "c":random.randint(1,10),
                     "p":round(random.uniform(10,500),2), "co":round(random.uniform(5,250),2),
                     "st":random.randint(0,200), "w":round(random.uniform(0.1,20),2),
                     "a":random.choice([True,False]), "r":round(random.uniform(1,5),1)})
    conn.commit()
    print("   Inserted 800 products")
    
    # TABLE 6: CUSTOMERS
    print("\n6/15 Creating CUSTOMERS...")
    conn.execute(text("""
        CREATE TABLE customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            address VARCHAR(200),
            city VARCHAR(50),
            state VARCHAR(2),
            zip_code VARCHAR(10),
            customer_type VARCHAR(20),
            total_orders INT,
            total_spent DECIMAL(12,2)
        )
    """))
    for i in range(1, 601):
        conn.execute(text("""INSERT INTO customers (name,email,phone,address,city,state,zip_code,customer_type,total_orders,total_spent)
                         VALUES (:n,:e,:p,:a,:c,:s,:z,:t,:o,:sp)"""),
                    {"n":f"Customer {i}", "e":f"cust{i}@test.com", "p":f"+1-555-{random.randint(1000,9999)}",
                     "a":f"{random.randint(100,999)} St", "c":random.choice(["NYC","LA","Chicago"]),
                     "s":random.choice(["NY","CA","IL"]), "z":f"{random.randint(10000,99999)}",
                     "t":random.choice(["retail","wholesale"]), "o":random.randint(0,50),
                     "sp":round(random.uniform(0,10000),2)})
    conn.commit()
    print("   Inserted 600 customers")
    
    # TABLE 7: SUPPLIERS
    print("\n7/15 Creating SUPPLIERS...")
    conn.execute(text("""
        CREATE TABLE suppliers (
            supplier_id INT PRIMARY KEY AUTO_INCREMENT,
            company_name VARCHAR(200),
            contact_name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            address VARCHAR(200),
            city VARCHAR(50),
            country VARCHAR(50),
            rating DECIMAL(3,1)
        )
    """))
    for i in range(1, 51):
        conn.execute(text("""INSERT INTO suppliers (company_name,contact_name,email,phone,address,city,country,rating)
                         VALUES (:cn,:c,:e,:p,:a,:ci,:co,:r)"""),
                    {"cn":f"Supplier Co {i}", "c":f"Contact {i}", "e":f"supplier{i}@company.com",
                     "p":f"+1-555-{random.randint(1000,9999)}", "a":f"{random.randint(100,999)} Ave",
                     "ci":random.choice(["Seattle","Boston","Miami"]), "co":"USA",
                     "r":round(random.uniform(3,5),1)})
    conn.commit()
    print("   Inserted 50 suppliers")
    
    # TABLE 8: ORDERS
    print("\n8/15 Creating ORDERS...")
    conn.execute(text("""
        CREATE TABLE orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            order_number VARCHAR(50),
            customer_id INT,
            employee_id INT,
            order_date DATETIME,
            status VARCHAR(20),
            subtotal DECIMAL(10,2),
            tax_amount DECIMAL(10,2),
            shipping_cost DECIMAL(10,2),
            total_amount DECIMAL(10,2),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        )
    """))
    for i in range(1, 1001):
        subtotal = round(random.uniform(50,2000),2)
        tax = round(subtotal*0.08,2)
        shipping = round(random.uniform(5,30),2)
        conn.execute(text("""INSERT INTO orders (order_number,customer_id,employee_id,order_date,status,subtotal,
                         tax_amount,shipping_cost,total_amount) VALUES (:on,:c,:e,:od,:s,:sub,:t,:sh,:tot)"""),
                    {"on":f"ORD{i:06d}", "c":random.randint(1,600), "e":random.randint(1,300),
                     "od":datetime.now()-timedelta(days=random.randint(1,180)),
                     "s":random.choice(["pending","shipped","delivered","cancelled"]),
                     "sub":subtotal, "t":tax, "sh":shipping, "tot":subtotal+tax+shipping})
    conn.commit()
    print("   Inserted 1000 orders")
    
    # TABLE 9: ORDER_ITEMS
    print("\n9/15 Creating ORDER_ITEMS...")
    conn.execute(text("""
        CREATE TABLE order_items (
            order_item_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT,
            product_id INT,
            quantity INT,
            unit_price DECIMAL(10,2),
            subtotal DECIMAL(10,2),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """))
    for i in range(1, 2001):
        qty = random.randint(1,5)
        price = round(random.uniform(10,200),2)
        conn.execute(text("""INSERT INTO order_items (order_id,product_id,quantity,unit_price,subtotal)
                         VALUES (:o,:p,:q,:up,:s)"""),
                    {"o":random.randint(1,1000), "p":random.randint(1,800), "q":qty,
                     "up":price, "s":round(qty*price,2)})
    conn.commit()
    print("   Inserted 2000 order items")
    
    # TABLE 10: PAYMENTS
    print("\n10/15 Creating PAYMENTS...")
    conn.execute(text("""
        CREATE TABLE payments (
            payment_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT,
            payment_date DATETIME,
            amount DECIMAL(10,2),
            payment_method VARCHAR(50),
            transaction_id VARCHAR(100),
            status VARCHAR(20),
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    """))
    for i in range(1, 1001):
        conn.execute(text("""INSERT INTO payments (order_id,payment_date,amount,payment_method,transaction_id,status)
                         VALUES (:o,:pd,:a,:pm,:tid,:s)"""),
                    {"o":i, "pd":datetime.now()-timedelta(days=random.randint(1,180)),
                     "a":round(random.uniform(50,2000),2),
                     "pm":random.choice(["Credit Card","PayPal","Cash","Bank Transfer"]),
                     "tid":f"TXN{i:010d}", "s":random.choice(["completed","pending","failed"])})
    conn.commit()
    print("   Inserted 1000 payments")
    
    # TABLE 11: SHIPMENTS
    print("\n11/15 Creating SHIPMENTS...")
    conn.execute(text("""
        CREATE TABLE shipments (
            shipment_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT,
            tracking_number VARCHAR(100),
            carrier VARCHAR(50),
            shipped_date DATETIME,
            delivery_date DATETIME,
            status VARCHAR(20),
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    """))
    for i in range(1, 801):
        ship_date = datetime.now()-timedelta(days=random.randint(1,150))
        conn.execute(text("""INSERT INTO shipments (order_id,tracking_number,carrier,shipped_date,delivery_date,status)
                         VALUES (:o,:t,:c,:sd,:dd,:s)"""),
                    {"o":random.randint(1,1000), "t":f"TRACK{i:010d}",
                     "c":random.choice(["FedEx","UPS","DHL","USPS"]), "sd":ship_date,
                     "dd":ship_date+timedelta(days=random.randint(2,7)) if random.choice([True,False]) else None,
                     "s":random.choice(["in_transit","delivered","returned"])})
    conn.commit()
    print("   Inserted 800 shipments")
    
    # TABLE 12: REVIEWS
    print("\n12/15 Creating REVIEWS...")
    conn.execute(text("""
        CREATE TABLE reviews (
            review_id INT PRIMARY KEY AUTO_INCREMENT,
            product_id INT,
            customer_id INT,
            rating INT,
            title VARCHAR(200),
            comment TEXT,
            review_date DATETIME,
            helpful_count INT,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """))
    for i in range(1, 1201):
        conn.execute(text("""INSERT INTO reviews (product_id,customer_id,rating,title,comment,review_date,helpful_count)
                         VALUES (:p,:c,:r,:t,:co,:rd,:h)"""),
                    {"p":random.randint(1,800), "c":random.randint(1,600), "r":random.randint(1,5),
                     "t":f"Review Title {i}", "co":f"This is review comment {i}",
                     "rd":datetime.now()-timedelta(days=random.randint(1,365)),
                     "h":random.randint(0,100)})
    conn.commit()
    print("   Inserted 1200 reviews")
    
    # TABLE 13: INVENTORY
    print("\n13/15 Creating INVENTORY...")
    conn.execute(text("""
        CREATE TABLE inventory (
            inventory_id INT PRIMARY KEY AUTO_INCREMENT,
            product_id INT,
            warehouse_location VARCHAR(100),
            quantity_available INT,
            quantity_reserved INT,
            reorder_level INT,
            last_stock_date DATETIME,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """))
    for i in range(1, 801):
        conn.execute(text("""INSERT INTO inventory (product_id,warehouse_location,quantity_available,
                         quantity_reserved,reorder_level,last_stock_date) VALUES (:p,:w,:qa,:qr,:r,:l)"""),
                    {"p":i, "w":random.choice(["Warehouse A","Warehouse B","Warehouse C"]),
                     "qa":random.randint(0,500), "qr":random.randint(0,50), "r":50,
                     "l":datetime.now()-timedelta(days=random.randint(1,90))})
    conn.commit()
    print("   Inserted 800 inventory records")
    
    # TABLE 14: SALES
    print("\n14/15 Creating SALES...")
    conn.execute(text("""
        CREATE TABLE sales (
            sale_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT,
            employee_id INT,
            customer_id INT,
            sale_date DATETIME,
            amount DECIMAL(10,2),
            commission DECIMAL(10,2),
            region VARCHAR(50),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """))
    for i in range(1, 1001):
        amount = round(random.uniform(100,3000),2)
        conn.execute(text("""INSERT INTO sales (order_id,employee_id,customer_id,sale_date,amount,commission,region)
                         VALUES (:o,:e,:c,:sd,:a,:com,:r)"""),
                    {"o":i, "e":random.randint(1,300), "c":random.randint(1,600),
                     "sd":datetime.now()-timedelta(days=random.randint(1,180)), "a":amount,
                     "com":round(amount*0.05,2), "r":random.choice(["North","South","East","West"])})
    conn.commit()
    print("   Inserted 1000 sales records")
    
    # TABLE 15: PROMOTIONS
    print("\n15/15 Creating PROMOTIONS...")
    conn.execute(text("""
        CREATE TABLE promotions (
            promotion_id INT PRIMARY KEY AUTO_INCREMENT,
            code VARCHAR(50),
            description TEXT,
            discount_type VARCHAR(20),
            discount_value DECIMAL(10,2),
            start_date DATE,
            end_date DATE,
            max_uses INT,
            times_used INT,
            is_active BOOLEAN
        )
    """))
    for i in range(1, 51):
        start = (datetime.now()-timedelta(days=random.randint(0,90))).date()
        conn.execute(text("""INSERT INTO promotions (code,description,discount_type,discount_value,start_date,
                         end_date,max_uses,times_used,is_active) VALUES (:c,:d,:dt,:dv,:sd,:ed,:m,:t,:a)"""),
                    {"c":f"PROMO{i:03d}", "d":f"Promotion {i} description",
                     "dt":random.choice(["percentage","fixed"]), "dv":round(random.uniform(5,50),2),
                     "sd":start, "ed":start+timedelta(days=random.randint(30,90)),
                     "m":random.randint(100,1000), "t":random.randint(0,500),
                     "a":random.choice([True,False])})
    conn.commit()
    print("   Inserted 50 promotions")
    
    print("\n" + "="*80)
    print("COMPLETE! 15 Tables Created with Data:")
    print("="*80)
    print("  1. users (500 rows)")
    print("  2. departments (10 rows)")
    print("  3. employees (300 rows)")
    print("  4. categories (10 rows)")
    print("  5. products (800 rows)")
    print("  6. customers (600 rows)")
    print("  7. suppliers (50 rows)")
    print("  8. orders (1000 rows)")
    print("  9. order_items (2000 rows)")
    print("  10. payments (1000 rows)")
    print("  11. shipments (800 rows)")
    print("  12. reviews (1200 rows)")
    print("  13. inventory (800 rows)")
    print("  14. sales (1000 rows)")
    print("  15. promotions (50 rows)")
    print("\nTotal Records: 9,120")
    print("="*80)
