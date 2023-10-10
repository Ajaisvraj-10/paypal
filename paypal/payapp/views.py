from django.shortcuts import render, redirect
from paypal_payment import create_paypal_payment

def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        payment = create_paypal_payment(amount, currency)
        
        approval_url = None
        for link in payment.links:
            if link.rel == 'approval_url':
                approval_url = link.href
                break

        if approval_url:
            return redirect(approval_url)
        else:
            return render(request, 'payment_error.html')

    return render(request, 'payment.html')
