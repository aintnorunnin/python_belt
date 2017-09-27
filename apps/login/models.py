# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def registration_validation(self,postData):
        results = {
            'state': True,
            'errors': []
        }

        if len(postData['name']) < 1:
            results['errors'].append('Name field required')
            results['state'] = False
        if len(postData['alias']) < 1:
            results['errors'].append('Alias field required')
            results['state'] = False
        if len(postData['email']) < 1:
            results['errors'].append('email field required')
            results['state'] = False
        if len(postData['name']) < 1:
            results['errors'].append('Name field required')
            results['state'] = False
        if postData['name'].isalpha() == False or postData['name'].isspace() == True:
            results['state'] = False
            results['errors'].append('Name must have characters')
        if postData['alias'].isalpha() == False or postData['alias'].isspace() == True:
            results['state'] = False
            results['errors'].append('Alias must have characters')
        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            results['state'] == False
            results['errors'].append("Email is not valid")
        if self.filter(email=postData['email']).exists():
            results['state'] == False
            results['errors'].append("Email is already in use")
        if postData['password'] != postData['confirm']:
            results['state'] == False
            results['errors'].append("Passwords do not match")
        if len(postData['password']) < 8 or len(postData['confirm']) < 8 :
            results['state'] == False
            results['errors'].append("Passwords must be 8 characters long")
        if not postData['birthday']:
            results['state'] = False
            results['errors'].append("Don't forget birthday")
        print postData['birthday']
        return results

    def login_valdiation(self,postData):
        results = {
            'state': True,
            'errors': [],
            'user': None,
        }
        list_of_users = self.filter(email=postData['email'])
        if len(list_of_users) < 1:
            results['state'] = False
            results['errors'].append('Email is not registered')
        else:
            user = list_of_users[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                results['user'] = user
            else:
                results['state'] = False
                results['errors'].append('Check email and paswword')
        return results

    def creator(self, postData):
        user = self.create(
            name= postData['name'],
            alias=postData['alias'],
            email =postData['email'],
            password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        )
        return user

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    friends = models.ManyToManyField("self")
    objects = UserManager()

# class Friend(models.Model):
#     users = models.ManyToManyField(User,related_name='friends')
