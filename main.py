"""
Habit Tracker
"""

import argparse
import os
from datetime import datetime

import requests

USERNAME = os.environ.get("USERNAME")
TOKEN = os.environ.get("TOKEN")
PIXELA_ENDPOINT = "https://pixe.la/v1/users"
GRAPH_ID = "graph1"
GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"


def args_parser():
    """Parse arguments"""
    parser = argparse.ArgumentParser(description="Habit Tracker")

    parser.add_argument(
        "--create_user",
        action="store_true",
        help="Create a new user on Pixela"
    )
    parser.add_argument(
        "--create_graph",
        action="store_true",
        help="Create a new graph on Pixela"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date in YYYYMMDD format"
    )
    parser.add_argument(
        "--quantity",
        type=int, help="Quantity"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete a pixel"
    )

    return parser.parse_args()


def create_user():
    """Create a new user on Pixela"""

    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }

    response = requests.post(
        url=PIXELA_ENDPOINT,
        json=user_params
    )

    print(response.text)


def create_graph():
    """Create a new graph on Pixela"""
    graph_config = {
        "id": GRAPH_ID,
        "name": "Learning Stuff",
        "unit": "minutes",
        "type": "int",
        "color": "momiji",
    }

    headers = {"X-USER-TOKEN": TOKEN, }

    response = requests.post(
        url=GRAPH_ENDPOINT,
        json=graph_config,
        headers=headers
    )

    print(response.text)


def add_pixel(quantity=0):
    """Add a new pixel to the graph"""
    pixel_endpoint = f"{GRAPH_ENDPOINT}/{GRAPH_ID}"
    today = datetime.now()
    today = today.strftime("%Y%m%d")
    pixel_config = {
        "date": today,
        "quantity": str(quantity),
    }
    headers = {"X-USER-TOKEN": TOKEN, }

    response = requests.post(
        url=pixel_endpoint,
        json=pixel_config,
        headers=headers
    )
    print(response.text)


def update_pixel(date, quantity):
    """Update a pixel on the graph"""
    pixel_endpoint = f"{GRAPH_ENDPOINT}/{GRAPH_ID}/{date}"
    pixel_config = {
        "date": date,
        "quantity": str(quantity),
    }
    headers = {"X-USER-TOKEN": TOKEN, }

    response = requests.put(
        url=pixel_endpoint,
        json=pixel_config,
        headers=headers
    )

    print(response.text)


def delete_pixel(date):
    """Delete a pixel from the graph"""
    pixel_endpoint = f"{GRAPH_ENDPOINT}/{GRAPH_ID}/{date}"
    headers = {"X-USER-TOKEN": TOKEN, }

    response = requests.delete(
        url=pixel_endpoint,
        headers=headers
    )

    print(response.text)


def main():
    args = args_parser()
    if args.create_user:
        create_user()
    elif args.create_graph:
        create_graph()
    elif args.quantity:
        add_pixel(args.quantity)
    elif args.date and args.quantity:
        update_pixel(args.date, args.quantity)
    elif args.delete and args.date:
        delete_pixel(args.date)
    else:
        args_parser().print_help()


if __name__ == "__main__":
    main()
