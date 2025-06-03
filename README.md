
    Aplikacja pobiera, selekcjonuje i składuje  wybranedane o narzuconym profilu z witryn internetowych.
    Profil danych jest ustalony przez realizującego projekt. Profil danych powinien obejmować min. 4 grupy, np. adresy email, adresy korespondencyjne, schemat organizacyjny itp.
    Program wykorzystuje wielowątkowość/wieloprocesowość. Silnik należy zrealizować we własnym zakresie wykorzystując: multiprocessing i asyncio. Przetwarzanie ma być wieloprocesowe, najlepiej z możliwością skalowania na rdzenie procesora, dalej na komputery, dalej na klastry itp.
    Do parsowania kontentu należy użyć beautifulsoup.
    Dane mają być zapisywane w BD, np. MongoDB
    Program ma posiadać interfejs graficzny zrealizowany w Python (Flask lub Django) 
    Docelowo aplikacja ma być rozproszona na min 3 moduły: interfejs (1 lub więcej kontenerów), silnik (1 kontener), BD (1 kontener). Sposób ulokowania należy opracować we własnym zakresie i potrafić uzasadnić wybory.
    Oprogramowanie może być zrealizowane w grupie 1 lub 2 osobowej. 
    Projekt uznaje się za złożony, jeżeli w wyznaczonym terminie zostanie opublikowany szczegółowy raport z dowiązaniem do repozytorium kodu (github) oraz zostanie zademonstrowany prowadzącemu na ostatnich zajęciach laboratoryjnych.
