from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if name and phone and message:
            success_message = (
                f'Спасибо, {name}! Ваше сообщение получено. '
                f'Мы свяжемся с вами по номеру {phone}.'
            )

    return render(request, 'catalog/contacts.html', {'success_message': success_message})
