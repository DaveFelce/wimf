import io
import logging

import pytest
from apps.recipes.models import Recipe
from apps.recipes.serializers import RecipeSerializer
from apps.search.test.fixtures.recipes import test_recipe
from django.shortcuts import get_object_or_404
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient

# Get an instance of a logger
logger = logging.getLogger(__name__)


# reset_sequences so we can fetch by known ids from the db
@pytest.mark.django_db(transaction=True, reset_sequences=True)
class TestRecipes:
    """ Test Recipes """

    def test_serialization_from_bytestream(self, clear_recipe_index):
        """
        Should be possible to store recipes as bytestream from JSON using the serializer
        """
        # GIVEN
        recipe = baker.make(
            "recipes.Recipe", name="testname", url="http://sometestplace.com"
        )

        # WHEN
        serializer = RecipeSerializer(recipe)
        json_content = JSONRenderer().render(serializer.data)
        stream = io.BytesIO(json_content)
        data = JSONParser().parse(stream)

        serializer = RecipeSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["name"] == "testname"
        assert serializer.save()

    def test_serialization_from_string(self, clear_recipe_index, test_recipe):
        """
        Should be possible to store recipes from JSON as string using the serializer
        """

        serializer = RecipeSerializer(data=test_recipe)
        assert serializer.is_valid()
        assert serializer.validated_data["name"] == "Three In One Onion Dip Recipe"
        assert serializer.save()

        recipe4 = get_object_or_404(Recipe, name="Three In One Onion Dip Recipe")
        assert recipe4.ingredients == "cheddar cheese, cheese, green onion"

    def test_many_recipe_objects(self, clear_recipe_index):
        """
        Should be possible to retrieve multiple recipe objs using the serializer
        """
        # GIVEN
        baker.make("recipes.Recipe", _quantity=2)
        serializer = RecipeSerializer(Recipe.objects.all(), many=True)
        assert len(serializer.data) == 2

    def test_REST_get_for_all_recipes(self, clear_recipe_index):
        """
        Test retrieval from the front end, using a Client and GET request
        """
        # WHEN
        baker.make("recipes.Recipe", name="testname", url="http://sometestplace.com")
        baker.make("recipes.Recipe", name="testname_recipe2")

        # THEN
        client = APIClient()
        response = client.get(reverse("recipes:recipelist"), format="json")
        data = response.data
        assert data[1]["name"] == "testname_recipe2"

    def test_json_post_and_retrieval(self, clear_recipe_index, test_recipe):
        """
        Test creation using the front end using POST, then retrieve using both
        DB obj and GET request
        """

        # Create a new object with a POST to the REST API
        client = APIClient()
        response = client.post(
            reverse("recipes:recipelist"), data=test_recipe, format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Test retrieval of the new obj using DB
        recipe = get_object_or_404(Recipe, pk=1)  # reset_sequences == True
        assert (
            recipe.url == "http://cookeatshare.com/recipes/three-in-one-onion-dip-4122"
        )
        assert Recipe.objects.count() == 1

        # Test retrieval of new obj using GET for list of all objects
        client = APIClient()
        response = client.get(reverse("recipes:recipelist"), format="json")
        data_as_ordered_dict = response.data
        assert data_as_ordered_dict[0]["name"] == "Three In One Onion Dip Recipe"

        # Test retrieval of new obj using GET for single object
        client = APIClient()
        response = client.get(
            reverse("recipes:recipedetail", kwargs={"pk": 1}), format="json"
        )
        data_as_dict = response.data
        assert data_as_dict["ingredients"] == "cheddar cheese, cheese, green onion"
