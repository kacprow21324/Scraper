# 🕸️ Projekt semestralny - Web Scraping
## 📄 Cel projektu

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
| 🗄️ Baza Danych         | Redis                                                       |

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
