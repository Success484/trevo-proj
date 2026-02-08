from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render 
from django.contrib import messages
from main_app.models import Order
import json
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def indexPage(request):
    # If user tries to search but is not logged in
    if not request.user.is_authenticated and request.GET.get("tracking_number"):
        messages.error(request, "🔐 Please login to track your shipment.")
        return redirect("login")
    tracking_number = request.GET.get("tracking_number")
    if tracking_number:
        try:
            order = Order.objects.get(tracking_number=tracking_number)
            return redirect("tracking_detail", tracking_number=order.tracking_number)
        except Order.DoesNotExist:
            messages.error(request, "❌ Invalid Tracking Code. Please try again.")
            return redirect("home")
    return render(request, "pages/index.html")

def tracking_detail(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number)

    # collect events with coordinates (asc order for route path)
    events_qs = order.events.order_by('timestamp')  # ascending
    events_list = []
    for e in events_qs:
        if e.latitude is not None and e.longitude is not None:
            events_list.append({
                "status": e.status,
                "location": e.location,
                "note": e.note,
                "timestamp": e.timestamp.isoformat(),
                "lat": float(e.latitude),
                "lng": float(e.longitude),
            })

    events_json = json.dumps(events_list)  # will be escaped in template
    return render(request, "pages/tracking_detail.html", {
        "order": order,
        "events_json": events_json,
    })

def loginPage(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "✅ Login successful.")
                return redirect("home")
    context = {
        "loginform": form
    }
    return render(request, "pages/login.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request, "🔐 You have been logged out.")
    return redirect("home")