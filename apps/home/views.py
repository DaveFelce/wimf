from django.contrib.messages import get_messages
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from apps.search.forms import RecipeSearchForm


class Home(View):
    """Home page class-based view

    Args:
        View (:obj:Django View base class, required)

    """

    def get(self, request):
        """get http method: search form will be empty
        """
        context = {
            "reverse": reverse(
                "home:index"
            ),  # So we can get back here if things go wrong
        }
        context.update(
            {"form": RecipeSearchForm(), "messages": get_messages(request),}
        )
        return render(request, "home/index.html", context)
