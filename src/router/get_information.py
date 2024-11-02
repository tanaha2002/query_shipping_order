import sqlite3

def check_customer_id(conn: sqlite3.Connection, customer_id: str) -> bool:
    """
    Check if the customer id is valid
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT customerid FROM orders WHERE customerid = '{customer_id}'")
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True

def check_product_name(conn: sqlite3.Connection, product_name: str) -> bool:
    """
    Check if the product name is valid
    """
    if product_name == "All":
        return True
    cursor = conn.cursor()
    cursor.execute(f"SELECT product_name FROM orders WHERE product_name = '{product_name}'")
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True

def get_list_product(conn: sqlite3.Connection, customer_id: str) -> list:
    """
    Get the list of product for that customer
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT product_name FROM orders WHERE customerid = '{customer_id}'")
    products = cursor.fetchall()
    return products

def get_order_status(conn: sqlite3.Connection, customer_id: str, product_name: str) -> list:
    """
    Get the status of the order
    """
    cursor = conn.cursor()
    if product_name == "All":
        cursor.execute(f"SELECT product_name,order_status FROM orders WHERE customerid = '{customer_id}'")
    else:
        cursor.execute(f"SELECT product_name, order_status FROM orders WHERE customerid = '{customer_id}' AND product_name like '{product_name}'")
    status = cursor.fetchall()
    return status

def get_shipping_issue(conn: sqlite3.Connection, customer_id: str, product_name: str) -> list:
    """
    Get the shipping issue for customer
    """
    cursor = conn.cursor()
    if product_name == "All":
        cursor.execute(f"SELECT product_name, reason FROM orders WHERE customerid = '{customer_id}' AND (order_status = 'Canceled' or order_status = 'Failed')")
    else:
        cursor.execute(f"SELECT product_name, reason FROM orders WHERE customerid = '{customer_id}' AND product_name = '{product_name}' AND (order_status = 'Canceled' or order_status = 'Failed')")
    issue = cursor.fetchall()
    return issue

def get_extra_information(conn: sqlite3.Connection, customer_id: str, product_name: str) -> list:
    """
    Get extra information for customer
    """
    cursor = conn.cursor()
    if product_name == "All":
        cursor.execute(f"SELECT product_name, order_status, shipping_date_estimate FROM orders WHERE customerid = '{customer_id}'")
    else:
        cursor.execute(f"SELECT product_name, order_status, shipping_date_estimate FROM orders WHERE customerid = '{customer_id}' AND product_name = '{product_name}'")
    extra = cursor.fetchall()
    return extra

def get_delivery_time(conn: sqlite3.Connection, customer_id: str, product_name: str) -> list:
    """
    Get the delivery time for customer
    """
    cursor = conn.cursor()
    if product_name == "All":
        cursor.execute(f"SELECT product_name, shipping_date_estimate FROM orders WHERE customerid = '{customer_id}' AND (order_status != 'Canceled' OR order_status != 'Failed')")
    else:
        cursor.execute(f"SELECT product_name, order_status, shipping_date_estimate, delivery_date_estimate FROM orders WHERE customerid = '{customer_id}' AND product_name = '{product_name}' AND (order_status != 'Canceled' OR order_status != 'Failed')")
    delivery = cursor.fetchall()
    return delivery
    