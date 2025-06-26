import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'DimondPricePrediction', 'source'))
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from DimondPricePrediction.pipelines.prediction_pipeline import CustomData, PredictPipeline
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Prediction
import csv
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from DimondPricePrediction.utils.utils import load_object
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO

# Home page
def home_page(request):
    return render(request, "index.html")

# Prediction form and result
@csrf_exempt
@login_required
def predict_datapoint(request):
    if request.method == "GET":
        return render(request, "form.html")
    if request.method == "POST":
        data = CustomData(
            carat=float(request.POST.get('carat')),
            depth=float(request.POST.get('depth')),
            table=float(request.POST.get('table')),
            x=float(request.POST.get('x')),
            y=float(request.POST.get('y')),
            z=float(request.POST.get('z')),
            cut=request.POST.get('cut'),
            color=request.POST.get('color'),
            clarity=request.POST.get('clarity')
        )
        final_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_data)
        result = round(pred[0], 2)
        # Save prediction to DB
        Prediction.objects.create(
            user=request.user,
            carat=data.carat,
            depth=data.depth,
            table=data.table,
            x=data.x,
            y=data.y,
            z=data.z,
            cut=data.cut,
            color=data.color,
            clarity=data.clarity,
            predicted_price=result
        )
        return render(request, "result.html", {"final_result": result})

@csrf_exempt
def live_prediction(request):
    if request.method == "POST":
        try:
            data = CustomData(
                carat=float(request.POST.get('carat', 0) or 0),
                depth=float(request.POST.get('depth', 0) or 0),
                table=float(request.POST.get('table', 0) or 0),
                x=float(request.POST.get('x', 0) or 0),
                y=float(request.POST.get('y', 0) or 0),
                z=float(request.POST.get('z', 0) or 0),
                cut=request.POST.get('cut', ''),
                color=request.POST.get('color', ''),
                clarity=request.POST.get('clarity', '')
            )
            final_data = data.get_data_as_dataframe()
            predict_pipeline = PredictPipeline()
            pred = predict_pipeline.predict(final_data)
            result = round(pred[0], 2)
            # Save prediction to DB
            Prediction.objects.create(
                user=request.user,
                carat=data.carat,
                depth=data.depth,
                table=data.table,
                x=data.x,
                y=data.y,
                z=data.z,
                cut=data.cut,
                color=data.color,
                clarity=data.clarity,
                predicted_price=result
            )
            return JsonResponse({'success': True, 'prediction': result})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    # Prepare data for Chart.js
    chart_data = [
        {
            'created_at': p.created_at.strftime('%Y-%m-%d %H:%M'),
            'carat': p.carat,
            'predicted_price': p.predicted_price
        } for p in predictions
    ]
    return render(request, 'dashboard.html', {
        'predictions': predictions,
        'chart_data_json': json.dumps(chart_data, cls=DjangoJSONEncoder)
    })

@login_required
def download_predictions_csv(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=prediction_history.csv'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Carat', 'Depth', 'Table', 'X', 'Y', 'Z', 'Cut', 'Color', 'Clarity', 'Predicted Price'])
    for p in predictions:
        writer.writerow([
            p.created_at.strftime('%Y-%m-%d %H:%M'),
            p.carat, p.depth, p.table, p.x, p.y, p.z,
            p.cut, p.color, p.clarity, p.predicted_price
        ])
    return response

@login_required
def download_predictions_pdf(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.setFont('Helvetica-Bold', 16)
    p.drawString(40, height - 40, f"Prediction History for {request.user.username}")
    data = [["Date", "Carat", "Depth", "Table", "X", "Y", "Z", "Cut", "Color", "Clarity", "Predicted Price ($)"]]
    for pred in predictions:
        data.append([
            pred.created_at.strftime('%Y-%m-%d %H:%M'),
            pred.carat, pred.depth, pred.table, pred.x, pred.y, pred.z,
            pred.cut, pred.color, pred.clarity, pred.predicted_price
        ])
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#375a7f')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    table.wrapOn(p, width, height)
    table_height = 30 + 18 * len(data)
    table.drawOn(p, 30, height - 70 - table_height)
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=prediction_history.pdf'
    return response

@login_required
def feature_importance(request):
    model_path = os.path.join('artifacts', 'model.pkl')
    preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
    try:
        model = load_object(model_path)
        preprocessor = load_object(preprocessor_path)
        # Get feature names after preprocessing
        num_features = preprocessor.transformers_[0][2]
        cat_features = preprocessor.transformers_[1][2]
        cat_feature_names = preprocessor.transformers_[1][1]['encoder'].get_feature_names_out(cat_features)
        feature_names = list(num_features) + list(cat_feature_names)
        # Get importances
        if hasattr(model, 'coef_'):
            importances = model.coef_.flatten().tolist()
        elif hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_.tolist()
        else:
            importances = [0] * len(feature_names)
        # Pair and sort
        feat_imp = sorted(zip(feature_names, importances), key=lambda x: abs(x[1]), reverse=True)
        labels = [f[0] for f in feat_imp]
        values = [f[1] for f in feat_imp]
        return JsonResponse({'labels': labels, 'values': values})
    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
def profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            messages.success(request, 'Email updated successfully!')
    return render(request, 'profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})
