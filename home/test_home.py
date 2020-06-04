from django.test import TestCase


class TestHome(TestCase):
    """ Test Home """

    def test_index(self):
        """Home page index page

        Simple tests for now
        """

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>What's in my Fridge</title>")
        self.assertContains(
            response,
            '<h3 class="panel-title">Search for recipes using ingredients found in your fridge or cupboards!</h3>',
        )
        self.assertContains(response, "<p>&copy; David Felce, 2020. Contact: davefelce@gmail.com</p>")
