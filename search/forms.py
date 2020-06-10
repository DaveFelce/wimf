from urllib.parse import urlencode

from common.utils import cleanup_ingredients
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


class RecipeSearchForm(forms.Form):
    """
    Simple search form config, for validating against
    """

    def __init__(self, *args, **kwargs):
        super(RecipeSearchForm, self).__init__(*args, **kwargs)

    ingredients = forms.CharField(label="Ingredients", max_length=2000, required=True)
