import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

# Load dataset (update with actual filename)
df = pd.read_csv('Energy_Consumption_Dataset.csv',
                 parse_dates=['Datetime'],
                 index_col='Datetime',
                dayfirst=True)

# Resample to hourly frequency (though it may already be hourly)
df_resampled = df.resample('h').mean()

# Fill missing values using forward fill
df_resampled = df_resampled.ffill ()

df_resampled = df_resampled.copy()

# Extract hour and day of the week for AI feature engineering
df_resampled['hour'] = df_resampled.index.hour
df_resampled['day_of_week'] = df_resampled.index.dayofweek  # Monday=0, Sunday=6

# Prepare features and target variable
X = df_resampled[['hour', 'day_of_week']]
y = df_resampled['AEP_MW']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train MLP Regressor model
mlp = MLPRegressor(hidden_layer_sizes=(50, 50), activation='relu', solver='adam', max_iter=500, random_state=42)
mlp.fit(X_train_scaled, y_train)

# Make predictions
y_pred = mlp.predict(X_test_scaled)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)

print(f'Mean Absolute Error: {mae}')

joblib.dump(mlp, 'energy_forecast_model.pkl')