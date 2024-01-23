from django.urls import path
from . import views
app_name = 'auth'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login-otp/', views.login_with_otp, name='login_otp'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.log_out_user, name='logout'),

    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]


# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('name')
#         email = request.POST.get('email')
#         password = request.POST.get('pasw')

#         check_user = User.objects.filter(email=email).first()

#         if check_user:
#             messages.warning(request, 'user is already exist')
#             return redirect('auth:register')
        
#         otp = str(random.randint(1000,9999))
#         user = User.objects.create(username=email, email=email,first_name=username, password=password,otp=otp)
#         user.save()

#         messages.success(request, 'user register succsess please login')
#         return redirect('auth:login')
    

#     return render(request,'auth/register.html')