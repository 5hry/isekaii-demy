from django.shortcuts import render
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from courses.models import Course, Category
from django.shortcuts import get_object_or_404, redirect
from .models import Wishlist



def index(request):
    return render(request, 'index.html', {})


class HomeListView(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_courses'] = self.model.objects.all().order_by('-rating')
        
        context['range'] = range(1,6)
        return context


class SearchView(ListView):
    model = Course
    template_name = 'search.html'
    context_object_name = 'courses'
    # paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(title__contains=self.request.GET['q'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['range'] = range(1,6)
        return context




