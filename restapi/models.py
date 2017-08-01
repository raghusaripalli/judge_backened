from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

#
# class CustomUser(AbstractUser):
#     gender = models.CharField(max_length=10,null=True)
#     city = models.CharField(max_length=25,null=True)
#     userType = models.CharField(max_length=25,null=True) #Student,Professional,Admin
#     FavoriteLanguage = models.CharField(max_length=25,null=True)
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10,null=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    userType = models.CharField(max_length=25, null=True)   #student professional
    FavoriteLanguage = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.user.username

class Contest(models.Model):
    contest_code = models.CharField(max_length=30)
    name = models.CharField(max_length=128)
    Admin = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    starts = models.DateTimeField()
    ends = models.DateTimeField()

    def __str__(self):
        return self.contest_code


class Problem(models.Model):
    problem_code = models.CharField(max_length=30)
    problem_name = models.CharField(max_length=30)
    contest = models.ForeignKey(Contest,related_name='contest',on_delete=models.CASCADE)
    votes = models.IntegerField(blank=True,default=0)
    submissions = models.IntegerField(blank=True,default=0)
    max_score = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return self.problem_code

class Solutions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    url = models.CharField(max_length=256)
    status = models.IntegerField(blank=True,default=0)
    verdict = models.IntegerField(blank=True,default=0)
    score = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return self.user.username