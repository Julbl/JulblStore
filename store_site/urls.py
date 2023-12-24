"""
Definition of urls for store_site.
"""

from datetime import datetime
from django.urls import path, include, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('links/', views.links, name='links'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('videopost/', views.videopost, name='videopost'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('anketa/', views.anketa, name='anketa'),
    path('registration/', views.registration, name='registration'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:category_id>/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('set_cart_item/<int:cart_item_id>/', views.set_cart_item, name='set_cart_item'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buy_cart/', views.buy_cart, name='buy_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('profile/', views.profile, name='profile'),

    path('management/', views.management, name= 'management'),
    path('management/orders', views.manage_orders, name= 'manage_orders'),
    path('management/blog', views.manage_blog, name= 'manage_blog'),
    path('management/feedback', views.manage_feedback, name= 'manage_feedback'),
    path('management/newpost', views.manage_new_post, name= 'manage_new_post'),
    path('management/products', views.manage_products, name= 'manage_products'),
    path('management/newproduct', views.manage_new_product, name= 'manage_new_product'),
    path('manage/order/status', views.manage_order_status, name= 'manage_order_status'),
    path('manage/blog/<int:parametr>/change', views.manage_blog_change, name= 'manage_blog_change'),
    path('manage/blog/<int:parametr>/delete', views.manage_blog_delete, name= 'manage_blog_delete'),
    path('manage/product/<int:parametr>/change', views.manage_product_change, name= 'manage_product_change'),
    path('manage/product/<int:parametr>/delete', views.manage_product_delete, name= 'manage_product_delete'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    re_path(r'^.*', views.missing_page),
]
