import requests
import json

url = "https://cl.milesawayy.com/api/Shipments/create_shipment_v2"

payload = json.dumps({
  "cust_name": "Parshu",
  "order_num": "DUMMY_20102875",
  "cust_mobile": "9869118993",
  "cust_alt_mobile": "",
  "cust_email": "",
  "cust_pincode": "400077",
  "cust_city": "Mumbai",
  "cust_state": "MH",
  "cust_add": "1216, E Wing, Advikalayam Apartments, Ghatpoar East, Mumbai",
  "prod_name": "Muslin Kids Cloth",
  "prod_quantity": "1",
  "prod_mrp": "575",
  "prod_wt": "500",
  "prod_leng": "10",
  "prod_height": "10",
  "prod_width": "10",
  "ship_mode": "0",
  "pickup_loc": {
    "pickup_name": "Mumbai",
    "pickup_cont_name": "John",
    "pickup_cont_num": "1236554778",
    "pickup_cont_email": "cont@email.com",
    "pickup_city": "Mumbai",
    "pickup_state": "MH",
    "pickup_pincode": "400022",
    "pickup_add": "Shop no.1, Building name, near landmark name, area name, Mumbai"
  },
  "return_loc": {
    "return_name": "Mumbai",
    "return_cont_name": "John",
    "return_cont_num": "1236554778",
    "return_cont_email": "cont@email.com",
    "return_city": "Mumbai",
    "return_state": "MH",
    "return_pincode": "400022",
    "return_add": "Shop no.1, Building name, near landmark name, area name, Mumbai"
  }
})
headers = {
  'token': '64b6f0cfa0785196d21a9ccd088cee9bc3',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
