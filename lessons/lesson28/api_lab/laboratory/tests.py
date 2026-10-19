from django.test import TestCase, Client
from django.core.management import call_command
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.validation import validate_schema
from rest_framework.test import APIClient
from .models import Category, Product


class ApiContractTests(TestCase):
    def setUp(self):
        call_command("seed_lab", verbosity=0)
        self.client = APIClient()

    def test_create_filter_detail_delete_and_errors(self):
        response = self.client.post("/api/v1/products/", {
            "name": "Test", "price": "12.50", "category": 2,
        }, format="json")
        self.assertEqual(response.status_code, 201)
        pk = response.data["id"]
        filtered = self.client.get("/api/v1/products/?category=2")
        self.assertTrue(all(item["category"] == 2 for item in filtered.data))
        self.assertIn(pk, [item["id"] for item in filtered.data])
        self.assertEqual(self.client.get(f"/api/v1/products/{pk}/").data["name"], "Test")
        self.assertEqual(self.client.get("/api/v1/products/?category=abc").status_code, 400)
        self.assertEqual(self.client.get("/api/v1/products/?category=0").status_code, 400)
        self.assertEqual(self.client.get("/api/v1/products/?category=9999").data, [])
        deleted = self.client.delete(f"/api/v1/products/{pk}/")
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(deleted.content, b"")
        for method in (self.client.get, self.client.delete):
            missing = method(f"/api/v1/products/{pk}/")
            self.assertEqual(missing.status_code, 404)
            self.assertIn("detail", missing.data)

    def test_validation_does_not_save_invalid_product(self):
        original = Product.objects.count()
        for body in [
            {"name": "", "price": "1.00", "category": 1},
            {"name": "X", "price": "-1", "category": 1},
            {"name": "X", "price": "0", "category": 1},
            {"name": "X", "price": "1", "category": 9999},
            {},
        ]:
            with self.subTest(body=body):
                self.assertEqual(self.client.post("/api/v1/products/", body, format="json").status_code, 400)
        self.assertEqual(Product.objects.count(), original)

    def test_sentiment_contract_and_limits(self):
        for text, sentiment in [("Kocham Python!", "positive"), ("fatalny dzień", "negative"), ("tekst", "neutral"), ("super fatalny", "neutral")]:
            response = self.client.post("/api/v1/sentiment/", {"text": text}, format="json")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["sentiment"], sentiment)
            self.assertNotIn("confidence_score", response.data)
        for text in ("", "   ", "a" * 501):
            self.assertEqual(self.client.post("/api/v1/sentiment/", {"text": text}, format="json").status_code, 400)
        self.assertEqual(self.client.post("/api/v1/sentiment/", {"text": "a" * 500}, format="json").status_code, 200)

    def test_schema_matches_operation_contract(self):
        schema = SchemaGenerator().get_schema(request=None, public=True)
        validate_schema(schema)
        paths = schema["paths"]
        listing = paths["/api/v1/products/"]["get"]
        self.assertEqual(listing["parameters"][0]["name"], "category")
        self.assertEqual(set(listing["responses"]), {"200", "400"})
        self.assertEqual(set(paths["/api/v1/products/"]["post"]["responses"]), {"201", "400"})
        delete = paths["/api/v1/products/{id}/"]["delete"]
        self.assertEqual(set(delete["responses"]), {"204", "404"})
        self.assertNotIn("content", delete["responses"]["204"])
        self.assertIn("Pobierz katalog", paths["/api/v1/docstrings/products/"]["get"]["description"])
        self.assertNotIn("description", paths["/api/v1/automatic/products/"]["get"])
        for url in ("/api/schema/?format=json", "/api/schema/swagger-ui/", "/api/schema/redoc/"):
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_seed_preserves_existing_data(self):
        Product.objects.filter(pk=1).update(name="Moja nazwa")
        call_command("seed_lab", verbosity=0)
        self.assertEqual(Product.objects.get(pk=1).name, "Moja nazwa")
        self.assertEqual(Category.objects.count(), 2)

    def test_all_educational_pages_and_source_symbols(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        for number in range(1, 9):
            response = self.client.get(f"/examples/{number}/")
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'id="request-form"')
            self.assertContains(response, 'class="highlight"')
        self.assertEqual(self.client.get("/examples/9/").status_code, 404)

    def test_anonymous_mutations_require_csrf(self):
        browser = Client(enforce_csrf_checks=True)
        body = {"name": "CSRF", "price": "1.00", "category": 1}
        self.assertEqual(browser.post("/api/v1/products/", body, content_type="application/json").status_code, 403)
        browser.get("/examples/5/")
        token = browser.cookies["csrftoken"].value
        created = browser.post("/api/v1/products/", body, content_type="application/json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(created.status_code, 201)
        self.assertEqual(browser.delete(f'/api/v1/products/{created.json()["id"]}/', HTTP_X_CSRFTOKEN=token).status_code, 204)
        swagger = Client(enforce_csrf_checks=True)
        swagger.get("/api/schema/swagger-ui/")
        self.assertIn("csrftoken", swagger.cookies)

    def test_documentation_comparison_comes_from_real_schema(self):
        from .documentation import STAGES, generated_documentation
        stages = generated_documentation()
        first, second, third = stages
        self.assertEqual(first["operations"][0]["description"], "")
        self.assertIn("Katalog sklepu", second["operations"][0]["description"])
        self.assertEqual(third["operations"][0]["summary"], "Obejrzyj katalog sklepu")
        self.assertEqual({r["code"] for r in first["operations"][1]["responses"]}, {"201"})
        self.assertEqual({r["code"] for r in third["operations"][1]["responses"]}, {"201", "400"})
        self.assertEqual({r["code"] for r in third["operations"][2]["responses"]}, {"204", "404"})
        self.assertTrue(third["operations"][1]["examples"])
        for stage in STAGES:
            schema = self.client.get(f'/documentation/{stage["key"]}/schema/?format=json').json()
            validate_schema(schema)
            self.assertEqual(len(schema["paths"]), 2)
            self.assertTrue(all(f'/comparison/{stage["key"]}/' in route for route in schema["paths"]))

    def test_comparison_versions_share_behavior_and_data(self):
        for stage in ("automatic", "docstring", "extended"):
            with self.subTest(stage=stage):
                url = f"/api/v1/comparison/{stage}/products/"
                created = self.client.post(url, {"name": "Comparison", "price": "19.90", "category": 1}, format="json")
                self.assertEqual(created.status_code, 201)
                pk = created.data["id"]
                for other in ("automatic", "docstring", "extended"):
                    self.assertEqual(self.client.get(f"/api/v1/comparison/{other}/products/{pk}/").status_code, 200)
                self.assertEqual(self.client.post(url, {"name": "X", "price": "-1", "category": 1}, format="json").status_code, 400)
                self.assertEqual(self.client.delete(f"{url}{pk}/").status_code, 204)
                self.assertEqual(self.client.delete(f"{url}{pk}/").status_code, 404)
