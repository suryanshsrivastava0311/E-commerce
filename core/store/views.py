from store.models import Product,ReviewRating
from cart.models import  CartItems
from category.models import Category
from django.shortcuts import render, get_object_or_404 , redirect
from cart.views import _cart_id
from .form import ReviewForm
from payments.models import Order
from django.contrib import messages
from store.models import Product
from django.http import Http404



def store(request,category_slug=None):
    categories = None
    products = None
    if category_slug !=None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_avilable=True)
        product_count = products.count()
    else:
        products=Product.objects.all().filter(is_avilable=True)
        product_count=products.count()
    
    context={
        'products' : products,
        'product_count': product_count,

    }
    return render(request, 'store/store.html',context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)

        in_cart = CartItems.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()   

    except Product.DoesNotExist:
        raise Http404("Product not found")

    # check authentication
    if request.user.is_authenticated:
        orderproduct = Order.objects.filter(user=request.user,is_paid=True).exists()
    else:
        orderproduct = False

    # Get the reviews
    reviews = ReviewRating.objects.filter(product=single_product,status=True)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
    }

    return render(request, 'store/product_detail.html', context)

  


def search(request):
    products = Product.objects.none()
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(description__icontains=keyword)
    context={
        'products': products,
    }
    return render(request,'store/store.html',context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

