from django.db import models

# Create your models here.
from django.utils.timezone import now

from accounts.models import Account
from courses.models import Course
from django.conf import settings
from django.utils import timezone

class Enroll(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolls')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    
