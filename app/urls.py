from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_photos/', views.add_photos, name='add_photos'),
    path('add_photos/<slug:pt_id>/', views.click_photos, name='click_photos'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('identify/', views.identify, name='identify'),
    path('train/', views.train, name='train'),

]
