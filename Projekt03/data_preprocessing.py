import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_and_clean_data(filepath='hotel_bookings.csv'):
    """Wczytuje zbiór danych i wykonuje wstępne czyszczenie braków."""
    df = pd.read_csv(filepath)
    
    # Zastąpienie wartości null zerami
    df.fillna(0, inplace=True)
    
    # Usunięcie wierszy, gdzie liczba dorosłych, dzieci i niemowląt wynosi 0 jednocześnie
    filter_zero_guests = (df.children == 0) & (df.adults == 0) & (df.babies == 0)
    df = df[~filter_zero_guests]
    
    return df

def preprocess_data(df):
    """Przetwarza cechy kategoryczne i numeryczne zgodnie z logiką projektu."""
    # Definicja kolumn nieprzydatnych do predykcji
    useless_col = ['days_in_waiting_list', 'arrival_date_year', 'assigned_room_type', 
                   'booking_changes', 'reservation_status', 'country']
    
    # Bezpieczne usunięcie kolumn (unikanie duplikatów z listy wyjściowej)
    cols_to_drop = [c for c in useless_col if c in df.columns]
    df_dropped = df.drop(cols_to_drop, axis=1)
    
    # Wyodrębnienie kolumn tekstowych
    cat_cols = [col for col in df_dropped.columns if df_dropped[col].dtype == 'O']
    cat_df = df_dropped[cat_cols].copy()
    
    # Przetwarzanie i ekstrakcja danych z daty rezerwacji
    if 'reservation_status_date' in cat_df.columns:
        cat_df['reservation_status_date'] = pd.to_datetime(cat_df['reservation_status_date'])
        cat_df['year'] = cat_df['reservation_status_date'].dt.year
        cat_df['month'] = cat_df['reservation_status_date'].dt.month
        cat_df['day'] = cat_df['reservation_status_date'].dt.day
        cat_df.drop(['reservation_status_date'], axis=1, inplace=True)
        
    if 'arrival_date_month' in cat_df.columns:
        cat_df.drop(['arrival_date_month'], axis=1, inplace=True)
        
    # Mapowanie zmiennych kategorycznych (oryginalne słowniki projektowe)
    cat_df['hotel'] = cat_df['hotel'].map({'Resort Hotel': 0, 'City Hotel': 1})
    cat_df['meal'] = cat_df['meal'].map({'BB': 0, 'FB': 1, 'HB': 2, 'SC': 3, 'Undefined': 4})
    cat_df['market_segment'] = cat_df['market_segment'].map({
        'Direct': 0, 'Corporate': 1, 'Online TA': 2, 'Offline TA/TO': 3,
        'Complementary': 4, 'Groups': 5, 'Undefined': 6, 'Aviation': 7
    })
    cat_df['distribution_channel'] = cat_df['distribution_channel'].map({
        'Direct': 0, 'Corporate': 1, 'TA/TO': 2, 'Undefined': 3, 'GDS': 4
    })
    cat_df['reserved_room_type'] = cat_df['reserved_room_type'].map({
        'C': 0, 'A': 1, 'D': 2, 'E': 3, 'G': 4, 'F': 5, 'H': 6, 'L': 7, 'B': 8
    })
    cat_df['deposit_type'] = cat_df['deposit_type'].map({'No Deposit': 0, 'Refundable': 1, 'Non Refund': 3})
    cat_df['customer_type'] = cat_df['customer_type'].map({
        'Transient': 0, 'Contract': 1, 'Transient-Party': 2, 'Group': 3
    })
    cat_df['year'] = cat_df['year'].map({2015: 0, 2014: 1, 2016: 2, 2017: 3})
    
    # Tworzenie zbioru numerycznego
    num_df = df_dropped.drop(columns=cat_cols, axis=1)
    if 'is_canceled' in num_df.columns:
        num_df.drop('is_canceled', axis=1, inplace=True)
        
    # Logarytmizacja cech w celu normalizacji rozkładów skośnych
    log_cols = ['lead_time', 'arrival_date_week_number', 'arrival_date_day_of_month', 'agent', 'company', 'adr']
    for col in log_cols:
        if col in num_df.columns:
            num_df[col] = np.log(num_df[col] + 1)
            
    if 'adr' in num_df.columns:
        num_df['adr'] = num_df['adr'].fillna(value=num_df['adr'].mean())
        
    # Połączenie przetworzonych ramek danych
    X = pd.concat([cat_df, num_df], axis=1)
    y = df_dropped['is_canceled']
    
    # Zabezpieczenie przed ewentualnymi brakami po mapowaniu nowych etykiet
    X.fillna(0, inplace=True)
    
    return X, y

def prepare_splits(X, y, test_size=0.30, random_state=42):
    """Dzieli zbiór danych na podzbiór treningowy i testowy."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)