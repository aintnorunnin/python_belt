# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from ..login.models import User

# Create your views here.

#Render home page
def index(request):
    try:
        request.session['user_id']
    except:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    all_users = User.objects.exclude(name=user.name)
    friends = user.friends.all()
    count = user.friends.all().count()
    non_friends = []

    for person in all_users:
        if person not in friends:
            non_friends.append(person)

    context = {
        'user': user,
        'friends':friends ,
        'count': count,
        'non_friends': non_friends,
    }

    return render (request, 'friends/index.html', context)


def add_friend(request, friend_id):
    try:
        request.session['user_id']
    except:
        return redirect('/')

#Create and add new friend to 'friends'
    friend = User.objects.get(id=friend_id)
    user = User.objects.get(id=request.session['user_id'])
    user.friends.add(friend)
    return redirect('/friends')

def remove_friend(request, friend_id):
    try:
        request.session['user_id']
    except:
        return redirect('/')

#remove friend from 'friends'
    friend = User.objects.get(id=friend_id)
    user = User.objects.get(id=request.session['user_id'])
    user.friends.remove(friend)
    return redirect('/friends')
