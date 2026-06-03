from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, log_loss

def get_models():
    #5 różnorodnych modeli uczenia maszynowego
    return {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(max_depth=10, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'XGBoost': XGBClassifier(learning_rate=0.1, max_depth=5, n_estimators=100, eval_metric='logloss', random_state=42),
        'CatBoost': CatBoostClassifier(iterations=100, depth=6, learning_rate=0.1, verbose=0, random_state=42)
    }

def train_and_evaluate(models, X_train, X_test, y_train, y_test):
    #Trenowanie i zbieranie metryk skuteczności
    results = {}
    for name, model in models.items():
        print(f"Trenowanie modelu: {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Obliczenie test loss za pomocą prawdopodobieństw klasowych
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)
            test_loss = log_loss(y_test, y_prob)
        else:
            test_loss = None
            
        acc = accuracy_score(y_test, y_pred)
        conf = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        results[name] = {
            'accuracy': acc,
            'test_loss': test_loss,
            'confusion_matrix': conf,
            'classification_report': report,
            'predictions': y_pred
        }
    return results