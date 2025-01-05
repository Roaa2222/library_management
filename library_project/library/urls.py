from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserViewSet, TransactionViewSet
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('books', BookViewSet, basename='book')
router.register('users', UserViewSet, basename='user')

transaction_list = TransactionViewSet.as_view({'post': 'create'})
transaction_return = TransactionViewSet.as_view({'post': 'return_book'})

urlpatterns = [
    path('', include(router.urls)),
    path('transactions/', transaction_list, name='transaction-list'),
    path('transactions/return/', transaction_return, name='transaction-return'),
     path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]