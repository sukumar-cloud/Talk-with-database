# 📝 MongoDB Query Examples

Try these natural language queries in the MongoDB Query page!

---

## 🔍 **FIND Queries (Search/Retrieve)**

### Basic Find:
```
Find all users
Show all customers
Get all products
List all documents
```

### Conditional Find:
```
Find users with age greater than 25
Get customers where status is active
Show products with price less than 100
Find orders where amount is greater than 1000
Search documents where name is John
```

### Multiple Conditions:
```
Find active users with age greater than 18
Get customers where status is active and country is USA
Show products with price between 50 and 200
```

### Text Search:
```
Search for users whose name contains "john"
Find customers with email ending in @gmail.com
Get products where name starts with "laptop"
```

---

## ➕ **INSERT Queries (Add/Create)**

```
Insert a new user
Add a new customer
Create a new document
Add a new product to inventory
Insert user with name John and age 25
```

**What happens:** System will create a sample document to insert

---

## ✏️ **UPDATE Queries (Modify/Change)**

```
Update user names
Modify customer status to active
Change product prices
Update all inactive records
Set status to completed for all orders
```

**What happens:** System will update matching documents

---

## 🗑️ **DELETE Queries (Remove)**

```
Delete inactive users
Remove old records
Delete customers where status is cancelled
Remove documents older than 30 days
```

**⚠️ Warning:** Be careful with delete operations!

---

## 📊 **COUNT Queries (Statistics)**

```
Count total users
How many customers are active
Count products with price greater than 100
Total number of orders today
```

---

## 🎯 **Comparison Operators**

### Greater Than:
```
Find users with age greater than 18
Get products with price greater than 50
Show orders with amount greater than 1000
```

### Less Than:
```
Find products with price less than 100
Get users with age less than 30
Show orders with quantity less than 10
```

### Equal To:
```
Find users where status equals active
Get customers where country is USA
Show products where category is electronics
```

### Not Equal To:
```
Find users where status is not inactive
Get products where price is not zero
Show orders where status is not cancelled
```

---

## 🔢 **Range Queries**

```
Find users with age between 18 and 65
Get products with price between 100 and 500
Show orders from last 7 days
Find customers who joined this month
```

---

## 📅 **Date/Time Queries**

```
Find users created today
Get orders from last week
Show customers who joined this month
Find documents updated yesterday
Get records from last 30 days
```

---

## 🎨 **Advanced Queries**

### Existence Check:
```
Find users where email exists
Get documents where phone number is missing
Show records where address is defined
```

### Null Check:
```
Find users where status is null
Get documents where age is not null
```

### Array Operations:
```
Find users with multiple addresses
Get products in multiple categories
Show orders with more than 3 items
```

---

## 💡 **Example Workflow**

### 1. Start Simple:
```
Find all users
```

### 2. Add Conditions:
```
Find active users
```

### 3. Multiple Conditions:
```
Find active users with age greater than 25
```

### 4. Complex Query:
```
Find active premium users who joined in the last month with age between 18 and 65
```

---

## 🎯 **Testing Different Operations**

### READ (Find):
```
Show all customers
```

### CREATE (Insert):
```
Add a new user
```

### UPDATE:
```
Update customer status to active
```

### DELETE:
```
Delete inactive records
```

### COUNT:
```
Count total users
```

---

## 📋 **Best Practices**

### ✅ DO:
- Use clear, descriptive language
- Specify conditions clearly
- Mention collection names when possible
- Use comparison words (greater than, less than, equals)

### ❌ DON'T:
- Use vague terms like "some" or "maybe"
- Mix multiple operations in one query
- Forget to specify what you're searching for

---

## 🔥 **Quick Test Queries**

Copy these to test immediately:

```
Find all active users
Get customers with age greater than 25
Show products with price less than 100
Find orders where status is pending
Count total documents
Search for users whose name contains john
Get records from last 7 days
Find documents where email exists
Show users with age between 18 and 65
Delete inactive records
```

---

## 🎊 **Your Turn!**

Try these queries in the MongoDB Query page:
- http://localhost:5173/mongodb-query

The system will:
1. ✅ Parse your natural language
2. ✅ Detect the operation (find, insert, update, delete, count)
3. ✅ Extract entities (collections, fields, conditions)
4. ✅ Validate for security (NoSQL injection)
5. ✅ Execute safely on MongoDB

---

**Happy Querying! 🚀**
