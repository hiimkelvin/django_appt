# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users, Appt
import datetime

def index(request):
    return render(request, 'Appt/index.html')

def register(request):
	context = {
		'name': request.POST['name'],
        'email': request.POST['email'],
		'pass': request.POST['password'],
		'c_pass': request.POST['confirm_pw'],
        'dob': request.POST['dob'],
	}
	reg_results = Users.objects.reg(context)
	if reg_results['new'] != None:

		request.session['users_id'] = reg_results['new'].id
		request.session['users_name'] = reg_results['new'].n_ame
		return redirect('/appointments')
	else:
		for error_str in reg_results['error_list']:
			messages.add_message(request, messages.ERROR, error_str)
		return redirect('/')

def login(request):
    context = {
        'email': request.POST['email'],
        'pass': request.POST['password'],
    }
    results = Users.objects.log(context)
    if results['list_errors'] != None:
        for error in results['list_errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['users_id'] = results['logged_user'].id
        request.session['users_name'] = results['logged_user'].n_ame
        return redirect('/appointments')

def logout(request):
    request.session.clear()
    return redirect('/')

def appointments(request):
    if 'users_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/')
    current_user = request.session['users_id']
    context ={
        'appts': Appt.objects.filter(user_id=current_user).order_by('time'),
    }
    return render(request, 'Appt/appt.html', context)

def add_task(request):
    if 'users_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/')

    context = {
        'users_id': request.session['users_id'],
        'date': request.POST['date'],
        'time': request.POST['time'],
        'task': request.POST['task'],
    }
    results = Appt.objects.add_task(context)
    if results['appt_errors'] != None:
        for error in results['appt_errors']:
            messages.add_message(request, messages.ERROR, error)
            return redirect('/appointments')
    else:
        return redirect('/appointments')

def delete(request, id):
    context = {
        "user": request.session['users_id'],
        "task_id": id
    }
    results = Appt.objects.delete(context)
    return redirect('/appointments')

def update_appt(request, id):
    task = Appt.objects.filter(id=id)
    context = {
        'curr_task': task,
    }
    return render(request, 'Appt/update_app.html', context)

def edit(request, id):
    context = {
        "user": request.session['users_id'],
        "task_id": id
    }
    results = Appt.objects.update(context)
    return redirect('/appointments')
