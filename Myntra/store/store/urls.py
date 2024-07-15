from django.urls import path
from . import views
from .views import account, login, home
urlpatterns=[
    path('',views.home, name="home"),
    path('login/',views.login, name="login"),
    path('account/',views.account, name="account"),
    path('store/',views.store, name="store"),
    path('size/',views.size, name="size"),
    path('chart/',views.chart, name="chart"),
    path('figure/',views.figure, name="figure"),
    path('logout/', views.logout, name='logout'),
]