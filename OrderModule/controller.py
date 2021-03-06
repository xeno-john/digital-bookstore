import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from db import orders_database
from view import OrderInput, OrderOutput, Error, Book
import requests
import datetime
from fastapi.middleware.cors import CORSMiddleware
import json

origins = ["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/orders",
          responses={200: {"model": OrderOutput},
                     404: {"model": Error},
                     401: {"model": Error},
                     500: {"model": Error}},
          response_model=OrderOutput
          )
async def check_and_place_order(order_input: OrderInput):
    user_id = order_input.user_id

    if user_id:
        order = {}
        response = requests.post("http://book-module.dev:8000/api/bookcollection/process-order-and-adapt-stocks",
                                 data=order_input.json())
        response_body = response.json()

        if response.status_code == 201:
            status_code = 201
            order["date"] = datetime.datetime.now()
            order["items"] = response_body
            order["status"] = "FINALIZED"
            orders_database[f"client.{user_id}"].insert_one(order)
        else:
            status_code = response.status_code
    else:
        status_code = 401
        # redo with the method in the BookModule
        response_body = {'error_code': 401, 'error_source': 'User not authenticated', 'error_reason': ''}

    return JSONResponse(status_code=status_code, content=response_body)


@app.get("/api/orders/{user_id}")
async def get_orders_for_user(user_id: int):
    orders = []

    for order in orders_database[f"client.{user_id}"].find():
        del order["_id"]
        orders.append({
            "date": str(order["date"]),
            "items": order["items"],
            "status": order["status"]
        })

    return orders


if __name__ == "__main__":
    uvicorn.run("controller:app", host='0.0.0.0', port=8001, reload=True, debug=True)
