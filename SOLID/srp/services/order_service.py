orders_db = []


def create_order(order_data):

    total = calculate_total(order_data["items"])

    validate_order_total(total)

    total = apply_discount(total)

    order = build_order(order_data, total)

    save_order(order)

    log_vip_order(order)

    return order


def calculate_total(items):
    return sum(
        item["price"] * item["quantity"] for item in items
    )


def validate_order_total(total):
    if total <= 0:
        raise ValueError("Invalid total")


def apply_discount(total):

    if total > 1000:
        return total - (total * 0.1)

    return total


def build_order(data, total):

    order = {
        "id": max((order["id"] for order in orders_db), default=0) + 1,
        "customer_id": data["customer_id"],
        "items": data["items"],
        "total": total
    }

    return order


def save_order(order):
    orders_db.append(order)


def log_vip_order(order):

    if order["total"] > 500:

        with open("vip_orders.log", "a") as f:
            f.write(
                f"VIP order: {order['id']} - ${order['total']}\n"
            )

#================================= update orders ===================================

def update_order(order_id, new_status):

    order = search_order(order_id)

    validate_status(new_status)

    old_status = order.get("status", "pending")

    order = change_status(order, new_status)

    notify_customer(order)

    save_status_change_log(
        order_id,
        old_status,
        new_status
    )

    return order


class OrderNotFoundError(Exception):
    pass

def search_order(order_id):

    for order in orders_db:

        if order["id"] == order_id:
            return order

    raise OrderNotFoundError("Order not found")


def validate_status(new_status):

    valid_statuses = [
        "pending",
        "shipped",
        "delivered",
        "cancelled"
    ]

    if new_status not in valid_statuses:
        raise ValueError("Invalid status")


def change_status(order, new_status):

    order["status"] = new_status

    return order


def notify_customer(order):

    print(
        f"Notifying customer {order['customer_id']}: "
        f"order {order['id']} is now {order['status']}"
    )


def save_status_change_log(order_id, old_status, new_status):

    with open("status_changes.log", "a") as f:

        f.write(
            f"Order {order_id}: "
            f"{old_status} -> {new_status}\n"
        )