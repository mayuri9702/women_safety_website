from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=122,null=False)
    email=models.CharField(max_length=122,null=False)
    phone=models.CharField(max_length=12,null=False)
    desc=models.TextField()

    def __str__(self):
        return self.name
