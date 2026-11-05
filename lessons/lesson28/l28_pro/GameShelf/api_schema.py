from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse


DETAIL_ERROR = {
    "type": "object",
    "required": ["detail"],
    "properties": {"detail": {"type": "string"}},
}
FIELD_ERRORS = {"type": "object", "additionalProperties": {"type": "array", "items": {"type": "string"}}}
NOT_FOUND = OpenApiResponse(DETAIL_ERROR, description="The requested resource was not found.")
FORBIDDEN = OpenApiResponse(
    DETAIL_ERROR, description="Sign in first. For writes, the session must also have a valid CSRF token."
)
INVALID_FILTER = OpenApiResponse(FIELD_ERRORS, description="Invalid filter value, keyed by field.")
CATALOG_PARAMETERS = [
    OpenApiParameter("q", {"type": "string", "maxLength": 120}, description="Title contains this text (case-insensitive)."),
    OpenApiParameter(
        "genre", str, description="Genre slug from GET /api/v1/genres/.",
        examples=[OpenApiExample("Seeded FAKE games", value="fake")],
    ),
    OpenApiParameter(
        "tag", str, description="Tag slug from GET /api/v1/tags/.",
        examples=[OpenApiExample("Seeded FAKE games", value="fake")],
    ),
]
