from django.shortcuts import render
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from courses.models import Course, Category
from django.shortcuts import get_object_or_404, redirect
from .models import Wishlist

from django.db.models import Q

def index(request):
    return render(request, 'index.html', {})


class HomeListView(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_courses'] = self.model.objects.all().order_by('-rating')[:10]
        
        context['range'] = range(1,6)
        return context


class SearchView(ListView):
    model = Course
    template_name = 'search.html'
    context_object_name = 'courses'
    # paginate_by = 10

    def get_queryset(self):
        # Lấy giá trị từ tham số 'q' và loại bỏ khoảng trắng
        query = self.request.GET.get('q', '').strip()

        # Kiểm tra nếu 'q' không rỗng
        if query:
            # Sử dụng Q objects để thực hiện truy vấn với điều kiện title__icontains
            return self.model.objects.filter(Q(title__icontains=query))
        else:
            # Nếu 'q' rỗng, trả về QuerySet trống
            return self.model.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['range'] = range(1,6)
        return context




