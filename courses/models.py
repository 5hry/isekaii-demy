from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.db.models import Avg
from django.core.validators import MinValueValidator
from accounts.models import Account
from django.utils import timezone
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Course(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=200, unique=True, primary_key=True, auto_created=False)
    short_description = models.TextField(blank=False, max_length=100)
    description = models.TextField(blank=False)
    outcome = models.CharField(max_length=200)
    requirements = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    price = models.FloatField(validators=[MinValueValidator(9.99)])
    level = models.CharField(max_length=20)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video_url = models.CharField(max_length=100)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    rating = models.FloatField(default=5)
    

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)
    def calculate_average_rating(self):
        # Lấy tất cả các đánh giá liên kết với khóa ngoại là course
        ratings = Rating.objects.filter(course=self)
        
        # Tính trung bình các giá trị rating nếu có ít nhất một đánh giá
        average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        
        # Nếu không có đánh giá, mặc định là 5
        return average_rating if average_rating is not None else 5

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    duration = models.FloatField(validators=[MinValueValidator(0.30), MaxValueValidator(30.00)])
    video_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    @property
    def duration_as_integer(self):
        return int(self.duration)
    
    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course_slug = models.SlugField()
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.course_slug}'