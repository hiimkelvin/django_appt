# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re, datetime

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UsersManager(models.Manager):
    def reg(self, data):
    	errors = []

    	if len(data['name']) < 3:
    		errors.append("Name must be at least two characters long.")
		if data['email'] == '':
			errors.append("Email may not be blank")
		if not EMAIL_REGEX.match(data['email']):
			errors.append("Please enter a valid email address.")
		try:
			Users.objects.get(e_mail=data['email'])
			errors.append("Email is already registered")
		except:
			pass
		if data['dob'] == '':
			errors.append("Birthday is required.")
		elif datetime.datetime.strptime(data['dob'], '%Y-%m-%d') >= datetime.datetime.now():
			errors.append("Birthday may not be in the future!!")
    	if len(data['pass']) < 8:
    		errors.append("Password must be at least eight characters long.")
    	if data['pass'] != data['c_pass']:
    		errors.append("Password does not match Confirm Password.")

    	if len(errors) == 0:
    		data['pass'] = bcrypt.hashpw(data['pass'].encode('utf-8'), bcrypt.gensalt())
    		new_user = Users.objects.create(n_ame=data['name'], e_mail=data['email'], pass_word=data['pass'], birthday=data['dob'])
    		return {
    			'new': new_user,
    			'error_list': None
    		}
    	else:
    		return {
    			'new': None,
    			'error_list': errors
    		}

    def log(self, data):
        errors = []
        try:
        	user = Users.objects.get(e_mail=data['email'])
        	if bcrypt.hashpw(data['pass'].encode('utf-8'), user.pass_word.encode('utf-8')) != user.pass_word.encode('utf-8'):
        		errors.append("Incorrect password.")
        except:
        	errors.append("Email not registered.")
        if len(errors) == 0:
        	return {
        		'logged_user': user,
        		'list_errors': None
        	}
        else:
            return {
                'logged_user': None,
                'list_errors': errors
            }

class ApptManager(models.Manager):
    def add_task(self, data):
        errors = []

        if data['date'] == '':
            errors.append("Date is required.")
        if data['time'] == '':
            errors.append("Time is required.")
        if data['task'] == '':
            errors.append("Task is required.")
        elif datetime.datetime.strptime(data['date'], '%Y-%m-%d') <= datetime.datetime.now():
            errors.append("Cannot add task in the past!")

        if len(errors) == 0:
            users_id = data['users_id']
            current_user = Users.objects.get(id = users_id)
            Appt.objects.create(user_id=current_user, task=data['task'], status='Pending', time=data['time'], date=data['date'])
            return {
                'appt_errors': None
            }
        else:
            return {
                'appt_errors': errors
            }

    def delete(self, data):
        del_appt = Appt.objects.get(id=data['task_id']).delete()
        return {
            'd_appt': del_appt,
        }

    def update(self, data):

        upt_appt = Appt.objects.get(id=data['task_id']).save()



class Users(models.Model):
    n_ame = models.CharField(max_length=255)
    e_mail = models.CharField(max_length=255)
    pass_word = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Appt(models.Model):
    task = models.CharField(max_length=255)
    time = models.TimeField()
    date = models.DateField()
    status = models.CharField(max_length=255)
    user_id = models.ForeignKey(Users, related_name='user_id_appts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ApptManager()
