# Najciekawsze bloki kodu GameShelf

> Plik generowany przez `update_docs.py`. Status pochodzi z `roadmap_done.md`, a fragmenty kodu i numery linii z aktualnych plików. Opisy PL: `docs_pl_data.py`.

To rzeczywisty kod projektu, nie uproszczone kopie. Numery linii i treść są odświeżane przez generator.

## Edycja przez REST API

Źródło: [l28_pro/GameShelf/api.py — LibraryDetail.patch](l28_pro/GameShelf/api.py#L114).

```python
    @extend_schema(
        tags=["My library"], summary="Update my saved game",
        description="Ratings are 1–10 or null. You can move wishlist to owned, but not owned to wishlist.",
        request=LibraryUpdateSerializer(partial=True),
        responses={200: LibraryEntrySerializer, 400: INVALID_ENTRY, 403: FORBIDDEN, 404: NOT_FOUND},
        examples=[
            OpenApiExample("Move to owned", value={"list_type": "owned"}, request_only=True),
            OpenApiExample("Rate a completed game", value={"play_status": "completed", "rating": 9}, request_only=True),
            OpenApiExample("Rating outside range", value={"rating": ["Ensure this value is less than or equal to 10."]},
                           response_only=True, status_codes=["400"]),
        ],
    )
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        entry = self.get_object()
        serializer = LibraryUpdateSerializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(self.get_serializer(serializer.save()).data)
```

Widok pobiera wpis z kolekcji ograniczonej do request.user. Transakcja obejmuje blokadę edytowanego wiersza, walidację zmian i zapis. partial=True pozwala wysłać tylko zmieniane pola; opis OpenAPI rozdziela dane wejściowe i odpowiedź.

## Import zewnętrznej okładki

Źródło: [l28_pro/GameShelf/management/commands/import_games.py — download_cover](l28_pro/GameShelf/management/commands/import_games.py#L37).

```python
def download_cover(url):
    if not isinstance(url, str):
        raise ValueError("Invalid image URL")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "media.rawg.io":
        raise ValueError("Unsupported image host")
    with requests.get(url, stream=True, timeout=(5, 20), allow_redirects=False) as response:
        if response.status_code != 200:
            raise ValueError("Image request failed")
        content = bytearray()
        for chunk in response.iter_content(64 * 1024):
            content.extend(chunk)
            if len(content) > MAX_IMAGE_BYTES:
                raise ValueError("Image is too large")
    with Image.open(BytesIO(content)) as image:
        extension = IMAGE_TYPES.get(image.format)
        if not extension or image.width * image.height > 20_000_000:
            raise ValueError("Unsupported image format or dimensions")
        image.verify()
    return extension, ContentFile(bytes(content))
```

Pobieranie dopuszcza wyłącznie znany host HTTPS, bez przekierowań. Limit bajtów i weryfikacja Pillow chronią przed błędnymi plikami, a ContentFile pozwala zapisać dane w ImageField.

## Relacje i ograniczenia bazy

Źródło: [l28_pro/GameShelf/models.py — UserGame](l28_pro/GameShelf/models.py#L69).

```python
class UserGame(models.Model):
    class PlayStatus(models.TextChoices):
        NOT_STARTED = "not_started", "Not started"
        PLAYING = "playing", "Playing"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"

    class ListType(models.TextChoices):
        OWNED = "owned", "Owned"
        WISHLIST = "wishlist", "Wishlist"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_entries",
    )
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="library_entries"
    )
    list_type = models.CharField(
        max_length=8, choices=ListType.choices, default=ListType.OWNED
    )
    play_status = models.CharField(
        max_length=11,
        choices=PlayStatus.choices,
        default=PlayStatus.NOT_STARTED,
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    note = models.TextField(blank=True, max_length=5000)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "game"), name="unique_user_game"
            ),
            models.CheckConstraint(
                condition=models.Q(list_type__in=("owned", "wishlist")),
                name="valid_user_game_list_type",
            ),
            models.CheckConstraint(
                condition=models.Q(rating__isnull=True)
                | models.Q(rating__gte=1, rating__lte=10),
                name="user_game_rating_1_to_10",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    play_status__in=(
                        "not_started",
                        "playing",
                        "completed",
                        "abandoned",
                    )
                ),
                name="valid_user_game_play_status",
            ),
        ]

    def can_move_to(self, list_type):
        return not (self.list_type == self.ListType.OWNED and list_type == self.ListType.WISHLIST)

    def __str__(self):
        return f"{self.user} - {self.game} ({self.get_list_type_display()})"
```

ForeignKey łączy wpis z użytkownikiem i grą. TextChoices nadaje czytelne nazwy stałym. UniqueConstraint pilnuje jednej pary użytkownik–gra, a CheckConstraint chroni oceny i status także przy bezpośrednim zapisie ORM. Walidacja formularza i ograniczenie bazy uzupełniają się.

## Wyszukiwanie i filtry w jednym miejscu

Źródło: [l28_pro/GameShelf/views.py — filtered_games](l28_pro/GameShelf/views.py#L33).

```python
def filtered_games(params):
    """Share search and filter rules between the catalog and live suggestions."""
    games = Game.objects.select_related("studio").order_by("title", "pk")
    filter_form = CatalogFilterForm(params)
    if filter_form.is_valid():
        query = filter_form.cleaned_data["q"]
        if query:
            games = games.filter(title__icontains=query)
        genre = filter_form.cleaned_data["genre"]
        if genre:
            games = games.filter(genres=genre)
        tag = filter_form.cleaned_data["tag"]
        if tag:
            games = games.filter(tags=tag)
    else:
        games = games.none()
    return games, filter_form
```

Formularz najpierw sprawdza parametry URL. cleaned_data zawiera już prawidłowe obiekty gatunku/tagu. Kolejne filter łączą warunki przez AND. select_related pobiera studio razem z grą, zamiast wykonywać dodatkowe zapytanie dla każdej karty.

## Trzy podpowiedzi z bazy

Źródło: [l28_pro/GameShelf/views.py — game_suggestions](l28_pro/GameShelf/views.py#L59).

```python
@require_GET
def game_suggestions(request):
    games, filter_form = filtered_games(request.GET)
    if not filter_form.is_valid() or not filter_form.cleaned_data["q"]:
        return JsonResponse({"results": []})
    results = [
        {
            "title": game.title,
            "url": reverse("gameshelf:game_detail", args=[game.pk]),
        }
        for game in games[:3]
    ]
    return JsonResponse({"results": results})
```

Widok współdzieli zasady wyszukiwania z katalogiem i odpowiada JSON-em. games[:3] ogranicza wyniki na poziomie SQL. reverse buduje adres szczegółów bez wpisywania go na sztywno. To mały endpoint Django, nie API z DRF ani dokumentacja OpenAPI.

## Lista dozwolonych pól formularza

Źródło: [l28_pro/GameShelf/forms.py — UserGameEditForm](l28_pro/GameShelf/forms.py#L42).

```python
class UserGameEditForm(forms.ModelForm):
    class Meta:
        model = UserGame
        fields = ("play_status", "rating", "note")
        labels = {"note": "Private note"}
        help_texts = {
            "rating": "Rate from 1 to 10, or leave blank.",
            "note": "Only you can see this note in your library (up to 5000 characters).",
        }
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10}),
            "note": forms.Textarea(attrs={"rows": 5}),
        }
```

ModelForm bierze walidatory i typy z modelu. Jawne fields ogranicza edycję do statusu, oceny i notatki: przesłanie user lub game w POST nie przeniesie wpisu na inną osobę.

## Sprawdzenie właściciela przed edycją

Źródło: [l28_pro/GameShelf/views.py — edit_library_entry](l28_pro/GameShelf/views.py#L147).

```python
@login_required
@require_http_methods(["GET", "POST"])
def edit_library_entry(request, pk):
    entry = get_object_or_404(
        UserGame.objects.select_related("game"), pk=pk, user=request.user
    )
    form = UserGameEditForm(
        request.POST if request.method == "POST" else None, instance=entry
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request, f"Your entry for {entry.game.title} has been updated."
        )
        return redirect("gameshelf:my_library")
    return render(
        request, "edit_library_entry.html", {"entry": entry, "form": form}
    )
```

get_object_or_404 filtruje jednocześnie po pk i request.user. Użytkownik nie może otworzyć cudzego wpisu nawet znając jego ID. Po prawidłowym POST następuje przekierowanie, co ogranicza przypadkowe ponowne wysłanie formularza.

## GET potwierdza, POST usuwa

Źródło: [l28_pro/GameShelf/views.py — remove_library_entry](l28_pro/GameShelf/views.py#L167).

```python
@login_required
@require_http_methods(["GET", "POST"])
def remove_library_entry(request, pk):
    entry = get_object_or_404(
        UserGame.objects.select_related("game"), pk=pk, user=request.user
    )
    if request.method == "POST":
        title = entry.game.title
        entry.delete()
        messages.success(
            request, f"{title} has been removed from your library."
        )
        return redirect("gameshelf:my_library")
    return render(request, "remove_library_entry.html", {"entry": entry})
```

Odczyt strony potwierdzenia niczego nie zmienia. Usunięcie jest wewnątrz warunku POST, po sprawdzeniu właściciela. Usuwany jest UserGame, a nie publiczny Game. Formularz szablonu dodatkowo przesyła token CSRF.

## Liczniki w jednym zapytaniu

Źródło: [l28_pro/GameShelf/admin.py — GameAdmin](l28_pro/GameShelf/admin.py#L50).

```python
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "studio", "release_date", "saved_by")
    list_editable = ("release_date",)
    search_fields = ("title", "studio__name", "seed_key")
    list_filter = ("studio", "genres", "tags", "release_date")
    filter_horizontal = ("genres", "tags")
    list_select_related = ("studio",)
    ordering = ("title", "pk")
    autocomplete_fields = ("studio",)
    readonly_fields = ("seed_key", "saved_by")
    inlines = (UserGameInline,)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(_saved_by=Count("library_entries", distinct=True))
        )

    @admin.display(description="Saved by users", ordering="_saved_by")
    def saved_by(self, obj):
        return getattr(obj, "_saved_by", 0)
```

annotate i Count obliczają licznik zapisów razem z danymi gry. distinct zapobiega zawyżaniu wyniku przy łączeniu relacji. Dekorator admin.display umożliwia sortowanie po obliczonej kolumnie; inline pozwala edytować powiązane wpisy.

## Powtarzalne biblioteki testowe

Źródło: [l28_pro/GameShelf/management/commands/seed_db.py — Command.seed_libraries](l28_pro/GameShelf/management/commands/seed_db.py#L115).

```python
    def seed_libraries(self, users, games, count, fake, seed):
        created_count = 0
        for number, user in enumerate(users, start=1):
            fake.seed_instance(seed + 30000 + number)
            for index, game in enumerate(games[:count]):
                list_type = UserGame.ListType.WISHLIST
                status = UserGame.PlayStatus.NOT_STARTED
                rating = None
                if index % 2 == 0:
                    list_type = UserGame.ListType.OWNED
                    status = fake.random_element(UserGame.PlayStatus.values)
                    if status in (
                        UserGame.PlayStatus.COMPLETED,
                        UserGame.PlayStatus.PLAYING,
                    ):
                        rating = fake.random_int(min=1, max=10)
                _, created = UserGame.objects.get_or_create(
                    user=user,
                    game=game,
                    defaults={
                        "list_type": list_type,
                        "play_status": status,
                        "rating": rating,
                        "note": f"FAKE demo note: {fake.sentence(nb_words=8)}",
                    },
                )
                created_count += int(created)
        return created_count
```

seed_instance odtwarza te same losowania. get_or_create szuka istniejącej pary użytkownik–gra, a defaults stosuje tylko przy tworzeniu. Ponowne uruchomienie nie nadpisuje notatek i ocen. Wyższe --entries-per-user dodaje brakujące wpisy.

## Okładka albo bezpieczny placeholder

Źródło: [l28_pro/GameShelf/models.py — Game.cover_url](l28_pro/GameShelf/models.py#L58).

```python
    @property
    def cover_url(self):
        """Use a static cover when no file was uploaded or the file is missing."""
        if self.cover and self.cover.storage.exists(self.cover.name):
            return self.cover.url
        return static("GameShelf/cover-placeholder.svg")
```

@property pozwala szablonowi czytać cover_url jak atrybut. Sam niepusty zapis ImageField nie gwarantuje, że plik nadal istnieje. storage.exists sprawdza plik; static wskazuje wersjonowany zasób projektu przy braku obrazu.

## Test prawdziwego uploadu do admina

Źródło: [l28_pro/GameShelf/test_covers.py — CoverUploadTests.test_admin_upload_stores_file_path_and_displays_cover](l28_pro/GameShelf/test_covers.py#L53).

```python
    def test_admin_upload_stores_file_path_and_displays_cover(self):
        response = self.client.post(
            reverse("admin:GameShelf_game_add"),
            self.admin_data(cover=uploaded_cover()),
        )
        self.assertEqual(response.status_code, 302)
        game = Game.objects.get(title="Uploaded cover game")
        self.assertTrue(game.cover.name.startswith("covers/"))
        self.assertTrue(Path(game.cover.path).is_file())
        with Image.open(game.cover.path) as image:
            self.assertEqual(image.size, (240, 360))
        for url in (
            reverse("gameshelf:game_list"),
            reverse("gameshelf:game_detail", args=[game.pk]),
        ):
            self.assertContains(self.client.get(url), game.cover.url)
```

Test przesyła rzeczywisty PNG jako plik formularza, sprawdza przekierowanie, ścieżkę w bazie, plik na dysku i HTML obu widoków. TemporaryDirectory w setUp izoluje pliki testowe od rzeczywistych okładek.

## Test całego przepływu z CSRF

Źródło: [l28_pro/GameShelf/test_workflows.py — PlayerWorkflowTests.test_register_discover_save_edit_remove_and_logout](l28_pro/GameShelf/test_workflows.py#L58).

```python
    def test_register_discover_save_edit_remove_and_logout(self):
        detail = reverse("gameshelf:game_detail", args=[self.game.pk])
        response = self.client.get(
            reverse("gameshelf:game_list"),
            {
                "q": "Orbit",
                "genre": "action",
                "tag": "singleplayer",
            },
        )
        self.assertContains(response, self.game.title)
        self.assertContains(response, "cover-placeholder.svg")
        client = self.register_and_login("workflow_player")
        wishlist = reverse("gameshelf:add_to_wishlist", args=[self.game.pk])
        self.assertRedirects(
            self.post_form(client, wishlist, form_url=detail), detail
        )
        entry = UserGame.objects.get()
        original_pk = entry.pk
        self.assertEqual(entry.list_type, "wishlist")
        self.post_form(client, wishlist, form_url=detail)
        self.assertEqual(UserGame.objects.count(), 1)
        self.post_form(
            client,
            reverse("gameshelf:add_to_owned", args=[self.game.pk]),
            form_url=detail,
        )
        entry.refresh_from_db()
        self.assertEqual((entry.pk, entry.list_type), (original_pk, "owned"))
        edit_url = reverse("gameshelf:edit_library_entry", args=[entry.pk])
        response = self.post_form(
            client,
            edit_url,
            {
                "play_status": "completed",
                "rating": 10,
                "note": "Workflow private note",
            },
        )
        self.assertRedirects(response, reverse("gameshelf:my_library"))
        self.assertContains(
            client.get(reverse("gameshelf:my_library")), "Workflow private note"
        )
        self.assertNotContains(self.client.get(detail), "Workflow private note")
        remove_url = reverse("gameshelf:remove_library_entry", args=[entry.pk])
        self.assertRedirects(
            self.post_form(client, remove_url), reverse("gameshelf:my_library")
        )
        self.assertFalse(UserGame.objects.exists())
        self.assertTrue(Game.objects.filter(pk=self.game.pk).exists())
        response = self.post_form(
            client,
            reverse("gameshelf:logout"),
            form_url=reverse("gameshelf:my_library"),
        )
        self.assertRedirects(response, reverse("gameshelf:home"))
        self.assertNotIn("_auth_user_id", client.session)
```

Zwykłe testy Django domyślnie pomijają sprawdzanie CSRF. Tutaj Client(enforce_csrf_checks=True) i helper post_form korzystają z prawdziwych ciasteczek i tokenów. Test łączy rejestrację, sesję, wishlistę, owned, edycję, usuwanie i wylogowanie.

