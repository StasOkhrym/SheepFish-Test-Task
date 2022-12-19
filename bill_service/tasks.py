from SheepFish_test_task.celery import app


def get_order_number_and_dict(check):
    order_dict = {}
    order_dict.update(check.order)
    order_number = order_dict.pop("order_number")
    return order_number, order_dict


def get_order_number_dict_and_price(check):
    order_number, order = get_order_number_and_dict(check.order)
    total_price = 0
    for item in order.values():
        total_price += int(item["price"])
    return order_number, total_price, order


@app.task
def render_pdf_kitchen(check):
    order_number, order = get_order_number_and_dict(check)


@app.task
def render_pdf_client(check):
    order_number, total_price, order = get_order_number_dict_and_price(check)
