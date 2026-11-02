"""ElevenLabs narration for the fixed task-7 script; API keys stay in Python.

Only the first generation contacts TTS. Content-addressed MP3 files are reused.
Uses the standard library so the course environments need no new dependencies.
"""

import hashlib
import json
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".runtime" / "narration"
API = "https://api.elevenlabs.io"
VOICE_SETTINGS = {
    "stability": 0.45,
    "similarity_boost": 0.75,
    "style": 0.15,
    "use_speaker_boost": True,
}
LOCK = threading.Lock()
VOICE_LOCK = threading.Lock()
VOICE_CACHE = {}


class NarrationError(Exception):
    def __init__(self, message, status=503):
        super().__init__(message)
        self.status = status


def config():
    """Read environment first, then local .env. Re-read so editing needs no restart."""
    values = {}
    for path in (ROOT.parents[1] / ".env", ROOT / ".env"):
        if path.exists():
            for line in path.read_text(encoding="utf-8-sig").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.removeprefix("export ").split("=", 1)
                values[key.strip()] = value.strip().strip("\"'")
    for key in ("ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID", "ELEVENLABS_MODEL_ID"):
        if os.environ.get(key):
            values[key] = os.environ[key]
    return {
        "key": values.get("ELEVENLABS_API_KEY", ""),
        "voice": values.get("ELEVENLABS_VOICE_ID", ""),
        "model": values.get("ELEVENLABS_MODEL_ID") or "eleven_multilingual_v2",
    }


def provider_request(path, cfg, payload=None):
    if not cfg["key"]:
        raise NarrationError(
            "Dodaj ELEVENLABS_API_KEY do lessons/lesson34/.env i odśwież głosy.", 503
        )
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        API + path,
        data=body,
        headers={
            "xi-api-key": cfg["key"],
            "Content-Type": "application/json",
            "Accept": "audio/mpeg" if payload is not None else "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=75) as response:
            data = response.read(10 * 1024 * 1024 + 1)
            if len(data) > 10 * 1024 * 1024:
                raise NarrationError("Odpowiedź ElevenLabs przekracza limit nagrania.")
            return data
    except urllib.error.HTTPError as error:
        # Only translate known error codes; never return raw provider bodies.
        try:
            detail = json.loads(error.read(16384)).get("detail", {})
            reason = detail.get("status") if isinstance(detail, dict) else None
        except (ValueError, OSError, AttributeError):
            reason = None
        reasons = {
            "detected_unusual_activity": "ElevenLabs zablokował generowanie: detected_unusual_activity. Sprawdź komunikaty i weryfikację konta w panelu ElevenLabs.",
            "quota_exceeded": "Wykorzystano limit generowania ElevenLabs na tym koncie lub kluczu.",
            "insufficient_credits": "Konto ElevenLabs nie ma wystarczającego limitu na to nagranie.",
            "missing_permissions": "Klucz ElevenLabs wymaga Text to Speech: Dostęp i Głosy: Przeczytane.",
        }
        if reason in reasons:
            raise NarrationError(reasons[reason], 502) from None
        messages = {
            401: "ElevenLabs odrzucił klucz API. Sprawdź ELEVENLABS_API_KEY.",
            403: "ElevenLabs odmówił dostępu. Sprawdź uprawnienia klucza, głosu oraz limit konta.",
            402: "Brak środków lub limitu generowania na koncie ElevenLabs.",
            404: "Nie znaleziono głosu lub modelu ElevenLabs.",
            422: "ElevenLabs odrzucił ustawienia głosu lub modelu.",
            429: "ElevenLabs zgłosił limit żądań lub wykorzystania konta. Spróbuj później.",
        }
        raise NarrationError(
            messages.get(error.code, f"ElevenLabs zwrócił błąd HTTP {error.code}."), 502
        ) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise NarrationError(
            "Nie można połączyć się z ElevenLabs. Sprawdź połączenie i spróbuj ponownie.",
            502,
        ) from None


def voices(cfg):
    def saved():
        try:
            return json.loads((CACHE / "voices.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return []

    if not cfg["key"]:
        return saved()
    fingerprint = hashlib.sha256(cfg["key"].encode()).hexdigest()
    with VOICE_LOCK:
        cached = VOICE_CACHE.get(fingerprint)
        if cached and time.monotonic() - cached[0] < 300:
            return cached[1]
        result, page = [], None
        for _ in range(10):
            query = {"page_size": 100}
            if page:
                query["next_page_token"] = page
            try:
                try:
                    data = json.loads(
                        provider_request(
                            "/v2/voices?" + urllib.parse.urlencode(query), cfg
                        )
                    )
                except NarrationError:
                    if saved():
                        return saved()
                    raise
                for voice in data.get("voices", []):
                    result.append(
                        {
                            "id": voice["voice_id"],
                            "name": voice.get("name") or voice["voice_id"],
                            "language": voice.get("labels", {}).get("language", ""),
                        }
                    )
                if not data.get("has_more"):
                    break
                page = data.get("next_page_token")
                if not page:
                    break
            except (ValueError, KeyError, TypeError):
                raise NarrationError(
                    "Nieprawidłowa lista głosów z ElevenLabs.", 502
                ) from None
        # Account defaults omit the Polish catalog. Read Polish library metadata
        # without modifying My Voices or requesting broader key permissions.
        try:
            shared = json.loads(
                provider_request(
                    "/v1/shared-voices?language=pl&page_size=30&sort=cloned_by_count",
                    cfg,
                )
            )
            for voice in shared.get("voices", []):
                if (
                    voice.get("language") == "pl"
                    and voice.get("free_users_allowed") is True
                ):
                    result.append(
                        {
                            "id": voice["voice_id"],
                            "name": voice["name"],
                            "language": "pl",
                            "source": "library",
                        }
                    )
        except (NarrationError, ValueError, KeyError, TypeError):
            # Existing Polish account voices remain usable if the catalog is down.
            pass
        result = list({v["id"]: v for v in result}.values())
        VOICE_CACHE.clear()
        VOICE_CACHE[fingerprint] = (time.monotonic(), result)
        CACHE.mkdir(parents=True, exist_ok=True)
        (CACHE / "voices.json").write_text(
            json.dumps(result, ensure_ascii=False), encoding="utf-8"
        )
        return result


def public_config(language="pl"):
    if language not in {"pl", "en"}:
        raise NarrationError("Nieznany język listy głosów.", 400)
    cfg = config()
    available = [
        v
        for v in voices(cfg)
        if v.get("language", "").lower().split("-")[0] == language
    ]
    preferred = cfg["voice"]
    if preferred not in {v["id"] for v in available}:
        preferred = next(
            (v["id"] for v in available if v["name"].startswith("Piotr - Engaging")),
            available[0]["id"] if available else "",
        )
    return {
        "configured": bool(cfg["key"]),
        "voices": available,
        "default_voice_id": preferred,
        "language": language,
        "model": cfg["model"],
        "cached_available": CACHE.exists() and any(CACHE.glob("*.mp3")),
    }


def clip_parameters(language, step, voice_id, cfg):
    if language not in {"pl", "en"} or type(step) is not int or not 0 <= step < 12:
        raise NarrationError("Nieznany język lub klatka prezentacji.", 400)
    if not isinstance(voice_id, str) or not re.fullmatch(
        r"[A-Za-z0-9_-]{1,100}", voice_id
    ):
        raise NarrationError("Wybierz prawidłowy głos ElevenLabs.", 400)
    script = json.loads(
        (ROOT / "static" / "narrated-script.json").read_text(encoding="utf-8")
    )
    return {
        "text": script[step]["text"][0 if language == "pl" else 1],
        "model_id": cfg["model"],
        "voice_settings": VOICE_SETTINGS,
    }


def generate(language, step, voice_id):
    cfg = config()
    payload = clip_parameters(language, step, voice_id, cfg)
    digest = hashlib.sha256(
        json.dumps(
            {
                "voice": voice_id,
                "language": language,
                "format": "mp3_44100_128",
                "payload": payload,
            },
            sort_keys=True,
            ensure_ascii=False,
        ).encode()
    ).hexdigest()
    target = CACHE / f"{digest}.mp3"
    # Serialize paid generation. A double click cannot buy the same clip twice.
    with LOCK:
        if target.is_file() and target.stat().st_size:
            return {"url": f"/api/narration/audio/{digest}", "cached": True}
        available = voices(cfg)
        if not cfg["key"]:
            raise NarrationError(
                "Dodaj ELEVENLABS_API_KEY do lessons/lesson34/.env i odśwież głosy."
            )
        if voice_id not in {
            v["id"]
            for v in available
            if v.get("language", "").lower().split("-")[0] == language
        }:
            raise NarrationError(
                "Ten głos nie jest dostępny na Twoim koncie ElevenLabs.", 400
            )
        audio = provider_request(
            f"/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128", cfg, payload
        )
        if not audio or not (audio.startswith(b"ID3") or audio[0] == 0xFF):
            raise NarrationError("ElevenLabs nie zwrócił poprawnego nagrania MP3.", 502)
        CACHE.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(".tmp")
        temporary.write_bytes(audio)
        temporary.replace(target)
        return {"url": f"/api/narration/audio/{digest}", "cached": False}


def config_view(request):
    from django.http import HttpResponseNotAllowed, JsonResponse

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    try:
        if request.GET.get("refresh") == "1":
            with VOICE_LOCK:
                VOICE_CACHE.clear()
        return JsonResponse(public_config(request.GET.get("language", "pl")))
    except NarrationError as error:
        return JsonResponse({"error": str(error)}, status=error.status)


def generate_view(request):
    from django.http import HttpResponseNotAllowed, JsonResponse

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        body = json.loads(request.body)
        if not isinstance(body, dict) or set(body) != {"language", "step", "voice_id"}:
            raise NarrationError(
                "Oczekiwano language, step i voice_id; tekst pochodzi ze scenariusza.",
                400,
            )
        return JsonResponse(generate(body["language"], body["step"], body["voice_id"]))
    except (ValueError, TypeError):
        return JsonResponse({"error": "Nieprawidłowe dane żądania."}, status=400)
    except NarrationError as error:
        return JsonResponse({"error": str(error)}, status=error.status)


def audio_view(request, digest):
    from django.http import FileResponse, Http404, HttpResponseNotAllowed

    if request.method not in {"GET", "HEAD"}:
        return HttpResponseNotAllowed(["GET", "HEAD"])
    if not re.fullmatch("[0-9a-f]{64}", digest):
        raise Http404
    target = CACHE / f"{digest}.mp3"
    if not target.is_file():
        raise Http404
    response = FileResponse(target.open("rb"), content_type="audio/mpeg")
    response["Cache-Control"] = "private, max-age=31536000, immutable"
    return response
