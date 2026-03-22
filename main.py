from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import math

app = FastAPI()

class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    item_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=20)
    delivery_address: str = Field(min_length=10)
    order_type: str = 'delivery'  # Default value is 'delivery'

class NewMenuItem(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(gt=0)
    category: str = Field(min_length=2)
    is_available: bool = True  # Default value is True

class CheckoutRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    delivery_address: str = Field(min_length=10)
    
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

cart = []

# ══ HELPER FUNCTIONS ═════════════════════════════════════════════════

def find_menu_item(item_id):
   
    for item in menu:
        if item['id'] == item_id:
            return item
    return None

def calculate_bill(price, quantity, order_type='delivery'):
   
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

def search_menu(keyword):
    keyword_lower = keyword.lower()
    results = [item for item in menu if keyword_lower in item['name'].lower() or keyword_lower in item['category'].lower()]
    return results

def sort_items(items, sort_by='price', order='asc'):
    reverse = order == 'desc'
    return sorted(items, key=lambda x: x[sort_by], reverse=reverse)

def paginate(items, page, limit):
    start = (page - 1) * limit
    end = start + limit
    total = len(items)
    total_pages = math.ceil(total / limit)
    
    paginated_items = items[start:end]
    
    return {
        'items': paginated_items,
        'page': page,
        'limit': limit,
        'total': total,
        'total_pages': total_pages
    }

# ══ HOME ROUTE ENDPOINTS ═════════════════════════════════════════════════════

@app.get('/')
def home():
    return {'message': 'Welcome to Food Delivery App'}


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
    filtered_items = filter_menu_logic(category, max_price, is_available)
    
    return {
        'filtered_items': filtered_items,
        'total_count': len(filtered_items)
    }

@app.get('/menu/search')
def search_menu_items(keyword: str):
    results = search_menu(keyword)
    
    if not results:
        return {
            'message': f'No items found matching "{keyword}"',
            'keyword': keyword,
            'total_found': 0,
            'items': []
        }
    
    return {
        'keyword': keyword,
        'total_found': len(results),
        'items': results
    }

@app.get('/menu/sort')
def sort_menu(sort_by: str = 'price', order: str = 'asc'):
    # Validate sort_by
    valid_sorts = ['price', 'name', 'category']
    if sort_by not in valid_sorts:
        return JSONResponse(
            status_code=400,
            content={'error': f'Invalid sort_by. Must be one of {valid_sorts}'}
        )
    
    # Validate order
    valid_orders = ['asc', 'desc']
    if order not in valid_orders:
        return JSONResponse(
            status_code=400,
            content={'error': f'Invalid order. Must be one of {valid_orders}'}
        )
    
    sorted_items = sort_items(menu, sort_by, order)
    
    return {
        'items': sorted_items,
        'total_count': len(sorted_items),
        'sort_by': sort_by,
        'order': order
    }

@app.get('/menu/page')
def paginate_menu(page: int = 1, limit: int = 3):
    # Validate page
    if page < 1:
        return JSONResponse(
            status_code=400,
            content={'error': 'page must be >= 1'}
        )
    
    # Validate limit
    if limit < 1 or limit > 10:
        return JSONResponse(
            status_code=400,
            content={'error': 'limit must be between 1 and 10'}
        )
    
    pagination_data = paginate(menu, page, limit)
    
    return {
        'page': pagination_data['page'],
        'limit': pagination_data['limit'],
        'total': pagination_data['total'],
        'total_pages': pagination_data['total_pages'],
        'items': pagination_data['items']
    }

@app.get('/menu/browse')
def browse_menu(keyword: str = None, sort_by: str = 'price', order: str = 'asc', page: int = 1, limit: int = 4):
    # Step 1: Filter by keyword if provided
    if keyword:
        filtered_items = search_menu(keyword)
    else:
        filtered_items = menu
    
    # Validate sort_by
    valid_sorts = ['price', 'name', 'category']
    if sort_by not in valid_sorts:
        return JSONResponse(
            status_code=400,
            content={'error': f'Invalid sort_by. Must be one of {valid_sorts}'}
        )
    
    # Validate order
    valid_orders = ['asc', 'desc']
    if order not in valid_orders:
        return JSONResponse(
            status_code=400,
            content={'error': f'Invalid order. Must be one of {valid_orders}'}
        )
    
    # Step 2: Sort
    sorted_items = sort_items(filtered_items, sort_by, order)
    
    # Validate pagination
    if page < 1:
        return JSONResponse(
            status_code=400,
            content={'error': 'page must be >= 1'}
        )
    if limit < 1 or limit > 10:
        return JSONResponse(
            status_code=400,
            content={'error': 'limit must be between 1 and 10'}
        )
    
    # Step 3: Paginate
    pagination_data = paginate(sorted_items, page, limit)
    
    return {
        'search_keyword': keyword,
        'sort_by': sort_by,
        'order': order,
        'page': pagination_data['page'],
        'limit': pagination_data['limit'],
        'total_filtered': len(sorted_items),
        'total_pages': pagination_data['total_pages'],
        'items': pagination_data['items']
    }

@app.get('/menu/{item_id}')
def get_menu_item(item_id: int):
    for item in menu:
        if item['id'] == item_id:
            return item
    return {'error': 'Item not found'}

@app.post('/menu')
def add_menu_item(new_item: NewMenuItem):
    # Check for duplicate name (case-insensitive)
    for existing_item in menu:
        if existing_item['name'].lower() == new_item.name.lower():
            return JSONResponse(
                status_code=400,
                content={'error': 'Item with this name already exists'}
            )
    
    # Assign new id (max existing id + 1)
    new_id = max([item['id'] for item in menu]) + 1 if menu else 1
    
    # Create new menu item
    added_item = {
        'id': new_id,
        'name': new_item.name,
        'price': new_item.price,
        'category': new_item.category,
        'is_available': new_item.is_available
    }
    
    # Append to menu
    menu.append(added_item)
    
    # Return with 201 status code
    return JSONResponse(
        status_code=201,
        content={'message': 'Menu item added successfully', 'item': added_item}
    )

@app.put('/menu/{item_id}')
def update_menu_item(item_id: int, price: int = None, is_available: bool = None):
    # Find the menu item using helper function
    menu_item = find_menu_item(item_id)
    if menu_item is None:
        return JSONResponse(
            status_code=404,
            content={'error': 'Item not found'}
        )
    
    # Update only the fields that are not None
    if price is not None:
        menu_item['price'] = price
    
    if is_available is not None:
        menu_item['is_available'] = is_available
    
    # Return the updated item
    return {
        'message': 'Menu item updated successfully',
        'item': menu_item
    }

@app.delete('/menu/{item_id}')
def delete_menu_item(item_id: int):
    # Find the menu item using helper function
    menu_item = find_menu_item(item_id)
    if menu_item is None:
        return JSONResponse(
            status_code=404,
            content={'error': 'Item not found'}
        )
    
    # Store the deleted item's name before removing
    deleted_name = menu_item['name']
    
    # Remove the item from menu list
    menu.remove(menu_item)
    
    # Return success message with deleted item details
    return {
        'message': 'Menu item deleted successfully',
        'deleted_item': {
            'id': menu_item['id'],
            'name': deleted_name
        }
    }


# ── ORDER ENDPOINTS ───────────────────────────────────────────────

@app.get('/orders')
def get_orders():
    return {
        'orders': orders,
        'total_orders': len(orders)
    }

@app.get('/orders/search')
def search_orders(customer_name: str):
    customer_name_lower = customer_name.lower()
    results = [order for order in orders if customer_name_lower in order['customer_name'].lower()]
    
    if not results:
        return {
            'message': f'No orders found for customer "{customer_name}"',
            'customer_name': customer_name,
            'total_found': 0,
            'orders': []
        }
    
    return {
        'customer_name': customer_name,
        'total_found': len(results),
        'orders': results
    }

@app.get('/orders/sort')
def sort_orders(sort_by: str = 'total_bill', order: str = 'asc'):
    # Validate sort_by
    if sort_by != 'total_bill':
        return JSONResponse(
            status_code=400,
            content={'error': 'sort_by must be "total_bill"'}
        )
    
    # Validate order
    valid_orders = ['asc', 'desc']
    if order not in valid_orders:
        return JSONResponse(
            status_code=400,
            content={'error': f'Invalid order. Must be one of {valid_orders}'}
        )
    
    reverse = order == 'desc'
    sorted_orders = sorted(orders, key=lambda x: x['total_bill'], reverse=reverse)
    
    return {
        'orders': sorted_orders,
        'total_count': len(sorted_orders),
        'sort_by': sort_by,
        'order': order
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


# ── CART ENDPOINTS ────────────────────────────────────────────────

@app.post('/cart/add')
def add_to_cart(item_id: int, quantity: int = 1):
    # Find the menu item
    menu_item = find_menu_item(item_id)
    if menu_item is None:
        return JSONResponse(
            status_code=404,
            content={'error': 'Item not found in menu'}
        )
    
    # Check if item is available
    if not menu_item['is_available']:
        return JSONResponse(
            status_code=400,
            content={'error': 'Item is not available'}
        )
    
    # Check if item already in cart
    for cart_item in cart:
        if cart_item['item_id'] == item_id:
            # Update quantity instead of adding duplicate
            cart_item['quantity'] += quantity
            cart_item['subtotal'] = cart_item['price'] * cart_item['quantity']
            return {
                'message': 'Item quantity updated in cart',
                'cart_item': cart_item
            }
    
    # Add new item to cart
    new_cart_item = {
        'item_id': item_id,
        'name': menu_item['name'],
        'price': menu_item['price'],
        'quantity': quantity,
        'subtotal': menu_item['price'] * quantity,
        'category': menu_item['category']
    }
    
    cart.append(new_cart_item)
    
    return {
        'message': 'Item added to cart',
        'cart_item': new_cart_item
    }

@app.get('/cart')
def get_cart():
    """
    Get all items in cart with grand total.
    """
    grand_total = sum(item['subtotal'] for item in cart)
    
    return {
        'cart_items': cart,
        'total_items': len(cart),
        'grand_total': grand_total
    }

@app.delete('/cart/{item_id}')
def remove_from_cart(item_id: int):
    global cart
    
    # Find and remove the item from cart
    for i, cart_item in enumerate(cart):
        if cart_item['item_id'] == item_id:
            removed_item = cart.pop(i)
            return {
                'message': 'Item removed from cart',
                'removed_item': removed_item
            }
    
    # Item not found in cart
    return JSONResponse(
        status_code=404,
        content={'error': 'Item not found in cart'}
    )

@app.post('/cart/checkout')
def checkout(checkout_request: CheckoutRequest):
    global order_counter, cart
    
    # Reject if cart is empty
    if not cart:
        return JSONResponse(
            status_code=400,
            content={'error': 'Cart is empty. Add items before checkout.'}
        )
    
    # Calculate grand total from cart
    grand_total = sum(item['subtotal'] for item in cart)
    
    # Loop through cart items and create orders
    placed_orders = []
    
    for cart_item in cart:
        new_order = {
            'order_id': order_counter,
            'customer_name': checkout_request.customer_name,
            'item_id': cart_item['item_id'],
            'item_name': cart_item['name'],
            'quantity': cart_item['quantity'],
            'price_per_unit': cart_item['price'],
            'subtotal': cart_item['subtotal'],
            'total_bill': cart_item['subtotal'],
            'delivery_address': checkout_request.delivery_address,
            'order_type': 'delivery'
        }
        
        orders.append(new_order)
        placed_orders.append(new_order)
        order_counter += 1
    
    # Clear the cart after checkout
    cart = []
    
    # Return placed orders with grand total and 201 status
    return JSONResponse(
        status_code=201,
        content={
            'message': 'Checkout successful',
            'placed_orders': placed_orders,
            'total_orders_placed': len(placed_orders),
            'grand_total': grand_total
        }
    )
