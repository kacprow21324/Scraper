# 🕸️ Projekt semestralny - Web Scraping
> ⚠️ **Uwaga: Scraper jest dostosowany do strony „Books to Scrape” (https://books.toscrape.com).**  
> Scraping danych ze stron bez wyraźnej zgody właściciela jest nieetyczny i może naruszać regulamny serwisu lub prawa autorskie.  

## 👤Autorzy
- Kacper Woszczyło - 21324
- Michał Lepak - 21255 🌈
- Grupa: 1

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

➡️ **Scrapowanie stron poprzez podanie linku**  
   - Użytkownik wkleja URL pierwszej strony (np. `https://books.toscrape.com/catalogue/page-1.html`),  
   - Scraper Master automatycznie odkrywa kolejne strony paginacji,  
   - Informacje szczegółowe (tytuł, cena, dostępność, kategoria, obrazek) są pobierane asynchronicznie i zapisywane w Redis.

➡️ **Sortowanie według potrzeb użytkownika**  
   - Dostępne tryby sortowania:  
     - Nazwa rosnąco (A → Z)  
     - Nazwa malejąco (Z → A)  
     - Cena rosnąco  
     - Cena malejąco  
     - Ilość dostępna rosnąco  
     - Ilość dostępna malejąco  
   - Sortowanie odbywa się po stronie serwera (Flask), na już zebranym zbiorze rekordów.

➡️ **Przeglądanie ponad 1000 książek (i więcej)**  
   - System został zoptymalizowany pod kątem dużej liczby pozycji — Redis zapewnia szybki dostęp do danych,  
   - Frontend wczytuje listę pozycji dynamicznie przy każdym odświeżeniu lub zmianie parametrów sortowania/filtrowania.

➡️ **Wybór kategorii według preferencji użytkownika**  
   - Na stronie WWW jest dostępne pole tekstowe (filtr kategorii),  
   - Użytkownik może wpisać fragment nazwy kategorii (np. „travel”, „science”),  
   - System wyświetli tylko te książki, których kategoria zawiera wpisaną frazę (ignorując wielkość liter).

## 📁 Struktura repozytorium

```bash
Repozytorium:
│───LICENSE
│───PRiR_21324_21255.docx
│───README.md
│
└───Projekt
    │───komendy.txt
    │
    ├───DB
    │    ├──Dockerfile
    │    └──redis.conf
    │
    ├───Interfejs
    │   │───app.py
    │   │───Dockerfile
    │   │───requirements.txt
    │   │
    │   ├───static
    │   │    └───style.css
    │   │
    │   └───templates
    │        └───index.html
    │
    ├───k8s
    │     ├───bd-deployment.yaml
    │     ├───engine-deployment.yaml
    │     ├───interface-deployment.yaml
    │     ├───redis-configmap.yaml
    │     └───redis-pvc.yaml
    │
    └───Silnik
           ├───Dockerfile
           ├───requirements.txt
           ├───scraper_master.py
           └───scraper_worker.py

```
---

## 🧱 Architektura systemu

Projekt zakłada **modularną, kontenerową architekturę**, która składa się z minimum **3 kontenerów**:

| Moduł                    | Opis                                                    |
|-------------------------------------------------------------|-----------------------------------------------------------|
| 🧠 Silnik              | Komponent odpowiedzialny za scraping, analizę i przetwarzanie danych; uruchamiany w kontenerze z Pythonem i multiprocessing |
| 🌐 Interfejs           | Serwer aplikacji webowej – obsługuje interakcję z użytkownikiem, prezentuje dane i uruchamia zadania scrapujące |
| 🗄️ Baza Danych (Redis)ㅤㅤㅤ| In-memory store – przechowuje dane w strukturach klucz-wartość; może pełnić rolę bufora, kolejki zadań, cache’u lub tymczasowego magazynu wyników  |

## 🧪 Technologie

- Python 3.x
- BeautifulSoup
- asyncio, multiprocessing
- Flask 
- Redis
- Docker
- Kuberneter
- HTML && CSS
- json
- os
- time

## 🚀 Uruchamianie aplikacji

```bash
# 1. Włączyć Kubernetes w Docker Desktop (GUI).

# 2. Zbudować obraz Redis:
cd Projekt/DB
docker build -t projekt-redis:latest .

# 3. Zbudować obraz Silnika:
cd ../Silnik
docker build -t projekt-silnik:latest .

# 4. Zbudować obraz Interfejs:
cd ../Interfejs
docker build -t projekt-interfejs:latest .

# 5. Wdróżyć manifesty w Kubernetes:
cd ../k8s
kubectl apply -f redis-configmap.yaml
kubectl apply -f redis-pvc.yaml
kubectl apply -f bd-deployment.yaml
kubectl apply -f engine-deployment.yaml
kubectl apply -f interface-deployment.yaml

# 6. Sprawdzić, czy pody działają:
kubectl get pods
kubectl get svc

# (opcjonalnie) 7. Jeżeli chcesz wyczyścić Redis przed nowym scrapowaniem:
kubectl exec deployment/redis -- redis-cli FLUSHALL

# 8. Wejść na interfejs w przeglądarce:
http://localhost:30000

# 9. Podać dowolny URLi kliknąć "Scrapuj".
https://books.toscrape.com/

# 10. Śledzić logi silnika, aby zobaczyć postęp:
kubectl logs -f deployment/scraper-engine

# 11. Po zakończeniu scrappingu odświeżyć stronę w przeglądarce i zobacz wyniki.
```
## 📝 Podsumowanie

---

## 📬 Kontakt

W razie pytań:
- Email:   21324@student.ans-elblag.pl
- GitHub:  https://github.com/kacprow21324

---

**Licencja:** [`MIT`](./LICENSE.md)   
