import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


RANDOM_SEED = 42

RAW_DIR = Path("data/raw")

COUNTRIES = [
    "Tunisia",
    "France",
    "Germany",
    "United Kingdom",
    "Italy",
]

DEVICE_TYPES = [
    "iOS",
    "Android",
    "Web",
]

EVENT_TYPES = [
    "app_open",
    "product_view",
    "search",
    "add_to_cart",
    "purchase",
    "logout",
]

PRODUCTS = [
    (
        "P001",
        "Wireless Earbuds",
        "Audio",
        79.99,
    ),
    (
        "P002",
        "Smart Watch",
        "Wearables",
        149.99,
    ),
    (
        "P003",
        "Phone Case",
        "Accessories",
        24.99,
    ),
    (
        "P004",
        "USB-C Charger",
        "Accessories",
        34.99,
    ),
    (
        "P005",
        "Bluetooth Speaker",
        "Audio",
        89.99,
    ),
]

START_DATE = datetime(2026, 1, 1)


def generate_customers():
    customers = []

    for number in range(1, 1001):
        signup_date = START_DATE + timedelta(
            days=random.randint(0, 180)
        )

        customers.append(
            {
                "customer_id": f"C{number:05d}",
                "country": random.choice(COUNTRIES),
                "signup_date": signup_date.date().isoformat(),
                "device_type": random.choice(DEVICE_TYPES),
            }
        )

    output_file = RAW_DIR / "customers.csv"

    with output_file.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "customer_id",
                "country",
                "signup_date",
                "device_type",
            ],
        )

        writer.writeheader()
        writer.writerows(customers)

    return customers


def generate_products():
    output_file = RAW_DIR / "products.csv"

    with output_file.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "product_id",
                "product_name",
                "category",
                "list_price",
            ],
        )

        writer.writeheader()

        for product_id, name, category, price in PRODUCTS:
            writer.writerow(
                {
                    "product_id": product_id,
                    "product_name": name,
                    "category": category,
                    "list_price": price,
                }
            )


def generate_events(customers):
    events = []

    for number in range(1, 10001):
        customer = random.choice(customers)

        timestamp = START_DATE + timedelta(
            days=random.randint(0, 180),
            minutes=random.randint(0, 1439),
        )

        events.append(
            {
                "event_id": f"E{number:06d}",
                "customer_id": customer["customer_id"],
                "event_type": random.choice(EVENT_TYPES),
                "event_timestamp": timestamp.isoformat(),
                "platform": customer["device_type"],
                "session_id": (
                    f"S{random.randint(1, 3000):05d}"
                ),
            }
        )

    output_file = RAW_DIR / "events.json"

    with output_file.open("w") as file:
        json.dump(events, file, indent=2)


def generate_orders(customers):
    orders = []

    for number in range(1, 2501):
        customer = random.choice(customers)

        timestamp = START_DATE + timedelta(
            days=random.randint(0, 180),
            minutes=random.randint(0, 1439),
        )

        product_id, _, _, list_price = random.choice(
            PRODUCTS
        )

        # Simulate prices varying around the catalog price.
        unit_price = round(
            list_price * random.uniform(0.9, 1.1),
            2,
        )

        orders.append(
            {
                "order_id": f"O{number:06d}",
                "customer_id": customer["customer_id"],
                "order_timestamp": timestamp.isoformat(),
                "product_id": product_id,
                "quantity": random.randint(1, 4),
                "unit_price": unit_price,
                "currency": "GBP",
            }
        )

    output_file = RAW_DIR / "orders.csv"

    with output_file.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "order_id",
                "customer_id",
                "order_timestamp",
                "product_id",
                "quantity",
                "unit_price",
                "currency",
            ],
        )

        writer.writeheader()
        writer.writerows(orders)


def main():
    random.seed(RANDOM_SEED)

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    customers = generate_customers()

    generate_products()

    generate_events(customers)

    generate_orders(customers)

    print(
        "Synthetic source data generated successfully."
    )


if __name__ == "__main__":
    main()