from datetime import datetime
from pickle import NONE
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import AnketaForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CommentForm
from .forms import BlogForm
from .models import Product, Cart, CartItem, Category, Order, OrderItem, Feedback
from .forms import CartItemForm, ProductForm
from .models import Blog
from django.http import JsonResponse
from .models import Comment
from django.shortcuts import render, redirect, get_object_or_404



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'message': 'Страница с нашими контактами.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О нас',
            'message': 'Сведения о нас.',
            'year': datetime.now().year,
        }
    )


def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'year': datetime.now().year,
        }
    )


def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,
            'year': datetime.now().year,
        }
    )


def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )


def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None

    gender = {
        'male': 'Мужчина',
        'female': 'Женщина'
    }
    internet = {
        '1': 'Каждый день',
        '2': 'Несколько раз в день',
        '3': 'Несколько раз в неделю',
        '4': 'Несколько раз в месяц'
    }
    
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            form.save()

            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['occupation'] = form.cleaned_data['occupation']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['internet'] = internet[form.cleaned_data['internet']]
            data['notice'] = 'Да' if form.cleaned_data['notice'] else 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']

            form = None

    else:
        form = AnketaForm()

    return render(
        request,
        'app/anketa.html',
        {
            'title': 'Анкета',
            'year': datetime.now().year,
            'form': form,
            'data': data
        }
    )


def registration(request):
    """Renders the registration page."""

    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False  # запрещен вход в административный отдел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации
            regform.save()  # сохраняем изменения после добавления полей
            return redirect('home')  # переадресация на главную старницу после регистарции
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )


def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видео',
            'year': datetime.now().year,
        }
    )


@login_required
def product_list(request, category_id = None):
    products = Product.objects.all()

    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = CartItem.objects.filter(cart=cart)
        
    else:
        cart = None
        cart_items = []

    total_price = 0
    quantity = 0

    for item in cart_items:
        total_price += item.quantity * item.product.price
        quantity += item.quantity

    return render(request, 'app/product_list.html',
        {
            'products': products.filter(category=category_id) if category_id else products,
            'cart_items': cart_items,
            'total_price': total_price,
            'quantity': quantity,
            'categories': Category.objects.all(),
            'category_id': category_id,
        })


@login_required
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = CartItemForm()

    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.subtotal = cart_item.product.price * cart_item.quantity
            cart_item.save()
            cart.total_price += cart_item.subtotal
            cart.save()

    return render(request, 'app/product_deta0il.html', {'product': product, 'form': form})


@login_required
def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('app:product_list')
    
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = 0
    quantity = 0

    for item in cart_items:
        total_price += item.quantity * item.product.price
        quantity += item.quantity
        item.sum = item.quantity * item.product.price

    return render(request, 'app/view_cart.html',
        {
            'cart_items': cart_items,
            'total_price': total_price,
            'quantity': quantity        
        })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = CartItemForm(request.POST or None)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        cart_item.quantity = quantity
        cart_item.save()

        cart.save()

    total_price = 0
    quantity = 0

    for item in CartItem.objects.filter(cart=cart):
        total_price += item.quantity * item.product.price
        quantity += item.quantity

    response_data = { 'total_price': total_price, 'quantity': quantity }
    return JsonResponse(response_data)

@login_required
def set_cart_item (request, cart_item_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, id=cart_item_id)
    form = CartItemForm(request.POST or None)
    
    if form.is_valid():
        cart_item.quantity = form.cleaned_data['quantity']
        cart_item.save()
        cart.save()

    total_price = 0
    quantity = 0

    for item in CartItem.objects.filter(cart=cart):
        total_price += item.quantity * item.product.price
        quantity += item.quantity

    response_data = { 'total_price': total_price, 'quantity': quantity }
    return JsonResponse(response_data)

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    cart_item.delete()

    return JsonResponse({'success': True})


@login_required
def update_cart(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')

        print(f"Updating cart item {cart_item_id} with quantity {quantity}")

        cart_item = get_object_or_404(CartItem, pk=cart_item_id)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity should be a positive integer.")
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'})

        cart_item.quantity = quantity
        cart_item.subtotal = cart_item.product.price * cart_item.quantity
        cart_item.save()

        # Обновляем общую стоимость корзины
        update_cart_total(cart_item.cart)


        return JsonResponse({
            'new_quantity': cart_item.quantity,
            'total_price': cart_item.cart.total_price,
        })
    else:
        return HttpResponse('Invalid request', status=400)

@login_required
def buy_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        order = Order()
        order.user = request.user
        order.save()

        for item in cart_items:
            if (item.quantity > 0):
                order_item = OrderItem()
                order_item.order = order
                order_item.product = item.product
                order_item.quantity = item.quantity
                order_item.price = item.product.price
                order_item.save()

            item.delete()

        return JsonResponse({'success': True})
    else:
        return HttpResponse('Invalid request', status=400)


@login_required
def profile(request):
    statuses = {
        'new': 'Новый',
        'in_progress': 'В обработке',
        'confirmed': 'Подтвержден',
        'sent': 'Отправлен',
        'done': 'Завершен',
        'canceled': 'Отменен',
    }

    orders = Order.objects.filter(user=request.user)

    for order in orders:
        order.order_items = OrderItem.objects.filter(order=order)
        order.total = 0
        order.status_ = statuses[order.status]

        for order_item in order.order_items:
            order_item.sum = order_item.quantity * order_item.price
            order.total += order_item.sum

    return render(request, 'app/profile.html', {
        'orders': orders,
        'year': datetime.now().year,
        'title': 'Профиль'
    })






@login_required
def management (request):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    return render(
        request,
        'app/management.html',
        {
            'title':'Управление',
            'year':datetime.now().year,
        }
    )

@login_required
def manage_orders (request):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    statuses = {
        'new': 'Новый',
        'in_progress': 'В обработке',
        'confirmed': 'Подтвержден',
        'sent': 'Отправлен',
        'done': 'Завершен',
        'canceled': 'Отменен',
    }

    orders = Order.objects.all()

    for order in orders:
        order.order_items = OrderItem.objects.filter(order=order)
        order.total = 0
        order.status_ = statuses[order.status]

        for order_item in order.order_items:
            order_item.sum = order_item.quantity * order_item.price
            order.total += order_item.sum

    return render(request, 'app/manage/orders.html', {
        'orders': orders,
        'year': datetime.now().year,
        'statuses': statuses,
        'title': 'Профиль'
    })

@login_required
def manage_order_status (request):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)
    order.status = request.POST.get('status')
    order.save()

    return redirect('manage_orders')

@login_required
def manage_blog (request):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    blog = Blog.objects.all()

    return render(
        request,
        'app/manage/blog.html',
        {
            'title':'Управление блогом',
            'year':datetime.now().year,
            'blog': blog,

        }
    )

def manage_feedback (request):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')
    
    gender = {
        'male': 'Мужчина',
        'female': 'Женщина'
    }
    internet = {
        '1': 'Каждый день',
        '2': 'Несколько раз в день',
        '3': 'Несколько раз в неделю',
        '4': 'Несколько раз в месяц'
    }

    feedback = Feedback.objects.all()

    for data in feedback:
        data.gender = gender[data.gender]
        data.internet = internet[data.internet]
        data.notice = 'Да' if data.notice else 'Нет'

    return render(
        request,
        'app/manage/feedback.html',
        {
            'title':'Управление отзывами',
            'year':datetime.now().year,
            'feedback': feedback,

        }
    )

@login_required
def manage_blog_change (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    blog_id = parametr
    blog = Blog.objects.get(id=blog_id)
    blog.image = request.POST.get('image')
    blog.title = request.POST.get('title')
    blog.content = request.POST.get('content')
    blog.save()

    return redirect('manage_blog')

@login_required
def manage_blog_delete (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    blog_id = parametr
    blog = Blog.objects.get(id=blog_id)
    blog.delete()

    return redirect('manage_blog')

@login_required
def manage_products (request):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    products = Product.objects.all()

    for product in products:
        product.price = int(product.price)

    return render(
        request,
        'app/manage/products.html',
        {
            'title':'Управление товарами',
            'year':datetime.now().year,
            'products': products,
            'categories': Category.objects.all()
        }
    )

@login_required
def manage_product_change (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    product = Product.objects.get(id=parametr)
    product.name = request.POST.get('name')
    product.description = request.POST.get('description')
    product.price = request.POST.get('price')
    product.category = Category.objects.get(id=request.POST.get('category'))
    product.save()

    return redirect('manage_products')

@login_required
def manage_product_delete (request, parametr):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    product = Product.objects.get(id=parametr)
    product.delete()

    return redirect('manage_products')

@login_required
def manage_new_post(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()
            return redirect('manage_blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/manage/new_post.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )

@login_required
def manage_new_product (request):
    assert isinstance(request, HttpRequest)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_staff:
        return redirect('home')

    if request.method =="POST":
        productform = ProductForm(request.POST,request.FILES)
        if productform.is_valid():
            product_f = productform.save(commit= False)
            product_f.save()

            return redirect('manage_products')
    else:
        productform = ProductForm()

    return render(
        request,
        'app/manage/new_product.html',
        {
           'productform':productform,
           'title': 'Добавить новый продукт',
           'year':datetime.now().year,
           'categories': Category.objects.all()
        }
    )

def missing_page (request):
    """Renders the 404 page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/404.html',
        {
            'title':'Страница не найдена',
            'year':datetime.now().year,
        }
    )
