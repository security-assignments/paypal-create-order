from paypal_client import PayPalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest
import hashlib
import os

class CreateOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """ This is the sample function to create an order. It uses the
    JSON body returned by buildRequestBody() to create an order."""

  def create_order(self, gcp_email, debug=False, amount="50.00"):
    request = OrdersCreateRequest()
    request.prefer('return=representation')
    #3. Call PayPal to set up a transaction
    request.request_body(self.build_request_body(gcp_email, amount=amount))
    response = self.client.execute(request)
    if debug:
      print('Status Code: {}'.format(response.status_code))
      print('Status: {}'.format(response.result.status))
      print('Order ID: {}'.format(response.result.id))
      print('Intent: {}'.format(response.result.intent))
      print('Links:')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                         response.result.purchase_units[0].amount.value))

    return response


  """Setting up the JSON request body for creating the order. Set the intent in the
  request body to "CAPTURE" for capture intent flow."""
  @staticmethod
  def build_request_body(gcp_email, amount):
    SHARED_SECRET = os.environ['PAYPAL_SHARED_SECRET']
    hash_me = f'{gcp_email}|{amount}|{SHARED_SECRET}'
    m = hashlib.sha256()
    m.update(hash_me.encode())
    sig = m.hexdigest()
    # print(sig)

    """Method to create body with CAPTURE intent"""
    return \
      {
        "intent": "CAPTURE",
        "application_context": {
          "brand_name": "Security-Assignments.com",
          "landing_page": "BILLING",
          "shipping_preference": "NO_SHIPPING",
          "user_action": "PAY_NOW"
        },
        "purchase_units": [
          {
            "reference_id": gcp_email,
            "description": f"Access to security-assignments.com lab virtual machines on GCP for email address {gcp_email}",
            "custom_id": sig,
            "invoice_id": gcp_email,
            "soft_descriptor": "Lab virtual machines",
            "amount": {
              "value": amount,
              "currency_code": "USD"
            },
            # "amount": {
            #   "currency_code": "USD",
            #   "value": "230.00",
            #   "breakdown": {
            #     "item_total": {
            #       "currency_code": "USD",
            #       "value": "180.00"
            #     },
            #     "shipping": {
            #       "currency_code": "USD",
            #       "value": "30.00"
            #     },
            #     "handling": {
            #       "currency_code": "USD",
            #       "value": "10.00"
            #     },
            #     "tax_total": {
            #       "currency_code": "USD",
            #       "value": "20.00"
            #     },
            #     "shipping_discount": {
            #       "currency_code": "USD",
            #       "value": "10"
            #     }
            #   }
            # },
            # "items": [
            #   {
            #     "name": "T-Shirt",
            #     "description": "Green XL",
            #     "sku": "sku01",
            #     "unit_amount": {
            #       "currency_code": "USD",
            #       "value": "90.00"
            #     },
            #     "tax": {
            #       "currency_code": "USD",
            #       "value": "10.00"
            #     },
            #     "quantity": "1",
            #     "category": "PHYSICAL_GOODS"
            #   },
            #   {
            #     "name": "Shoes",
            #     "description": "Running, Size 10.5",
            #     "sku": "sku02",
            #     "unit_amount": {
            #       "currency_code": "USD",
            #       "value": "45.00"
            #     },
            #     "tax": {
            #       "currency_code": "USD",
            #       "value": "5.00"
            #     },
            #     "quantity": "2",
            #     "category": "PHYSICAL_GOODS"
            #   }
            # ],
            # "shipping": {
            #   "method": "United States Postal Service",
            #   "address": {
            #     "name": {
            #       "full_name":"John",
            #       "surname":"Doe"
            #     },
            #     "address_line_1": "123 Townsend St",
            #     "address_line_2": "Floor 6",
            #     "admin_area_2": "San Francisco",
            #     "admin_area_1": "CA",
            #     "postal_code": "94107",
            #     "country_code": "US"
            #   }
            # }
          }
        ]
      }
