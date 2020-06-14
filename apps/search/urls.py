from django.conf.urls import url

from apps.search.views import ProcessRecipeSearch

app_name = "search"

urlpatterns = [
    url(
        r"^process_recipe_search/$",
        ProcessRecipeSearch.as_view(),
        name="process_recipe_search",
    ),
]
