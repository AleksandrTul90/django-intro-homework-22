from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from catalog.forms import ProductForm
from catalog.models import Product


def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'catalog/product_list.html',
        {
            'products': page_obj,
            'page_obj': page_obj,
        },
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()

    return render(request, 'catalog/product_form.html', {'form': form})


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
