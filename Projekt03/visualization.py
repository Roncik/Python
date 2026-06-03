import plotly.express as px
import pandas as pd

def plot_model_comparison(results):
    """Tworzy interaktywny wykres słupkowy porównujący celność wszystkich modeli."""
    models_summary = pd.DataFrame({
        'Model': list(results.keys()),
        'Accuracy': [res['accuracy'] for res in results.values()],
        'Test Loss': [res['test_loss'] if res['test_loss'] is not None else 0 for res in results.values()]
    })
    
    fig_acc = px.bar(
        models_summary, 
        x='Accuracy', 
        y='Model', 
        color='Accuracy',
        orientation='h',
        title='Porównanie Celności Modeli Uczenia Maszynowego (Test Accuracy)',
        template='plotly_dark',
        color_continuous_scale='Viridis'
    )
    fig_acc.update_layout(xaxis=dict(range=[0, 1]))
    fig_acc.show()
    return fig_acc

def plot_confusion_matrix(matrix, model_name):
    """Wizualizuje macierz błędów (Confusion Matrix) dla wskazanego modelu."""
    fig_cm = px.imshow(
        matrix,
        text_auto=True,
        labels=dict(x="Przewidywana Etykieta", y="Rzeczywista Etykieta", color="Liczba"),
        x=['Zrealizowana (0)', 'Anulowana (1)'],
        y=['Zrealizowana (0)', 'Anulowana (1)'],
        title=f'Macierz Błędów (Confusion Matrix) - {model_name}',
        template='plotly_dark',
        color_continuous_scale='Blues'
    )
    fig_cm.show()
    return fig_cm