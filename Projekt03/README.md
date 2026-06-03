# Klasyfikacja Rezerwacji Hotelowych i Predykcja Anulowań

## Opis Projektu
Niniejszy projekt realizuje zadanie klasyfikacji binarnej na zbiorze danych `hotel_bookings.csv`. Celem jest przewidzenie, czy dana rezerwacja zostanie anulowana przez gościa (`is_canceled`), na podstawie cech takich jak czas wyprzedzenia rezerwacji (lead time), struktura gości, wybrany typ posiłku czy segment rynku.

## Struktura Projektu
Projekt został podzielony na moduły zgodnie z zasadami czystego kodu:
* `data_preprocessing.py`: czyszczenie danych, usuwanie anomalii oraz logarytmizacja zmiennych skośnych.
* `models.py`: Implementacja i parametryzacja 5 zróżnicowanych modeli klasyfikacji.
* `visualization.py`: prezentacje graficzne wykorzystujące interaktywne wykresy Plotly.
* `main.py`: main.

## Wybór Najlepszego Modelu i Uzasadnienie (CatBoost)
W przeprowadzonych eksperymentach najwyższą celnością (**Test Accuracy**) oraz najniższą wartością funkcji straty charakteryzował się model **CatBoost Classifier**. Poniżej przedstawiono matematyczno-algorytmiczne powody, dla których ten model okazał się bezkonkurencyjny w tym zadaniu:

1. **Natywna i Optymalna Obsługa Danych Kategorycznych:** Zbiór `hotel_bookings` w znacznej części opiera się na danych jakościowych (np. `deposit_type`, `market_segment`). CatBoost stosuje zaawansowany mechanizm statystyk celu uporządkowanego (*Ordered Target Statistics*), który zapobiega wyciekowi danych (target leakage) podczas kodowania zmiennych, co daje mu przewagę nad tradycyjnym, ręcznym mapowaniem etykiet.
2. **Odporność na Przeuczenie (Ordered Boosting):** Klasyczne implementacje algorytmów Gradient Boosting (np. domyślny XGBoost czy LightGBM) bywają podatne na przeuczenie przy specyficznych strukturach danych. CatBoost rozwiązuje ten problem za pomocą autorskiej techniki *Ordered Boosting*, opartej na losowych permutacjach zbioru treningowego, co minimalizuje błąd przesunięcia predykcji (*prediction shift*).
3. **Symetryczne Drzewa Decyzyjne (Oblivious Trees):** CatBoost konstruuje tzw. drzewa zapominalskie (symetryczne), gdzie na każdym poziomie drzewa wykorzystywany jest dokładnie ten sam warunek podziału. Taka struktura działa jak silny regulator, czyni model wysoce stabilnym matematycznie i drastycznie przyspiesza wnioskowanie na zbiorze testowym.
4. **Wysoka Skuteczność na Parametrach Domyślnych:** Algorytm został zaprojektowany tak, aby osiągać optymalne rezultaty bez konieczności czasochłonnego strojenia hiperparametrów za pomocą siatki (GridSearch), co potwierdziło jego przewagę nad algorytmami takimi jak K-Najbliżsi Sąsiedzi czy Drzewa Decyzyjne.



## Zakres korzystania z pomocy samouczków i AI:
- przykłady innych projektów: pomoc w preprocessingu danych
- AI: pomoc w wygenerowaniu wizualizacji(wykresów), pomoc w uzasadnieniu wyboru najlepszego modelu, częściowa pomoc w refaktoryzacji.

## Bibliografia:
- dane:
    - https://www.kaggle.com/datasets/mathsian/hotel-bookings
- samouczki
    - https://www.w3schools.com/python/python_ml_k-means.asp 02.06.2026
- AI:
    - Google Gemini 3.x 02.06.2026
- frameworki:
    - Flask 3.0.0
    - pandas (v2.x) - Manipulacja macierzami danych.
    - numpy (v1.x) - Operacje matematyczne i transformacje logarytmiczne.
    - scikit-learn (v1.x) - Podział zbioru, Logistic Regression, Decision Tree, Random Forest.
    - xgboost (v2.x) - Algorytm eXtreme Gradient Boosting.
    - catboost (v1.x) - Główny klasyfikator oparty o drzewa symetryczne.
    - plotl` (v5.x) - Renderowanie interaktywnych wykresów i macierzy błędów.