from datetime import timezone
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer, UserSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        books = Book.objects.filter(copies_available__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TransactionViewSet(viewsets.ViewSet):
    def create(self, request):
        user = request.user
        book = get_object_or_404(Book, id=request.data['book_id'])

        if book.copies_available > 0:
            book.copies_available -= 1
            book.save()
            transaction = Transaction.objects.create(user=user, book=book)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        transaction = get_object_or_404(Transaction, id=request.data['transaction_id'])
        transaction.return_date = timezone.now()
        transaction.book.copies_available += 1
        transaction.book.save()
        transaction.save()
        return Response({'message': 'Book returned successfully'})

# Create your views here.
