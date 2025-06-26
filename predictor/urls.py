from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('predict/', views.predict_datapoint, name='predict'),
    path('live-predict/', views.live_prediction, name='live_prediction'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download_predictions_csv/', views.download_predictions_csv, name='download_predictions_csv'),
    path('feature_importance/', views.feature_importance, name='feature_importance'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('download_predictions_pdf/', views.download_predictions_pdf, name='download_predictions_pdf'),
] 