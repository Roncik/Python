import warnings
warnings.filterwarnings('ignore')

from data_preprocessing import load_and_clean_data, preprocess_data, prepare_splits
from models import get_models, train_and_evaluate
from visualization import plot_model_comparison, plot_confusion_matrix

def main():
    print("=== Krok 1: Ładowanie i wstępne czyszczenie zbioru danych ===")
    df = load_and_clean_data('hotel_bookings.csv')
    
    print("=== Krok 2: Pre-processing i kodowanie zmiennych ===")
    X, y = preprocess_data(df)
    print(f"Wymiary zbioru: Cechy {X.shape}, Cel {y.shape}")
    
    print("=== Krok 3: Podział na zbiór treningowy i testowy ===")
    X_train, X_test, y_train, y_test = prepare_splits(X, y, test_size=0.30, random_state=42)
    
    print("=== Krok 4: Uruchomienie i ewaluacja 5 modeli ML ===")
    models = get_models()
    results = train_and_evaluate(models, X_train, X_test, y_train, y_test)
    
    print("\n=== Krok 5: Zbiorcze podsumowanie wyników w konsoli ===")
    for name, metrics in results.items():
        print(f"\nModel: {name}")
        print(f" -> Test Accuracy: {metrics['accuracy']:.4f}")
        if metrics['test_loss'] is not None:
            print(f" -> Test Loss (LogLoss): {metrics['test_loss']:.4f}")
            
    print("\n=== Krok 6: Generowanie interaktywnych wizualizacji Plotly ===")
    #plot_model_comparison(results)
    
    # Wizualizacja macierzy błędów dla najlepszego modelu (CatBoost)
    if 'CatBoost' in results:
        plot_confusion_matrix(results['CatBoost']['confusion_matrix'], 'CatBoost')

if __name__ == '__main__':
    main()