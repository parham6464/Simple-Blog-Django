from django.shortcuts import render , redirect 
from django.urls import reverse , reverse_lazy
from django.http import HttpResponseRedirect
from posts.models import Post , BannerPosts , FeaturedPost , FeaturedCategory , Category , FooterCategory , Comments , Product
import random
from django.core.paginator import Paginator

# Create your views here.
def showhome(request):
    last_three_product = Product.objects.order_by('-id')[:3]
    last_three_in_ascending_order = reversed(last_three_product)


    last_ten = Post.objects.order_by('-id')[:3]
    last_ten_in_ascending_order = reversed(last_ten)

    last_six = Post.objects.order_by('-id')[:6]
    last_six_in_ascending_order = reversed(last_ten)


    bannerpost=BannerPosts.objects.all()
    featured = FeaturedPost.objects.all()
    category_featured = FeaturedCategory.objects.all()
    all_category = Category.objects.all()
    Footer = FooterCategory.objects.all()
    allposts = Paginator(Post.objects.order_by('-id'),6)
    p = request.GET.get('page')
    allpost_pg= allposts.get_page(p)


    return render (request , 'index.html' , context={'products':last_three_in_ascending_order,'allposts':allpost_pg,'featured':last_ten_in_ascending_order , 'banner':bannerpost , 'last':last_six_in_ascending_order , 'featured_down':featured , 'category_featured':category_featured , 'all_category':all_category , 'footerct':Footer})

def filtercat(request , category):
    last_ten = Post.objects.order_by('-id')[:3]
    last_ten_in_ascending_order = reversed(last_ten)

    last_six = Post.objects.order_by('-id')[:6]
    last_six_in_ascending_order = reversed(last_ten)


    bannerpost=BannerPosts.objects.all()
    featured = FeaturedPost.objects.all()
    category_featured = FeaturedCategory.objects.all()
    all_category = Category.objects.all()
    Footer = FooterCategory.objects.all()
    cat_filter = Category.objects.get(name=category)
    allposts = Paginator(Post.objects.order_by('-id').filter(category=cat_filter),6)
    p = request.GET.get('page')
    allpost_pg= allposts.get_page(p)


    return render (request , 'index.html' , context={'allposts':allpost_pg,'featured':last_ten_in_ascending_order , 'banner':bannerpost , 'last':last_six_in_ascending_order , 'featured_down':featured , 'category_featured':category_featured , 'all_category':all_category , 'footerct':Footer})


def showdetail1(request , id):
    if request.method == "POST":
        post = Post.objects.get(pk=id)
        Comments.objects.create(name=request.POST['name'] , gmail=request.POST['gmail'] , body=request.POST['body'] , post=post )

        return redirect('showdetail' , id=id)
    else:
        post = Post.objects.get(pk=id)
        cat_name = Category.objects.get(name=post.category.name)
        suggest = list(Post.objects.all().filter(category=cat_name))
        commentsshow = Paginator(Comments.objects.all().filter(post=post) , 3)
        p = request.GET.get('page')
        comment_pg= commentsshow.get_page(p)
        if len(suggest) >=2:
            random_items = random.sample(suggest, 2)
        else:
            random_items = suggest

        return render (request , 'details.html' , context={"post":post , 'suggest':random_items , 'commentsshow':comment_pg})


def addlike(request , id):
    post = Post.objects.get(pk=id)
    try:
        post.likes +=1
    except:
        post.likes = 1
    post.save()
    return redirect('showdetail' , id=id)


def searchresult(request):
    if request.META.get("HTTP_REFERER"):
        post = Post.objects.all()
        name = request.POST['search']
        request.session['search'] = name
        ids = []
        print(post)
        for i in post:
            if name in i.title:
                ids.append(i.id)

        print(ids)
        result = Paginator(Post.objects.all().filter(id__in=ids) , 6)
        
        p = request.GET.get('page')
        result_pg= result.get_page(p)

        return render (request , 'search.html' , context={'result':result_pg , 'text':name})
    else:
        if request.session['search']:
            post = Post.objects.all()
            name = request.session['search']
            request.session['search'] = name
            ids = []
            print(post)
            for i in post:
                if name in i.title:
                    ids.append(i.id)

            print(ids)
            result = Paginator(Post.objects.all().filter(id__in=ids) , 6)
            
            p = request.GET.get('page')
            result_pg= result.get_page(p)

            return render (request , 'search.html' , context={'result':result_pg , 'text':name})
        else:
            return redirect ('home')