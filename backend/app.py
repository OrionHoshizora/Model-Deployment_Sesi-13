from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np

app = FastAPI(
    title="Abalone Age Prediction API",
    description="Simple API for predicting abalone age",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Global variables for model artifacts
model = None
scaler = None
label_encoder = None
feature_columns = None
model_metadata = None

def load_models():
    """Load model artifacts with detailed error handling"""
    global model, scaler, label_encoder, feature_columns, model_metadata
    
    try:
        print("🔄 Attempting to load model artifacts...")
        
        # Try loading each component individually
        model = joblib.load('./models/best_abalone_model.pkl')
        print("✅ Model loaded")
        
        scaler = joblib.load('./models/scaler.pkl')
        print("✅ Scaler loaded")
        
        label_encoder = joblib.load('./models/label_encoder.pkl')
        print("✅ Label encoder loaded")
        
        feature_columns = joblib.load('./models/feature_columns.pkl')
        print("✅ Feature columns loaded")
        
        model_metadata = joblib.load('./models/model_metadata.pkl')
        print("✅ Model metadata loaded")
        
        print("🎉 All model artifacts loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        print("⚠️  API will run in 'mock mode' - returning dummy predictions")
        
        # Set all to None to indicate model not loaded
        model = None
        scaler = None 
        label_encoder = None
        feature_columns = None
        model_metadata = None
        return False

# Try to load models at startup
model_loaded = load_models()

class AbaloneFeatures(BaseModel):
    sex: str = Field(..., description="Sex of abalone: M (Male), F (Female), I (Infant)")
    length: float = Field(..., ge=0, le=1, description="Longest shell measurement (normalized)")
    diameter: float = Field(..., ge=0, le=1, description="Perpendicular to length (normalized)")
    height: float = Field(..., ge=0, le=1, description="With meat in shell (normalized)")
    whole_weight: float = Field(..., ge=0, description="Whole abalone weight")
    shucked_weight: float = Field(..., ge=0, description="Weight of meat")
    viscera_weight: float = Field(..., ge=0, description="Gut weight after bleeding")
    shell_weight: float = Field(..., ge=0, description="Weight after being dried")
    
    class Config:
        # Fixed Pydantic V2 warning
        json_schema_extra = {
            "example": {
                "sex": "M",
                "length": 0.595,
                "diameter": 0.475,
                "height": 0.15,
                "whole_weight": 0.9145,
                "shucked_weight": 0.3755,
                "viscera_weight": 0.2055,
                "shell_weight": 0.25
            }
        }

class PredictionResponse(BaseModel):
    predicted_rings: float
    predicted_age: float
    model_status: str = "loaded"  # Add status indicator

def engineer_features(data: dict):
    """Create engineered features matching the training notebook exactly"""
    # Calculate volume using the same formula as training
    volume = (4/3) * np.pi * data['length'] * data['diameter'] * data['height']
    
    # Calculate all engineered features exactly as in training
    density = data['whole_weight'] / (volume + 1e-8)
    shell_ratio = data['shell_weight'] / (data['whole_weight'] + 1e-8)
    meat_ratio = data['shucked_weight'] / (data['whole_weight'] + 1e-8)
    bmi = data['whole_weight'] / (data['length']**2 + 1e-8)
    
    # Add the missing features from training
    surface_area = 2 * np.pi * ((data['length']*data['diameter'] + data['length']*data['height'] + data['diameter']*data['height'])/3)
    shucked_viscera_ratio = data['shucked_weight'] / (data['viscera_weight'] + 1e-8)
    
    return {
        'Volume': volume,
        'Density': density,
        'Shell_ratio': shell_ratio,
        'Meat_ratio': meat_ratio,
        'BMI': bmi,
        'Surface_area': surface_area,  # Missing feature 1
        'Shucked_Viscera_ratio': shucked_viscera_ratio  # Missing feature 2
    }

def mock_prediction(features_dict):
    """Generate mock prediction when model is not available"""
    # Simple heuristic based on size and weight
    size_factor = features_dict['length'] * features_dict['diameter'] * features_dict['height']
    weight_factor = features_dict['whole_weight']
    
    # Mock prediction logic
    base_rings = 8.0  # Average rings
    
    # Adjust based on size
    if size_factor > 0.05:
        base_rings += 3
    elif size_factor > 0.02:
        base_rings += 1
    
    # Adjust based on weight
    if weight_factor > 0.5:
        base_rings += 2
    elif weight_factor > 0.1:
        base_rings += 1
    
    # Add some variation based on sex
    if features_dict['sex'] == 'I':  # Infant
        base_rings = max(3, base_rings - 3)
    
    return base_rings

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "message": "API is running" + (" with model" if model else " in mock mode")
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_abalone_age(features: AbaloneFeatures):
    """Predict abalone age based on physical measurements"""
    
    try:
        input_data = features.dict()
        
        # Validate sex input
        if input_data['sex'] not in ['M', 'F', 'I']:
            raise HTTPException(status_code=400, detail="Sex must be 'M', 'F', or 'I'")
        
        # If model is loaded, use real prediction
        if model is not None:
            print("🤖 Using trained model for prediction")
            
            sex_encoded = label_encoder.transform([input_data['sex']])[0]
            engineered_features = engineer_features(input_data)
            
            # Create feature vector with ALL 15 features (matching training exactly)
            feature_vector = [
                sex_encoded,                                    # 1
                input_data['length'],                          # 2
                input_data['diameter'],                        # 3
                input_data['height'],                          # 4
                input_data['whole_weight'],                    # 5
                input_data['shucked_weight'],                  # 6
                input_data['viscera_weight'],                  # 7
                input_data['shell_weight'],                    # 8
                engineered_features['Volume'],                 # 9
                engineered_features['Density'],                # 10
                engineered_features['Shell_ratio'],            # 11
                engineered_features['Meat_ratio'],             # 12
                engineered_features['BMI'],                    # 13
                engineered_features['Surface_area'],           # 14 - was missing
                engineered_features['Shucked_Viscera_ratio']   # 15 - was missing
            ]
            
            print(f"Feature vector length: {len(feature_vector)}")  # Debug
            
            feature_vector_scaled = scaler.transform([feature_vector])
            predicted_rings = float(model.predict(feature_vector_scaled)[0])
            model_status = "loaded"
            
        else:
            print("🎭 Using mock prediction (model not loaded)")
            predicted_rings = mock_prediction(input_data)
            model_status = "mock"
        
        predicted_age = predicted_rings + 1.5
        
        return PredictionResponse(
            predicted_rings=round(predicted_rings, 2),
            predicted_age=round(predicted_age, 2),
            model_status=model_status
        )
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)