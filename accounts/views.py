from django.shortcuts import render ,redirect 
from .forms import UserRegistrationForm , UserSignUpForm  , UpdateProfile , UpdatePasswordProfile , ForgetPassowrd
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login , logout 
from .models import CustomUser
from allauth.account.forms import LoginForm 
from django.contrib import messages
from django.views.generic import ListView , DeleteView , DetailView , CreateView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password , check_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings



def login1(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method =="POST":
        form = UserRegistrationForm(request.POST , )

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user1 = authenticate(request,username=username , password=password)
            if user1 is not None:
                login(request,user1)
                return redirect('profile')
            else:
                messages.warning(request,'نام کاربری یا رمز عبور شما اشتباه است')
                form = UserRegistrationForm()
                return render(request,"account/login.html" , {'forms':form})
        else:
            messages.warning(request,'مقادیر را به درستی وارد کنید!')
            form = UserRegistrationForm()
            return render(request,"account/login.html" , {'forms':form})

    else:
        form = UserRegistrationForm()
        return render(request,"account/login.html" , {'forms':form})

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        password_checker = request.POST.get('password')
        if len(password_checker) < 8 :
            form = UserSignUpForm()
            messages.warning(request,'رمز عبور شما بسیار کوتاه است')
            return redirect("signup1")

        if len(request.POST.get('email'))== 0:
            form = UserSignUpForm()
            messages.warning(request,'باید ایمیل را وارد کنید')
            return redirect("signup1")
        if len(request.POST.get('phone_number')) == 0:
            form = UserSignUpForm()
            messages.warning(request,'لطفا شماره تلفن خود را وارد کنید')
            return redirect("signup1")
        if len(request.POST.get('username'))==0:
            form = UserSignUpForm()
            messages.warning(request,'لطفا نام کاربری را وارد کنید')
            return redirect("signup1")
        else:
            username = request.POST.get('username')
            check_user = CustomUser.objects.filter(username=username)
            if check_user == True:
                form = UserSignUpForm()
                messages.warning(request,'این نام کاربری توسط یه کاربر دیگر استفاده شده')
                return redirect("signup1")

        
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            CD = form.cleaned_data
            CustomUser.objects.create(username = CD['username'] , phone_number=CD['phone_number'] , password = make_password(CD['password']) , email=CD['email'])
            messages.success(request,'حساب شما با موفقیت ایجاد شد')
            return redirect("login1")
        else:
            form = UserSignUpForm()
            messages.warning(request,'هر ورودی را به درستی وارد کنید!')
            return redirect("signup1")
            

    else:
        form = UserSignUpForm()
    return render(request,"Sign-up/index.html",{'form':form})

@login_required
def log_out(request):
    if request.method =="POST":
        logout(request)
        return redirect('home')
    else:
        return render(request , 'logout.html')





@login_required
def updateprofile(request):
    if request.method == "POST":
        my_user = CustomUser.objects.get(id=request.user.id)
        form = UpdateProfile(request.POST)
        if form.is_valid():
            CD = form.cleaned_data
            if CD['phone_number'] is not None :
                if CD['phone_number'] >= 0:
                    my_user.phone_number = CD['phone_number']
                else:
                    messages.warning(request,'شماره نادرست است')
                    return redirect('profile')
            
            username = CD['username']
            email = CD['email']
            first_name = CD['first_name']
            last_name = CD['last_name']
            if request.user.username != username:
                if len(username)>0:
                    check_user = CustomUser.objects.filter(username=username).exists()
                    if check_user == False :
                        my_user.username = username
                    else:
                        messages.warning(request,'این نام کاربری از قبل وجود دارد')
                        return redirect('profile')

            if request.user.email != email:
                if len(email)>0:
                    check_user = CustomUser.objects.filter(email=email).exists()
                    if check_user == False :
                        my_user.email = email
                    else:
                        messages.warning(request,'این ایمیل وجود دارد !')
                        return redirect('profile')

            if len(first_name) > 0:
                my_user.first_name = first_name
            if len(last_name) > 0:
                my_user.last_name = last_name
            
            CustomUser.save(my_user)
            messages.success(request,'اطلاعات شما با موفقیت تغییر کرد')
            return redirect('profile')
           
        else:
            messages.warning(request,'مطمئن شوید که ورودی ها را به درستی وارد کنید!')
            return redirect('profile')
    else:
        return render(request , 'Profile/index.html')

@login_required
def changepassword(request):
    if request.method == "POST":
        new_pass = request.POST.get('new_pass')
        if len(new_pass)<8:
            messages.warning(request,'رمز عبور شما حداقل باید 8 کاراکتر باشد')
            return redirect('profile')
        else:
            my_user = CustomUser.objects.get(id=request.user.id)
            form = UpdatePasswordProfile(request.POST)
            if form.is_valid():
                CD = form.cleaned_data
                checker = check_password(CD['current_pass'] , my_user.password)
                if checker == True:
                    my_user.password = make_password(CD['new_pass'])
                    CustomUser.save(my_user)
                    messages.success(request,'رمز عبور شما با موفقیت تغییر کرد اکنون دوباره وارد شوید')
                    return redirect ('login1')
                else:
                    messages.warning(request,'رمز عبور شما با رمز عبور حساب شما برابر نیست')
                    return redirect ('profile')
                

    else:
        return render(request , 'Profile/index.html')
    

def passwordforget(request):
    if request.method == "POST":
        form = ForgetPassowrd(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                obj = CustomUser.objects.get(email=email)
                if obj.is_active == False:
                    messages.warning(request,'دسترسی اکانت شما بسته شده است')
                    form = ForgetPassowrd()
                    return render (request , 'registration/password_reset.html' , context={'form':form})

                send_list = []
                send_list.append(obj.email)
            except:
                messages.warning(request,'این ایمیل وجود ندارد')
                form = ForgetPassowrd()
                return render (request , 'registration/password_reset.html' , context={'form':form})

            try:
                send_mail(subject='اطلاعات حساب کاربری' , message=f'با عرض سلام و ادب رمز عبور شما در سایت انجمن علمی کامپیوتر در زیر نوشته شده است \n نا کاربری :\n {obj.username} \nرمز عبور :\n {obj.password}' , from_email=settings.EMAIL_HOST_USER ,recipient_list=send_list)
                return redirect('completereset')
            except:
                messages.warning(request,'ایمیل ارسال نشد')
                form = ForgetPassowrd()
                return render (request , 'registration/password_reset.html' , context={'form':form})

        else:
            messages.warning(request,'ایمیل را درست وارد کنید')
            form = ForgetPassowrd()
            return render (request , 'registration/password_reset.html' , context={'form':form})

            
    else:
        form = ForgetPassowrd()
        return render (request , 'registration/password_reset.html' , context={'form':form})

def completereset(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return render(request , '404.html')

    return render (request , 'registration/password_complete.html')

