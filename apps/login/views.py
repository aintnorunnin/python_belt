# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from models import User



#Render Registration page
def index(request):
    return render(request,'login/index.html')

#Process registration form
def register(request):
    results = User.objects.registration_validation(request.POST)
    if results['state'] == False:
        for error in results['errors']:
            messages.error(request, error)
    else:
        user = User.objects.creator(request.POST)
        messages.success(request,"Success, user has been created")
    return redirect('/')


#Validate login form and log user in
def login(request):
    results = User.objects.login_valdiation(request.POST)
    if results['state'] == False:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = results['user'].id
        return redirect('friends:index')


#Display user information
def show(request,friend_id):
    try:
        request.session['user_id']
    except:
        return redirect('/')

    user = User.objects.get(id=friend_id)
    context = {
        'user': user
    }
    return render(request,'login/user.html', context)


#Log user out
def logout(request):
    try:
        request.session['user_id']
    except:
        return redirect('/')

    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

# def clear(request):
#     User.objects.all().delete()
#     return redirect('/')
