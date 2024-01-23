from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, UserProfile
from .forms import MyForm
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
import os
import random
from django.contrib import messages
import string
from django.utils import timezone
from datetime import timedelta


def send_otp_email(email, otp):
    subject = 'Your OTP for registration'
    message = f'{otp}'
    plain_message = strip_tags(message)
    from_email = os.environ.get('EMAIL_FROM')
    send_mail(subject, plain_message, from_email,
              [email], html_message=message)


def register(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        otp = str(random.randint(1000, 9999))
        if form.is_valid():
            # Check if the user with the provided email already exists
            email = form.cleaned_data['email']
            check_user = User.objects.filter(email=email).first()

            if check_user:
                messages.warning(request, 'User already exists')
                return redirect('auth:register')

            try:
                # Send OTP via email
                send_otp_email(email, otp)

                # Save the user
                user = form.save(commit=False)
                user.last_name = user.username
                user.username = email
                user.set_password(form.cleaned_data['password'])
                user.otp = otp  # Set the OTP
                user.save()

                messages.success(
                    request, 'User registered successfully. Please check your email for OTP.')
                return redirect('auth:login_otp')

            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('auth:register')

    else:
        form = MyForm()

    return render(request, 'auth/register.html', {'form': form})


def login_with_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        # Retrieve the user based on the entered OTP
        user = User.objects.filter(otp=entered_otp).first()

        print("Entered OTP during login:", entered_otp)

        if user:
            messages.success(
                request, 'OTP verification successful. Please log in.')
            return redirect('auth:login')

        else:
            messages.warning(request, 'Invalid OTP. Please try again.')

    return render(request, 'auth/otp_email.html')


def login_user(request):
    # if request.user.is_authenticated:
    #     messages.warning(request, 'yeah your already login')
    #     return redirect('auth:login_otp')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pasw')

        user = authenticate(request, email=email, password=password)
        print(f'user {user}')

        if user is not None:
            print(f"Authenticated user: {user}")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Login success')
            return redirect('app:index')
        else:
            print("Authentication failed")
            messages.warning(
                request, 'Invalid email or password. Please try again.')

    return render(request, 'auth/login.html')


def log_out_user(request):
    logout(request)
    messages.warning(request, 'logout successfully')
    return redirect('auth:login')


# forget password
def generate_otp(length=4):
    return ''.join(random.choices(string.digits, k=length))


def send_reset_email(email, otp):
    subject = 'Password Reset'
    message = f'Use the following OTP to reset your password: {otp}'
    plain_message = strip_tags(message)
    from_email = os.environ.get('EMAIL_FROM')
    send_mail(subject, plain_message, from_email,
              [email], html_message=message)


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate OTP
            otp = generate_otp()

            # Send the password reset email
            send_reset_email(user.email, otp)

            # Store the OTP and timestamp in the database
            user.otp = otp
            user.reset_token_created_at = timezone.now()
            user.save()

            messages.success(
                request, 'Password reset email sent. Please check your inbox.')
            return redirect('auth:password_reset_confirm', token=user.otp)

        messages.warning(request, 'User with this email does not exist.')
        return redirect('auth:password_reset_request')

    return render(request, 'auth/password_reset_request.html')


def password_reset_confirm(request, token):
    user = get_object_or_404(User, otp=token)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        entered_otp = request.POST.get('otp')

        if new_password != confirm_password or user.otp != entered_otp:
            messages.warning(
                request, 'Password and confirmation password should be the same, and the OTP should match.')
            return render(request, 'auth/password_reset_confirm.html', {'token': token})

        # Use Django's built-in set_password method to securely update the password
        user.set_password(new_password)
        user.save()

        messages.success(
            request, 'Password reset successfully. You can now log in with your new password.')
        return redirect('auth:login')

    return render(request, 'auth/password_reset_confirm.html', {'token': token})


# @login_required
# def user_profile(request):
#     # Assuming you're getting the user from the request
#     user = request.user

#     try:
#         # Try to get the associated UserProfile
#         user_profile = user.userprofile
#     except UserProfile.DoesNotExist:
#         # If UserProfile does not exist, handle it accordingly
#         user_profile = None

#     return render(request, 'user_profile.html', {'user': user, 'user_profile': user_profile})
