# Paypal-create-order

Creates an order for purchase of lab access for security-assignments.com

This avoids the threat of customers modifying javascript to pay whatever they
want for the purchase.

Paypal client examples were taken from paypal doc pages such as
<https://developer.paypal.com/docs/checkout/reference/server-integration/set-up-transaction/>.


## Configuring

In `env.yml`, set the two client ids:
* `PAYPAL_SANDBOX_CLIENT_ID`
* `PAYPAL_LIVE_CLIENT_ID`

In gcp secrets, set the two secrets, and expose them as env vars named as below:

* `PAYPAL_SANDBOX_CLIENT_SECRET`
* `PAYPAL_LIVE_CLIENT_SECRET`


## Use

Post the following json to the http-target:

- "gcp_email": a valid email address with which to associate this purchase. Will
  be added to the paypal order as "order_id", "invoice_id", and purchase_unit
  "reference_id".
- "paypal_mode": expected either "LIVE" or "SANDBOX". Determines which
  credentials to use to create the order.


## Deploy

```bash
gcloud beta functions deploy security-assignments-paypal-order-create \
  --entry-point main \
  --allow-unauthenticated \
  --runtime python37 \
  --env-vars-file env.yml \
  --trigger-http \
  --region us-central1 \
  --security-level secure-always \
  --set-secrets 'PAYPAL_LIVE_CLIENT_SECRET=PAYPAL_LIVE_CLIENT_SECRET:latest,PAYPAL_SANDBOX_CLIENT_SECRET=PAYPAL_SANDBOX_CLIENT_SECRET:latest'
```


Describe:

```bash
gcloud beta functions describe security-assignments-paypal-order-create
```
