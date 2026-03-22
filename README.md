# Food Delivery App API

A simple and fast REST API for a food delivery application built with **FastAPI**. This app allows customers to browse menu items, manage their cart, place orders, and search for food items.

---

## 📋 How This Project Works

### **Three Main Features:**

1. **📱 Menu Management** - Browse, search, sort, and filter food items
2. **🛒 Shopping Cart** - Add items to cart and manage quantities
3. **📦 Orders** - Place orders and track them

---

## ✨ Key Features

### **🔍 Search & Browse**
- Search for menu items by **name** or **category** (case-insensitive)
- Browse menu with **keyword search, sorting, and pagination** in one call

### **📊 Sort & Filter**
- Sort items by: **price**, **name**, or **category**
- Sort in: **ascending (asc)** or **descending (desc)** order
- Filter by: **category**, **max price**, or **availability**

### **📄 Pagination**
- View items page by page with **custom page size**
- Get total pages and total items count

### **🛍️ Shopping Cart**
- Add items to cart (prevents duplicate entries, updates quantity instead)
- View cart with **grand total** calculation
- Remove specific items from cart
- **One-click checkout** - creates orders for all cart items

### **✅ Order Management**
- Place orders with item details and delivery address
- **Delivery charge:** ₹30 for delivery, ₹0 for pickup
- Search orders by **customer name**
- Sort orders by **total bill amount**
- Get order history with all details

### **🔧 Add/Update/Delete Menu Items**
- Add new menu items to the system
- Update item price and availability
- Delete items from menu
- Automatic duplicate name prevention (case-insensitive)

---

## 🚀 Installation & Setup

### **1. Prerequisites**
- Python 3.8+
- Virtual environment (recommended)

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run the Server**
```bash
uvicorn main:app --reload
```

The API will start at: **`http://127.0.0.1:8000`**

### **4. Open Swagger Documentation**
Visit: **`http://127.0.0.1:8000/docs`**

---

## 📡 API Endpoints

### **MENU ENDPOINTS**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/menu` | Get all menu items |
| GET | `/menu/summary` | Get menu summary (total, available, categories) |
| GET | `/menu/{item_id}` | Get specific item details |
| GET | `/menu/search?keyword=pizza` | Search items by name/category |
| GET | `/menu/sort?sort_by=price&order=asc` | Sort items by price/name/category |
| GET | `/menu/filter?category=Pizza&max_price=100` | Filter items by category/price |
| GET | `/menu/page?page=1&limit=3` | Paginate menu items |
| GET | `/menu/browse?keyword=pizza&sort_by=price&order=asc&page=1` | Smart browse (search + sort + paginate) |
| POST | `/menu` | Add new menu item |
| PUT | `/menu/{item_id}` | Update item price/availability |
| DELETE | `/menu/{item_id}` | Delete menu item |

### **ORDER ENDPOINTS**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/orders` | Get all orders |
| GET | `/orders/search?customer_name=John` | Search orders by customer name |
| GET | `/orders/sort?sort_by=total_bill&order=desc` | Sort orders by bill amount |
| POST | `/orders` | Create new order |

### **CART ENDPOINTS**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/cart/add?item_id=1&quantity=2` | Add item to cart |
| GET | `/cart` | View cart items and grand total |
| DELETE | `/cart/{item_id}` | Remove item from cart |
| POST | `/cart/checkout` | Checkout and place order(s) |

---

## 💡 Example Usage

### **1. Search for Pizza**
```
GET /menu/search?keyword=pizza
```
Returns: All items with "pizza" in name or category

### **2. Sort by Price (Low to High)**
```
GET /menu/sort?sort_by=price&order=asc
```
Returns: All items sorted by price in ascending order

### **3. Add Item to Cart**
```
POST /cart/add?item_id=1&quantity=2
```
Adds 2 Margherita Pizzas to cart

### **4. View Cart**
```
GET /cart
```
Shows all cart items with **grand total**

### **5. Checkout**
```
POST /cart/checkout
Body: {
  "customer_name": "John Doe",
  "delivery_address": "123 Main Street, City"
}
```
Creates order(s) and clears cart

---

## 🔍 Testing in Swagger

1. Open **`http://127.0.0.1:8000/docs`**
2. Click on any endpoint (e.g., GET `/menu/sort`)
3. Click **"Try it out"** button
4. Set parameters:
   - `sort_by` = price
   - `order` = asc
5. Click **"Execute"** button
6. See the response with sorted items

---

## 📦 Sample Menu Items

| ID | Name | Price | Category | Available |
|---|---|---|---|---|
| 1 | Margherita Pizza | ₹80.99 | Pizza | ✅ |
| 2 | Pepperoni Pizza | ₹100.99 | Pizza | ✅ |
| 3 | Classic Burger | ₹177.99 | Burger | ✅ |
| 4 | Cheese Burger | ₹150.99 | Burger | ❌ |
| 5 | Coca Cola | ₹69.99 | Drink | ✅ |
| 6 | Chocolate Cake | ₹35.99 | Dessert | ✅ |

---

## ⚙️ Technologies Used

- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Python 3.8+** - Programming language

---

## 📝 Notes

- All prices are in **Indian Rupees (₹)**
- Delivery charge: **₹30** for delivery orders, **₹0** for pickup
- Cart persists during the session (clears on checkout)
- Search is **case-insensitive** across all endpoints
- Maximum 20 items per order (quantity limit)

---

## 🎯 Future Enhancements

- Database integration (PostgreSQL/MongoDB)
- User authentication & authorization
- Payment gateway integration
- Real-time order tracking
- Email notifications
- Admin dashboard

---

## 👤 Support

For issues or questions, please check the Swagger documentation at `/docs`

**Email for queries:** nandishgs60@gmail.com

Happy ordering! 🍕🍔🍰
