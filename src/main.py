from router.get_information import get_order_status, get_shipping_issue, check_customer_id, check_product_name, get_list_product, get_extra_information, get_delivery_time
import os
import sqlite3

RED_COLOR = "\033[91m"
GREEN_COLOR = "\033[92m"
YELLOW_COLOR = "\033[93m"
WHILE_COLOR = "\033[90m"
def get_customer_id() -> str:
    """
    Get customer ID from input
    """
    while True:
        print(f"{YELLOW_COLOR}Please input your customer ID{WHILE_COLOR}:")
        customer_id = input()
        if not check_customer_id(conn, customer_id):
            print(f"{RED_COLOR}Customer ID is invalid{WHILE_COLOR}")
            continue
        break
    print(f"{YELLOW_COLOR}Here is your list of product you order:{WHILE_COLOR}")
    products = get_list_product(conn, customer_id)
    for product in products:
        print(product[0])
    return customer_id

def get_product_name() -> str:
    """
    Get product name from input
    """
    while True:
        print(f"{YELLOW_COLOR}Please input your product name (You can input \"All\" for all product):{WHILE_COLOR}")
        product_name = input()
        if not check_product_name(conn, product_name):
            print(f"{RED_COLOR}You don't have this product in your order{WHILE_COLOR}")
            continue
        break
    return product_name

def app(tokenizer, model, conn: sqlite3.Connection) -> None:
    """
    Run app
    """
    customer_id = get_customer_id()
    product_name = get_product_name()

    while True: 
        question = input(f"{YELLOW_COLOR}What is your question?:{WHILE_COLOR} ")
        if question == "\exit":
            break
        if question == "\cproduct":
            print(f"{YELLOW_COLOR}Here is your list of product you order:{WHILE_COLOR}")
            products = get_list_product(conn, customer_id)
            for product in products:
                print(product[0])
            product_name = get_product_name()
            continue
        if question == "\ccustomer":
            customer_id = get_customer_id()
            product_name = get_product_name()
            continue
        label = predict(question, model, tokenizer)
        print(f"{YELLOW_COLOR}Classify: {label}{WHILE_COLOR}")
        if label == 'Order Status':
            status = get_order_status(conn, customer_id, product_name)
            for s in status:
                response = f"{GREEN_COLOR}Your product {s[0]} has status: {s[1]}{WHILE_COLOR}"
                print(response)
            
        elif label == 'Shipping Issues':
            issue = get_shipping_issue(conn, customer_id, product_name)
            if issue == []:
                print(f"{YELLOW_COLOR}It seems like you don't have any shipping issue, don't worry, here is your order status and delivery time{WHILE_COLOR}")
                extra_info = get_extra_information(conn, customer_id, product_name)
                for info in extra_info:
                    print(f"{GREEN_COLOR}Your product {info[0]} has status: {info[1]} and estimated delivery time is: {info[2]}{WHILE_COLOR}")
        
            else:
                for i in issue:
                    response = f"{RED_COLOR}Your product {i[0]} got issue or canceled, here is the reason: {i[1]}{WHILE_COLOR}"
                    print(response)
        elif label == 'Delivery Time':
            delivery_time = get_delivery_time(conn, customer_id, product_name)
            for d in delivery_time:
                response = f"{GREEN_COLOR}Your product {d[0]} has estimated delivery time: {d[1]}{WHILE_COLOR}"
                print(response)
        else:
            print(f"{YELLOW_COLOR}Sorry, It look like your question is out of domain, I cannot help with that.{WHILE_COLOR}")


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(current_path, "data\\e_commerce.db")
    model_path = os.path.join(current_path, "models\\checkpoint-252")
    tokenizer_path = os.path.join(current_path, "models\\distillbert-tokenizer")
    print("Please wait a second for loading the model")
    try:
        from models.model_predict import init, predict
        tokenizer, model = init(model_path, tokenizer_path)
        conn = sqlite3.connect(database_path)
        print("Model and database are loaded successfully")
        app(tokenizer, model, conn)
    except Exception as e:
        print(e)
        
    
