from apps.home.views import Home
from django.conf.urls import url

app_name = "home"

urlpatterns = [
    url(r"^$", Home.as_view(), name="index"),
]
