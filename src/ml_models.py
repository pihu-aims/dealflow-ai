import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import streamlit as st
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class AcquisitionPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        self.is_trained = False
    
    def prepare_features(self, df):
        """Prepare features for ML model training."""
        # Select features for model
        feature_columns = [
            'revenue_multiple', 'growth_rate', 'profit_margin', 'market_share',
            'geography_overlap', 'technology_fit', 'cultural_fit', 
            'integration_complexity', 'deal_value', 'employee_count'
        ]
        
        # Handle categorical variables
        categorical_columns = ['industry']
        
        # Prepare feature matrix
        X = df[feature_columns].copy()
        
        # Log transform deal value and employee count
        X['deal_value'] = np.log1p(X['deal_value'])
        X['employee_count'] = np.log1p(X['employee_count'])
        
        # Encode categorical variables
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                X[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col])
            else:
                X[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        return X.values
    
    def train_model(self, dataset_path='data/ml_models/historical_ma_deals.csv'):
        """Train the acquisition success prediction model."""
        try:
            # Load dataset
            if isinstance(dataset_path, str):
                df = pd.read_csv(dataset_path)
            else:
                df = dataset_path
            
            logger.info(f"Training on {len(df)} historical deals")
            
            # Prepare features and target
            X = self.prepare_features(df)
            y = df['success'].values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Train multiple models and select best
            models = {
                'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
                'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
            }
            
            best_score = 0
            best_model = None
            
            for name, model in models.items():
                # Cross-validation
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
                mean_score = cv_scores.mean()
                
                logger.info(f"{name} - CV AUC: {mean_score:.3f} (+/- {cv_scores.std() * 2:.3f})")
                
                if mean_score > best_score:
                    best_score = mean_score
                    best_model = model
            
            # Train best model on full training set
            best_model.fit(X_train, y_train)
            self.model = best_model
            
            # Evaluate on test set
            y_pred = self.model.predict(X_test)
            y_pred_proba = self.model.predict_proba(X_test)[:, 1]
            
            test_auc = roc_auc_score(y_test, y_pred_proba)
            
            logger.info(f"✅ Model trained successfully!")
            logger.info(f"Test AUC: {test_auc:.3f}")
            logger.info(f"Test Accuracy: {(y_pred == y_test).mean():.3f}")
            
            self.is_trained = True
            
            # Save model
            self.save_model()
            
            return {
                'success': True,
                'test_auc': test_auc,
                'test_accuracy': (y_pred == y_test).mean(),
                'cv_score': best_score,
                'feature_importance': self.get_feature_importance()
            }
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def predict_acquisition_success(self, company_features):
        """Predict acquisition success probability for a company."""
        try:
            if not self.is_trained:
                self.load_model()
            
            if not self.is_trained:
                raise Exception("Model not trained. Please train the model first.")
            
            # Prepare features (same as training)
            features = np.array(company_features).reshape(1, -1)
            features_scaled = self.scaler.transform(features)
            
            # Get prediction probability
            success_probability = self.model.predict_proba(features_scaled)[0, 1]
            
            # Get feature importance for explanation
            feature_importance = self.get_feature_importance()
            
            return {
                'success_probability': success_probability,
                'recommendation': 'BUY' if success_probability > 0.7 else 'HOLD' if success_probability > 0.4 else 'PASS',
                'confidence': 'High' if abs(success_probability - 0.5) > 0.3 else 'Medium' if abs(success_probability - 0.5) > 0.15 else 'Low',
                'key_factors': feature_importance[:5]  # Top 5 factors
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return {'error': str(e)}
    
    def get_feature_importance(self):
        """Get feature importance from trained model."""
        if self.model is None or self.feature_names is None:
            return []
        
        importance_scores = self.model.feature_importances_
        feature_importance = [
            {'feature': name, 'importance': score}
            for name, score in zip(self.feature_names, importance_scores)
        ]
        
        return sorted(feature_importance, key=lambda x: x['importance'], reverse=True)
    
    def save_model(self):
        """Save trained model and preprocessors."""
        try:
            model_dir = Path('data/ml_models')
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # Save model and preprocessors
            joblib.dump(self.model, model_dir / 'acquisition_predictor.pkl')
            joblib.dump(self.scaler, model_dir / 'scaler.pkl')
            joblib.dump(self.label_encoders, model_dir / 'label_encoders.pkl')
            joblib.dump(self.feature_names, model_dir / 'feature_names.pkl')
            
            logger.info("✅ Model saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_model(self):
        """Load trained model and preprocessors."""
        try:
            model_dir = Path('data/ml_models')
            
            if not (model_dir / 'acquisition_predictor.pkl').exists():
                logger.warning("No trained model found")
                return False
            
            self.model = joblib.load(model_dir / 'acquisition_predictor.pkl')
            self.scaler = joblib.load(model_dir / 'scaler.pkl')
            self.label_encoders = joblib.load(model_dir / 'label_encoders.pkl')
            self.feature_names = joblib.load(model_dir / 'feature_names.pkl')
            
            self.is_trained = True
            logger.info("✅ Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False

@st.cache(allow_output_mutation=True)
def get_acquisition_predictor():
    """Get cached acquisition predictor instance."""
    return AcquisitionPredictor()