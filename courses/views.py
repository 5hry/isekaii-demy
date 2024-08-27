from django.shortcuts import render


from django.http import Http404
from django.views.generic import DetailView, ListView
from django.db import models
from cart.models import Cart
from courses.models import Course, Category, Lesson
from account_courses.models import Enroll

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .form import RatingForm
from .models import Rating
from .models import Lesson
# Create your views here.
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/details.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object(self.get_queryset())
        ratings = Rating.objects.filter(course_slug=course.slug)
        context['ratings'] = ratings

        if self.request.user.is_authenticated:
            if Enroll.objects.filter(course=course, user_id=self.request.user.id).exists():
                context['is_enrolled'] = True
            else:
                cart = Cart(self.request)
                context['is_in_cart'] = cart.has_course(course)
        else:
            cart = Cart(self.request)
            context['is_in_cart'] = cart.has_course(course)
        context['range'] = range(1,6)

        return context



class CoursesByCategoryListView(ListView):
    model = Course
    template_name = 'courses/courses_by_category.html'
    context_object_name = 'courses'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(category_id=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        context['range'] = range(1,6)
        return context



@login_required(login_url='/login')
def submit_rating(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        # print(form.is_valid())
        if form.is_bound:
            # Lưu thông tin đánh giá vào cơ sở dữ liệu
            rating = Rating(
                user=request.user,
                course_slug=request.POST.get('slug', ''),
                rating=request.POST.get('rating'),
                comment=request.POST.get('review')
            )
            print(request.POST.get('slug', ''))
            rating.save()
            return redirect('courses:course-details', slug=request.POST.get('slug', ''))
    else:
        form = RatingForm()
    return render(request, 'index.html', {'form': form})