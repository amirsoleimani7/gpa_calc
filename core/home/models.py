from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    name = models.CharField(max_length=255)
    grade = models.CharField(max_length=2 , choices=[('S','S') ,('A','A') ,('B','B') , ('C','C') , ('D','D') ,('D','D')])
    credits = models.PositiveIntegerField()

    def __str__(self): # for the django admin page
        return f"{self.name} - grade : {self.grade} , credits : {self.credits}"



