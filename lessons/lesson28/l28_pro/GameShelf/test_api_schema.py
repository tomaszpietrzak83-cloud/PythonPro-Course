from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse


class APISchemaTests(TestCase):
    def test_schema_matches_read_api(self):
        response = self.client.get(reverse("api-schema"), HTTP_ACCEPT="application/vnd.oai.openapi+json")
        self.assertEqual(response.status_code, 200)
        schema = response.json()
        games = schema["paths"]["/api/v1/games/"]["get"]
        self.assertEqual({p["name"] for p in games["parameters"]}, {"q", "genre", "tag"})
        self.assertIn("400", games["responses"])
        library = schema["paths"]["/api/v1/library/"]["get"]
        self.assertIn("403", library["responses"])
        self.assertEqual(library["security"], [{"cookieAuth": []}])
        paths = schema["paths"]
        create = paths["/api/v1/library/"]["post"]
        self.assertEqual(set(create["responses"]), {"201", "400", "403"})
        examples = create["requestBody"]["content"]["application/json"]["examples"]
        self.assertIn({"game": 1, "list_type": "wishlist"}, [item["value"] for item in examples.values()])
        entry = paths["/api/v1/library/{id}/"]
        self.assertEqual(set(entry), {"get", "patch", "delete"})
        self.assertEqual(set(entry["patch"]["responses"]), {"200", "400", "403", "404"})
        self.assertEqual(set(entry["delete"]["responses"]), {"204", "403", "404"})

    def test_swagger_and_redoc_load_local_assets(self):
        for name, asset in (
            ("swagger-ui", "drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-bundle.js"),
            ("redoc", "drf_spectacular_sidecar/redoc/bundles/redoc.standalone.js"),
        ):
            self.assertIsNotNone(finders.find(asset))
            self.assertContains(self.client.get(reverse(name)), asset)

    def test_swagger_offers_login_and_sets_csrf_cookie(self):
        response = self.client.get(reverse("swagger-ui"))
        self.assertContains(response, "Sign in to test your library")
        self.assertIn("csrftoken", response.cookies)
