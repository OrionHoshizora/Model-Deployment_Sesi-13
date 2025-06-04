import requests

BASE_URL = "http://localhost:8000"

def test_prediction():
    test_cases = [
        {
            "name": "Adult Male Abalone",
            "data": {
                "sex": "M",
                "length": 0.595,
                "diameter": 0.475,
                "height": 0.15,
                "whole_weight": 0.9145,
                "shucked_weight": 0.3755,
                "viscera_weight": 0.2055,
                "shell_weight": 0.25
            }
        },
        {
            "name": "Adult Female Abalone",
            "data": {
                "sex": "F",
                "length": 0.530,
                "diameter": 0.420,
                "height": 0.135,
                "whole_weight": 0.677,
                "shucked_weight": 0.256,
                "viscera_weight": 0.142,
                "shell_weight": 0.210
            }
        },
        {
            "name": "Infant Abalone",
            "data": {
                "sex": "I",
                "length": 0.200,
                "diameter": 0.150,
                "height": 0.030,
                "whole_weight": 0.055,
                "shucked_weight": 0.020,
                "viscera_weight": 0.010,
                "shell_weight": 0.015
            }
        }
    ]
    
    print("🔮 Testing Abalone Age Prediction API\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print("-" * 50)
        
        try:
            response = requests.post(f"{BASE_URL}/predict", json=test_case['data'])
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Status: SUCCESS")
                print(f"📊 Input Data:")
                for key, value in test_case['data'].items():
                    print(f"   {key}: {value}")
                print(f"🎯 Prediction Results:")
                print(f"   Predicted Rings: {result['predicted_rings']}")
                print(f"   Predicted Age: {result['predicted_age']} years")
            else:
                print(f"❌ Status: FAILED ({response.status_code})")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Status: ERROR")
            print(f"   Exception: {e}")
        
        print("\n")

if __name__ == "__main__":
    try:
        test_prediction()
        print("🎉 Testing completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API!")
        print("💡 Make sure the server is running:")
        print("   cd abalone-backend")
        print("   uvicorn app:app --reload")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
