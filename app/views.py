from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .facerec.click_photos import click
from .facerec.identify import identify2
from .models import Patient
from .forms import PatientForm
from .facerec.train_model import trainer
import cv2
import datetime

def index(request):
    return render(request, 'app/index.html')


def add_photos(request):
	pt_list = Patient.objects.all()
	return render(request, 'app/add_photos.html', {'pt_list': pt_list})


def click_photos(request, pt_id):
	cam = cv2.VideoCapture(0)
	pt = get_object_or_404(Patient, id=pt_id)
	click(pt.name, pt.id, cam)
	return HttpResponseRedirect(reverse('add_photos'))

def identify(request):
	
	identify2()
	return HttpResponseRedirect(reverse('index'))

def train(request):
	trainer()
	return HttpResponseRedirect(reverse('index'))


def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            pt = form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = PatientForm()
    return render(request, 'app/add_patient.html', {'form': form})
