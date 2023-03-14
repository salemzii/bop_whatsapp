from fastapi import FastAPI 
from typing import List
import json, requests, os

from pydantic import BaseModel
app = FastAPI()

url = os.getenv("URL")
token = os.getenv("ACCESS_TOKEN")

class Order(BaseModel):
    name: str
    price: str

class Booking(BaseModel):
    orders: List[Order]
    fullname: str
    phone: str


@app.post("/place-order")
async def send_whatsapp_order(booking: Booking):
    order_tup = []
    total_order_price = 0

    for order in booking.orders:
        order_tup.append(order.name)
        total_order_price += float(order.price)

    msg = {
        "messaging_product": "whatsapp",
        "to": "2347014327332",
        "type": "template", 
        "template":{
            "name": "new_table_booking",
            "language": {
            "code": "en_GB"
        },
        "components": [
            {
            "type": "body",
            "parameters": [
                {
                "type": "text",
                "text": ""
                },
                {
                "type": "text",
                "text": ""
                },
                {
                "type": "text",
                "text": ""
                }
            ]
            }
        ]
        }
    }

    msg["template"]["components"][0]["parameters"][0]["text"] = str(tuple(order_tup))
    msg["template"]["components"][0]["parameters"][1]["text"] = booking.fullname
    msg["template"]["components"][0]["parameters"][2]["text"] = str(total_order_price)

    jsonBody = json.dumps(msg)

    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {token}",
    }


    res = requests.post(url=f"{url}", data=jsonBody, headers=headers)

    if res.status_code == 200:
        return {"msg": "message sent successfully"}
    return {"error": "message sending failed"}
