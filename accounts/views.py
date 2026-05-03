from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

def register_choice(request):
    return render(request, 'accounts/register_choice.html')

def register_customer(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create or get profile
            profile, created = Profile.objects.get_or_create(user=user)
            
            # Save all the additional fields
            profile.user_type = 'customer'
            profile.phone = request.POST.get('phone', '')
            profile.address = request.POST.get('address', '')
            profile.postcode = request.POST.get('postcode', '')  # THIS IS IMPORTANT
            profile.save()
            
            # Log the user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register_customer.html', {'form': form})

def register_producer(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.user_type = 'producer'
            profile.phone = request.POST.get('phone', '')
            profile.address = request.POST.get('address', '')
            profile.postcode = request.POST.get('postcode', '')
            profile.save()
            
            # Create producer record
            from products.models import Producer
            producer, created = Producer.objects.get_or_create(
                user=user,
                defaults={
                    'farm_name': request.POST.get('farm_name', f"{user.username}'s Farm"),
                    'farm_description': request.POST.get('farm_description', ''),
                    'postcode': request.POST.get('postcode', ''),  # Add postcode to producer too
                    'is_active': True
                }
            )
            
            # Log the user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            messages.success(request, f'Producer account created for {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register_producer.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.postcode = request.POST.get('postcode', '')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/edit_profile.html')
