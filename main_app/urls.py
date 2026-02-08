from django.urls import path
from main_app.views import indexPage, loginPage, logoutUser, tracking_detail

urlpatterns = [
    path('', indexPage, name="home"),
    path("track/<str:tracking_number>/", tracking_detail, name="tracking_detail"),
    path("login/", loginPage, name="login"),
    path("logout/", logoutUser, name="logout"),
]