# Paypal-create-order

Creates an order for purchase of lab access for security-assignments.com

This avoids the threat of customers modifying javascript to pay whatever they
want for the purchase.

Paypal client examples were taken from paypal doc pages such as
<https://developer.paypal.com/docs/archive/checkout/how-to/server-integration/>.


## Configuring

In `env.yml`, set the two client ids:
* `PAYPAL_SANDBOX_CLIENT_ID`
* `PAYPAL_LIVE_CLIENT_ID`

In gcp secrets, set the two secrets, and expose them as env vars named as below:

* `PAYPAL_SANDBOX_CLIENT_SECRET`
* `PAYPAL_LIVE_CLIENT_SECRET`
* `PAYPAL_SHARED_SECRET`


## Use

Post the following json to the http-target:

- "gcp_email": a valid email address with which to associate this purchase. Will
  be added to the paypal order as "order_id", "invoice_id", and purchase_unit
  "reference_id".
- "paypal_mode": expected either "LIVE" or "SANDBOX". Determines which
  credentials to use to create the order.


## Develop locally


```bash
LOCAL_DEV=1 functions-framework --target=main --debug --source=main.py
```

The function should be running at `localhost:8080`

Modify the store to post to the local service instead of to the gcp-hosted service:

```diff
diff --git a/store.md b/store.md
index 5c95a8d..1a9bb9e 100644
--- a/store.md
+++ b/store.md
@@ -93,8 +93,8 @@ function initPayPalButton() {
     },
     // https://developer.paypal.com/docs/checkout/reference/server-integration/set-up-transaction/
     createOrder: function(data, actions) {
-      // return fetch('http://localhost:8080/', {
-      return fetch('https://us-central1-security-assignments-kali.cloudfunctions.net/security-assignments-paypal-order-create', {
+      return fetch('http://localhost:8080/', {
+      // return fetch('https://us-central1-security-assignments-kali.cloudfunctions.net/security-assignments-paypal-order-create', {
         method: 'post',
         headers: {
           'content-type': 'application/json'

```

In sandbox mode, test credit cards can be used. See https://developer.paypal.com/tools/sandbox/card-testing/#link-simulatesuccessfulpayments


The store needs to be running via https in order for the store => paypal CORS requests to succeed.

## Deploy

```bash
gcloud functions deploy security-assignments-paypal-order-create \
  --entry-point main \
  --allow-unauthenticated \
  --runtime python39 \
  --env-vars-file env.yml \
  --trigger-http \
  --region us-central1 \
  --security-level secure-always \
  --set-secrets 'PAYPAL_LIVE_CLIENT_SECRET=PAYPAL_LIVE_CLIENT_SECRET:latest,PAYPAL_SANDBOX_CLIENT_SECRET=PAYPAL_SANDBOX_CLIENT_SECRET:latest,PAYPAL_SHARED_SECRET=PAYPAL_SHARED_SECRET:latest'
```


Describe:

```bash
gcloud beta functions describe security-assignments-paypal-order-create
```
