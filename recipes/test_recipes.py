""" Recipes Tests """

import logging

from django.urls import reverse
from django.shortcuts import get_object_or_404
import io
from model_bakery import baker
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITransactionTestCase

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class TestRecipes(APITransactionTestCase):
    """ Test Recipes """

    reset_sequences = True  # So we can check an auto-incremented pk further down

    def setUp(self):
        """ Set up some commonly needed attributes """

        self.recipe1 = baker.make(
            "recipes.Recipe", name="testname", url="http://sometestplace.com"
        )
        self.recipe2 = baker.make("recipes.Recipe", name="testname_recipe2")
        self.test_recipe = {
            "name": "Three In One Onion Dip Recipe",
            "url": "http://cookeatshare.com/recipes/three-in-one-onion-dip-4122",
            "ingredients": "cheddar cheese, cheese, green onion",
        }

    def test_serialization_from_stored_recipes(self):
        """
        Stored recipes should be serialized into JSON using the serializer
        """
        serializer = RecipeSerializer(self.recipe1)
        json_content = JSONRenderer().render(serializer.data)
        self.assertIsInstance(json_content, bytes)

    def test_serialization_from_bytestream(self):
        """
        Should be possible to store recipes as bytestream from JSON using the serializer
        """
        serializer = RecipeSerializer(self.recipe1)
        json_content = JSONRenderer().render(serializer.data)
        stream = io.BytesIO(json_content)
        data = JSONParser().parse(stream)

        serializer = RecipeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "testname")  # OrderedDict
        self.assertTrue(serializer.save())

    def test_serialization_from_string(self):
        """
        Should be possible to store recipes from JSON as string using the serializer
        """

        serializer = RecipeSerializer(data=self.test_recipe)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["name"], "Three In One Onion Dip Recipe"
        )
        serializer.save()

        recipe4 = get_object_or_404(Recipe, name="Three In One Onion Dip Recipe")
        self.assertEqual(recipe4.ingredients, "cheddar cheese, cheese, green onion")

    def test_many_recipe_objects(self):
        """
        Should be possible to retrieve multiple recipe objs using the serializer
        """
        serializer = RecipeSerializer(Recipe.objects.all(), many=True)
        self.assertEqual(len(serializer.data), 2)

    def test_REST_get_for_all_recipes(self):
        """
        Test retrieval from the front end, using a Client and GET request
        """
        response = self.client.get(reverse("recipes:recipelist"), format="json")
        data = response.data
        self.assertEqual(data[1]["name"], "testname_recipe2")

    def test_json_post_and_retrieval(self):
        """
        Test creation using the front end using POST, then retrieve using both
        DB obj and GET request
        """

        # Create a new object with a POST to the REST API
        response = self.client.post(
            reverse("recipes:recipelist"), data=self.test_recipe, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test retrieval of the new obj using DB
        recipe = get_object_or_404(Recipe, pk=3)  # reset_sequences == True
        self.assertEqual(
            recipe.url, "http://cookeatshare.com/recipes/three-in-one-onion-dip-4122"
        )
        self.assertEqual(Recipe.objects.count(), 3)

        # Test retrieval of new obj using GET for list of all objects
        response = self.client.get(reverse("recipes:recipelist"), format="json")
        data_as_ordered_dict = response.data
        self.assertEqual(
            data_as_ordered_dict[2]["name"], "Three In One Onion Dip Recipe"
        )

        # Test retrieval of new obj using GET for single object
        response = self.client.get(
            reverse("recipes:recipedetail", kwargs={"pk": 3}), format="json"
        )
        data_as_dict = response.data
        self.assertEqual(
            data_as_dict["ingredients"], "cheddar cheese, cheese, green onion"
        )
