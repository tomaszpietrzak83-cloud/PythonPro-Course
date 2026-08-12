# Importuje klase Path z modulu pathlib, aby tworzyc foldery w wygodny sposob.
from pathlib import Path

# Ustalam folder, w ktorym znajduje sie ten skrypt.
folder_skryptu = Path(__file__).resolve().parent

# Tworze sciezke do glownego folderu Projekt.
folder_projektu = folder_skryptu / "Projekt"

# Tworze liste folderow, ktore maja zostac utworzone wewnatrz projektu.
foldery_do_utworzenia = [
    # Dodaje folder src do listy folderow.
    folder_projektu / "src",
    # Dodaje folder data do listy folderow.
    folder_projektu / "data",
    # Dodaje folder docs do listy folderow.
    folder_projektu / "docs",
]

# Przechodze po kazdym folderze z listy.
for folder in foldery_do_utworzenia:
    # Tworze dany folder oraz brakujace foldery nadrzedne, jesli jeszcze nie istnieja.
    folder.mkdir(parents=True, exist_ok=True)

# Wyswietlam komunikat informujacy, ze struktura folderow zostala utworzona.
print("Struktura folderow Projekt/src, Projekt/data i Projekt/docs zostala utworzona.")

