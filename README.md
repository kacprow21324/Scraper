# 🕸️ Projekt semestralny - Web Scraping
## 📄 Cel projektu
1. Aplikacja pobiera, selekcjonuje i składuje  wybranedane o narzuconym profilu z witryn internetowych.
2. Profil danych jest ustalony przez realizującego projekt. Profil danych powinien obejmować min. 4 grupy, np. adresy email, adresy korespondencyjne, schemat organizacyjny itp.
3. Program wykorzystuje wielowątkowość/wieloprocesowość. Silnik należy zrealizować we własnym zakresie wykorzystując: multiprocessing i asyncio. Przetwarzanie ma być wieloprocesowe, najlepiej z możliwością skalowania na rdzenie procesora, dalej na komputery, dalej na klastry itp.
4. Do parsowania kontentu należy użyć beautifulsoup.
5. Dane mają być zapisywane w BD, np. MongoDB
6. Program ma posiadać interfejs graficzny zrealizowany w Python (Flask lub Django)
7. Docelowo aplikacja ma być rozproszona na min 3 moduły: interfejs (1 lub więcej kontenerów), silnik (1 kontener), BD (1 kontener). Sposób ulokowania należy opracować we własnym zakresie i potrafić uzasadnić wybory.
8. Oprogramowanie może być zrealizowane w grupie 1 lub 2 osobowej.
9. Projekt uznaje się za złożony, jeżeli w wyznaczonym terminie zostanie opublikowany szczegółowy raport z dowiązaniem do repozytorium kodu (github) oraz zostanie zademonstrowany prowadzącemu na ostatnich zajęciach laboratoryjnych.
## 📌 Opis projektu
Niniejsza aplikacja to rozproszony system do **automatycznego pobierania, selekcjonowania i przechowywania danych** z witryn internetowych, zgodnie z uprzednio zdefiniowanym **profilem danych**. Celem projektu jest stworzenie skalowalnego i modularnego narzędzia do web scrapingu, które może funkcjonować w środowisku wieloprocesorowym i rozproszonym.

## 📋 Zakres funkcjonalności

- ✅ Tytuł
- ✅ Kategoria
- ✅ Cena
- ✅ Ilość
 

## 🧱 Architektura systemu

Projekt zakłada **modularną, kontenerową architekturę**, która składa się z minimum **3 kontenerów**:

| Moduł                    | Opis                                                    |
|-------------------------------------------------------------|-----------------------------------------------------------|
| 🧠 Silnik              | Komponent odpowiedzialny za scraping, analizę i przetwarzanie danych; uruchamiany w kontenerze z Pythonem i multiprocessing |
| 🌐 Interfejs           | Serwer aplikacji webowej – obsługuje interakcję z użytkownikiem, prezentuje dane i uruchamia zadania scrapujące |
| 🗄️ Baza Danych (Redis)        | In-memory store – przechowuje dane w strukturach klucz-wartość; może pełnić rolę bufora, kolejki zadań, cache’u lub tymczasowego magazynu wyników  |

## 🧪 Technologie

- Python 3.x
- BeautifulSoup
- asyncio, multiprocessing
- Flask
- Redis
- Docker
- Kuberneter
## 📝 Podsumowanie
## 🚀 Uruchamianie aplikacji

```bash
# 1. Klonowanie repozytorium
git clone https://github.com/twoj-uzytkownik/nazwa-repo.git
cd nazwa-repo

# 2. Uruchomienie kontenerów (Docker Compose)
docker-compose up --build
