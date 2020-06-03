from django.conf.urls import url

from home.views import Home

app_name = "home"

urlpatterns = [
    url(r"^$", Home.as_view(), name="index"),
]
