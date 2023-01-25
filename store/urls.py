from django.urls import path
from .views import *

urlpatterns = [

    path('', GetIndex.as_view(), name='index'),
    path('category/<int:pk>/', ProductByCategory.as_view(), name='category'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('mailing/', SendSpam.as_view(), name='send_spam'),
    path('search/', Search.as_view(), name='search'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),

]
