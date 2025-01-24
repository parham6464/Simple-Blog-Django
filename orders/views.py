from django.shortcuts import render
from posts.models import Product
# Create your views here.

def cartshow(request):
    product=Product.objects.all()
    return render (request , 'cart.html' , context={"products":product})