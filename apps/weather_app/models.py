from __future__ import unicode_literals
from django.db import models
import datetime, re, bcrypt
# Create your models here.

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        matchingEmail = User.objects.filter(email=postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if len(postData['fname']) == 0:
            errors['fname'] = "First name is required"

        if len(postData['lname']) == 0:
            errors['lname'] = "Last name is required"

        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email not in correct format"
        elif len(matchingEmail) > 0:
            errors['email'] = "Email already registered"

        if len(postData['pass']) == 0:
            errors['pass'] = "Password is required"
        elif len(postData['pass']) < 8:
            errors['pass'] = "Password must be at least 8 characters"
        elif postData['pass'] != postData['confirmPass']:
            errors['pass'] = "Passwords do not match"

        return errors

    def loginValidator(self, postData):
        matchingEmail = User.objects.filter(email=postData['email'])
        errors = {}

        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif len(matchingEmail) == 0:
            errors['email'] = "Email is not yet registered"

        if len(postData['pass']) == 0:
            errors['pass'] = "Password is required"
        elif not bcrypt.checkpw(postData['pass'].encode(), matchingEmail[0].password.encode()):
            errors['pass'] = "Password is incorrect"

        return errors

class Favorite(models.Model):
    city=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorites=models.ManyToManyField(Favorite, related_name="users")
    objects = UserManager()