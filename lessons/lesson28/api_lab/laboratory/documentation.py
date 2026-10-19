"""Prezentacja danych rzeczywiście wygenerowanych przez drf-spectacular."""
import json
from django.urls import path
from drf_spectacular.generators import SchemaGenerator
from . import comparison_api as api

STAGES = [
    {"key": "automatic", "title": "1. Sam kod", "classes": (api.AutomaticProducts, api.AutomaticProduct),
     "explanation": "Nie dopisaliśmy opisu dokumentacji. Generator rozpoznaje GET, POST i DELETE z klas DRF, a pola produktu z serializera. Nie potrafi sam wyjaśnić celu sklepu ani wszystkich błędów."},
    {"key": "docstring", "title": "2. Dodany docstring", "classes": (api.DocstringProducts, api.DocstringProduct),
     "explanation": "Dopisaliśmy tekst w potrójnym cudzysłowie przy klasie. Generator przenosi go do opisu operacji. To opis napisany przez programistę, automatycznie umieszczony w dokumentacji."},
    {"key": "extended", "title": "3. Dodany @extend_schema", "classes": (api.ExtendedProducts, api.ExtendedProduct),
     "explanation": "Dekorator pozwala nadać osobny tytuł i opis każdej operacji, pokazać przykład notesu oraz wyjaśnić odpowiedzi 400 i 404. @extend_schema_view przypisuje @extend_schema do odziedziczonych metod GET, POST i DELETE."},
]


def patterns_for(stage):
    listing, detail = stage["classes"]
    prefix = f'api/v1/comparison/{stage["key"]}/products/'
    return [path(prefix, listing.as_view()), path(prefix + "<int:pk>/", detail.as_view())]


def resolve(schema, value):
    if "$ref" in value:
        return schema["components"]["schemas"][value["$ref"].rsplit("/", 1)[-1]]
    return value


def fields_for(schema, content, request=False):
    value = content.get("application/json", {}).get("schema", {})
    value = resolve(schema, value)
    if value.get("type") == "array":
        value = resolve(schema, value["items"])
    fields = []
    for name, field in value.get("properties", {}).items():
        field = resolve(schema, field)
        if request and field.get("readOnly"):
            continue
        fields.append({"name": name, "type": field.get("type", "dane"),
                       "required": name in value.get("required", []),
                       "readonly": field.get("readOnly", False),
                       "description": field.get("description", "")})
    return fields


def generated_documentation():
    result = []
    for stage in STAGES:
        schema = SchemaGenerator(patterns=patterns_for(stage)).get_schema(request=None, public=True)
        operations = []
        for method in ("get", "post", "delete"):
            route, operation = next((route, item[method]) for route, item in schema["paths"].items()
                                    if method in item and (method == "delete" or "{" not in route))
            request_content = operation.get("requestBody", {}).get("content", {})
            examples = request_content.get("application/json", {}).get("examples", {})
            operations.append({
                "method": method.upper(), "path": route,
                "summary": operation.get("summary", ""),
                "description": operation.get("description", ""),
                "tags": operation.get("tags", []),
                "input_fields": fields_for(schema, request_content, request=True),
                "examples": [json.dumps(entry.get("value"), ensure_ascii=False, indent=2) for entry in examples.values()],
                "responses": [{"code": code, "description": response.get("description", ""),
                               "fields": fields_for(schema, response.get("content", {})),
                               "empty": not response.get("content")}
                              for code, response in operation["responses"].items()],
            })
        result.append({**stage, "operations": operations})
    return result
