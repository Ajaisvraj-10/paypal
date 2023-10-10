import paypalrestsdk
from decouple import config
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": config("PAYPAL_CLIENT_ID"),
    "client_secret": config("PAYPAL_CLIENT_SECRET")
})

def create_paypal_payment(amount, currency):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": f"http://localhost:3000/execute?amount={amount}&currency={currency}",
            "cancel_url": "http://cancel.url"
        },
        "transactions": [{
            "amount": {
                "total": amount,
                "currency": "USD"  
            },
            "description": "Payment description"
        }]
    })

    try:
        if payment.create():
            return payment  
        else:
            
            logging.error(f"Failed to create PayPal payment: {payment.error}")
            return None
    except Exception as e:
       
        logging.exception("An error occurred while creating PayPal payment:")
        return None


def execute_paypal_payment(payment_id, payer_id):
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return True
    else:
        return False
