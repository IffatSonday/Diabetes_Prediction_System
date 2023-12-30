from django.shortcuts import render
import pandas as pd
from .models import DiabetesPrediction
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

def home(request):
    return render(request, 'home.html')

def predict(request):
    return render(request, 'predict.html')

def result(request):
    try:
        # Load the pre-trained model
        model = joblib.load('C:\\Users\\Effat\\Desktop\\SystemTronInternship\\Daibetic_Prediction_System\\Model\\log_reg_Model.pkl')

        # Get input values from the request
        Pregnancies = float(request.GET.get('Pregnancies', 0))
        Glucose = float(request.GET.get('Glucose', 0))
        SkinThickness = float(request.GET.get('SkinThickness', 0))
        Insulin = float(request.GET.get('Insulin', 0))
        BMI = float(request.GET.get('BMI', 0.0))
        DiabetesPedigreeFunction = float(request.GET.get('DiabetesPedigreeFunction', 0.0))
        Age = float(request.GET.get('Age', 0))

        # Reshape the input data
        input_data = np.array([Pregnancies, Glucose, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]).reshape(1, -1)

        # Make a prediction
        Outcome = model.predict(input_data)
        print(Outcome)
        
        # Map prediction to "Diabetic" or "Non-Diabetic"
        result_label = "Diabetic" if Outcome[0] == 1 else "Non-Diabetic"

        return render(request, 'predict.html', {'Outcome': result_label})

    except ValueError:
        return render(request, 'predict.html', {'error_message': 'Invalid input. Please enter numeric values.'})

    except Exception as e:
        # Handle errors, you might want to log the error for debugging
        print("Error:", str(e))
        return render(request, 'predict.html', {'error_message': 'Error occurred. Please try again.'})