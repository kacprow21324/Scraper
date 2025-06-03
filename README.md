# 🕸️ Distributed Web Data Harvester

## 📌 Opis projektu

Niniejsza aplikacja to rozproszony system do **automatycznego pobierania, selekcjonowania i przechowywania danych** z witryn internetowych, zgodnie z uprzednio zdefiniowanym **profilem danych**. Celem projektu jest stworzenie skalowalnego i modularnego narzędzia do web scrapingu, które może funkcjonować w środowisku wieloprocesorowym i rozproszonym.

> 🧠 **Ciekawostka od prof. Czyżaka:** Pierwszy znany system zbierający dane z internetu nazywał się „WebCrawler” i powstał w 1994 roku. Dziś każdy z nas może mieć własnego „crawlera” – a jakże, w Pythonie!

## 📋 Zakres funkcjonalności

- ✅ Automatyczne zbieranie danych z internetu na podstawie zadanego profilu
- ✅ Obsługa minimum **4 grup danych**, np.:
  - Adresy email
  - Adresy korespondencyjne
  - Nazwy i struktury organizacyjne
  - Numery telefonów / linki / social media
- ✅ Wieloprocesowe przetwarzanie danych z wykorzystaniem:
  - `multiprocessing` (dystrybucja na rdzenie CPU)
  - `asyncio` (asynchroniczna obsługa I/O)
- ✅ Parsowanie treści przy pomocy `BeautifulSoup`
- ✅ Zapis danych w bazie danych **MongoDB**
- ✅ Interfejs graficzny (webowy) zrealizowany przy użyciu:
  - `Flask` **lub** `Django`

## 🧱 Architektura systemu

Projekt zakłada **modularną, kontenerową architekturę**, która składa się z minimum **3 kontenerów**:

| Moduł             | Opis                                                           |
|------------------|----------------------------------------------------------------|
| 🧠 Silnik         | Komponent odpowiedzialny za scraping, analizę i przetwarzanie danych; uruchamiany w kontenerze z Pythonem i multiprocessing |
| 🌐 Interfejs      | Serwer aplikacji webowej – obsługuje interakcję z użytkownikiem, prezentuje dane i uruchamia zadania scrapujące |
| 🗄️ Baza Danych    | MongoDB w osobnym kontenerze – przechowuje dane w elastycznym formacie dokumentowym (JSON-like) |

> 🔧 Skalowalność:
> - poziom 1: rozbicie procesu na wiele CPU
> - poziom 2: uruchamianie silników scrapujących na wielu maszynach
> - poziom 3: możliwa integracja z klastrami obliczeniowymi (np. z użyciem Celery + Redis)

## 🧪 Technologie

- Python 3.x
- BeautifulSoup
- asyncio, multiprocessing
- Flask / Django
- MongoDB
- Docker, Docker Compose

## 🚀 Uruchamianie aplikacji

```bash
# 1. Klonowanie repozytorium
git clone https://github.com/twoj-uzytkownik/nazwa-repo.git
cd nazwa-repo

# 2. Uruchomienie kontenerów (Docker Compose)
docker-compose up --build
