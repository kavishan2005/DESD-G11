# Placeholder file - producer views temporarily disabled
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def producer_dashboard(request):
    return render(request, 'products/producer_dashboard.html', {'message': 'Producer dashboard coming soon'})
