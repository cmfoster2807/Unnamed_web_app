from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Developer, Game, Review


class GameDetailViewTests(TestCase):
    def test_renders_synced_game_data_and_reviews(self):
        developer = Developer.objects.create(name="Test Studio", igdb_id=101)
        game = Game.objects.create(
            title="Test Adventure",
            igdb_id=202,
            cover_image_url="https://example.com/cover.jpg",
            platform="PC",
            description="A game-detail integration test.",
            genre="Adventure",
        )
        game.developers.add(developer)

        user = get_user_model().objects.create_user(
            username="reviewer",
            password="test-password",
        )
        Review.objects.create(
            user=user,
            game=game,
            rating=8.5,
            review_text="A strong test review.",
        )

        response = self.client.get(reverse("game_detail", args=[game.igdb_id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "games/game_detail.html")
        self.assertContains(response, "Test Adventure")
        self.assertContains(response, "Test Studio")
        self.assertContains(response, "A strong test review.")
        self.assertContains(response, "pages/style.css")


class GameSearchViewTests(TestCase):
    @patch("games.views.search_games")
    def test_search_result_links_to_game_detail(self, mock_search_games):
        mock_search_games.return_value = [
            {
                "id": 303,
                "name": "Search Result",
                "cover": {"url": "//example.com/cover.jpg"},
            }
        ]

        response = self.client.get(reverse("search"), {"q": "result"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "games/search.html")
        self.assertContains(response, "Search Result")
        self.assertContains(response, reverse("game_detail", args=[303]))
        self.assertContains(response, "pages/style.css")

    @patch("games.views.search_games", side_effect=KeyError("access_token"))
    def test_search_api_failure_renders_helpful_message(self, _mock_search_games):
        response = self.client.get(reverse("search"), {"q": "result"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Search unavailable")
        self.assertContains(response, "IGDB client ID")

class DeveloperNavigationTests(TestCase):
    def setUp(self):
        self.developer = Developer.objects.create(
            name="Test Studio",
            igdb_id=404,
        )
        self.game = Game.objects.create(
            title="Test Game",
            igdb_id=505,
        )
        self.game.developers.add(self.developer)

    def test_game_detail_links_to_developer(self):
        response = self.client.get(
            reverse("game_detail", args=[self.game.igdb_id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse(
                "developer_detail",
                args=[self.developer.igdb_id],
            ),
        )

    def test_developer_detail_links_to_games(self):
        response = self.client.get(
            reverse(
                "developer_detail",
                args=[self.developer.igdb_id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "games/developer_detail.html",
        )
        self.assertContains(response, self.developer.name)
        self.assertContains(response, self.game.title)
        self.assertContains(
            response,
            reverse("game_detail", args=[self.game.igdb_id]),
        )

    @patch("games.views.search_developers")
    def test_search_can_select_developers(
        self,
        mock_search_developers,
    ):
        mock_search_developers.return_value = [
            {
                "id": 606,
                "name": "Search Studio",
            }
        ]

        response = self.client.get(
            reverse("search"),
            {
                "q": "studio",
                "type": "developers",
            },
        )

        self.assertEqual(response.status_code, 200)
        mock_search_developers.assert_called_once_with("studio")
        self.assertContains(response, "Search Studio")
        self.assertContains(
            response,
            reverse("developer_detail", args=[606]),
        )