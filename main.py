from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    item_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=20)
    delivery_address: str = Field(min_length=10)
    order_type: str = 'delivery'  # Default value is 'delivery'
    
# ══ DATA ══════════════════════════════════════════════════════════

menu = [
    {'id': 1, 'name': 'Margherita Pizza', 'price': 80.99, 'category': 'Pizza', 'is_available': True},
    {'id': 2, 'name': 'Pepperoni Pizza', 'price': 100.99, 'category': 'Pizza', 'is_available': True},
    {'id': 3, 'name': 'Classic Burger', 'price': 177.99, 'category': 'Burger', 'is_available': True},
    {'id': 4, 'name': 'Cheese Burger', 'price': 150.99, 'category': 'Burger', 'is_available': False},
    {'id': 5, 'name': 'Coca Cola', 'price': 69.99, 'category': 'Drink', 'is_available': True},
    {'id': 6, 'name': 'Chocolate Cake', 'price': 35.99, 'category': 'Dessert', 'is_available': True}
]

orders = []
order_counter = 1

# ══ HELPER FUNCTIONS ═════════════════════════════════════════════════

def find_menu_item(item_id):
   
    for item in menu:
        if item['id'] == item_id:
            return item
    return None

def calculate_bill(price, quantity, order_type='delivery'):
    """
    Calculate the total bill amount.
    Returns price * quantity + delivery charge (₹30 for delivery, ₹0 for pickup).
    """
    subtotal = price * quantity
    delivery_charge = 30 if order_type == 'delivery' else 0
    return subtotal + delivery_charge

def filter_menu_logic(category=None, max_price=None, is_available=None):
   
    filtered_items = menu
    
    # Filter by category if provided
    if category is not None:
        filtered_items = [item for item in filtered_items if item['category'] == category]
    
    # Filter by max_price if provided
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item['price'] <= max_price]
    
    # Filter by is_available if provided
    if is_available is not None:
        filtered_items = [item for item in filtered_items if item['is_available'] == is_available]
    
    return filtered_items

# ══ HOME ROUTE ENDPOINTS ═════════════════════════════════════════════════════

@app.get('/')
def home():
    return {'message': 'Welcome to QuickBite Food Delivery'}


# ── MENU ENDPOINTS ────────────────────────────────────────────────

@app.get('/menu')
def get_menu():
    return {
        'items': menu,
        'total_count': len(menu)
    }

@app.get('/menu/summary')
def get_menu_summary():
    available = sum(1 for item in menu if item['is_available'])
    unavailable = len(menu) - available
    categories = list(set(item['category'] for item in menu))
    
    return {
        'total_items': len(menu),
        'available_items': available,
        'unavailable_items': unavailable,
        'categories': categories
    }

@app.get('/menu/filter')
def filter_menu(category: str = None, max_price: int = None, is_available: bool = None):
    """
    Filter menu items by optional parameters.
    Query params: category (str), max_price (int), is_available (bool)
    """
    filtered_items = filter_menu_logic(category, max_price, is_available)
    
    return {
        'filtered_items': filtered_items,
        'total_count': len(filtered_items)
    }

@app.get('/menu/{item_id}')
def get_menu_item(item_id: int):
    for item in menu:
        if item['id'] == item_id:
            return item
    return {'error': 'Item not found'}


# ── ORDER ENDPOINTS ───────────────────────────────────────────────

@app.get('/orders')
def get_orders():
    return {
        'orders': orders,
        'total_orders': len(orders)
    }

@app.post('/orders')
def create_order(order_request: OrderRequest):
    global order_counter
    
    # Check if menu item exists using helper function
    menu_item = find_menu_item(order_request.item_id)
    if menu_item is None:
        return {'error': 'Item not found in menu'}
    
    # Check if item is available
    if not menu_item['is_available']:
        return {'error': 'Item is not available at the moment'}
    
    # Calculate bill using helper function with order_type
    bill_amount = calculate_bill(menu_item['price'], order_request.quantity, order_request.order_type)
    
    # Create order dict
    new_order = {
        'order_id': order_counter,
        'customer_name': order_request.customer_name,
        'item_id': order_request.item_id,
        'item_name': menu_item['name'],
        'quantity': order_request.quantity,
        'price_per_unit': menu_item['price'],
        'order_type': order_request.order_type,
        'delivery_charge': 30 if order_request.order_type == 'delivery' else 0,
        'total_bill': bill_amount,
        'delivery_address': order_request.delivery_address
    }
    
    # Append to orders and increment counter
    orders.append(new_order)
    order_counter += 1
    
    return {'message': 'Order placed successfully', 'order': new_order}
