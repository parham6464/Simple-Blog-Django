from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(BannerPosts)
admin.site.register(FeaturedPost)
admin.site.register(FeaturedCategory)
admin.site.register(FooterCategory)
admin.site.register(Comments)
admin.site.register(Product)