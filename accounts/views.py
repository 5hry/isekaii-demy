from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, RedirectView, ListView, DetailView, UpdateView

from courses.models import Category, Lesson, Course
# from courses.form import NoteForm
from account_courses.models import Enroll, Wishlist
from .models import Account
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
# from co.models import Note
# from .forms import NoteForm
from django.views.decorators.csrf import csrf_exempt
class RegisterView(CreateView):
    model = Account
    form_class = UserRegistrationForm
    template_name = 'accounts/form.html'
    success_url = '/login'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):

        user_form = self.form_class(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/form.html', {'form': user_form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/form.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())

        return HttpResponseRedirect(self.get_success_url())
        # return super(Login, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


class EnrolledCoursesListView(ListView):
    model = Enroll
    template_name = 'courses/enrolled_courses.html'
    context_object_name = 'enrolls'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('course').filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class WishlistCoursesListView(ListView):
    model = Wishlist
    template_name = 'courses/wishlist_courses.html'
    context_object_name = 'wishlist'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('course').filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class StartLessonView(DetailView):
    model = Lesson
    template_name = 'lessons/lessons_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        queryset = queryset.filter(course=course)
        try:
            # Get the single item from the filtered queryset
            obj = queryset[:1].get()
            url = obj.video_url
            url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
            obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        lessons = self.model.objects.filter(course=course)
        # notes = Note.objects.filter(lesson__in=lessons)

        context["lessons"] = lessons
        context["course"] = course
        # context["notes"] = "123"
        return context
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        lessons = Lesson.objects.filter(course=course)
        # notes = Note.objects.filter(lesson__in=lessons)
        context = {'course': course, 'lessons': lessons}
        return render(request, self.template_name, context)

# @csrf_exempt
# def save_note(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             lesson_id = data['lesson_id']
#             content = data['content']

#             lesson = Lesson.objects.get(pk=lesson_id)
#             note, created = Note.objects.get_or_create(lesson=lesson)
#             note.content = content
#             note.save()

#             # Trả về response rỗng
#             return redirect(reverse_lazy("accounts:my-profile"))

#         except Exception as e:
#             return redirect(reverse_lazy("accounts:my-profile"))

#     return redirect(reverse_lazy("accounts:my-profile"))

class LessonView(DetailView):
    model = Lesson
    template_name = 'lessons/lessons_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        lesson_id = self.kwargs['id']
        queryset = queryset.filter(id=lesson_id)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
            url = obj.video_url
            url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
            obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["lessons"] = self.model.objects.filter(course=course)
        context["course"] = course
        return context


class ProfileUpdateView(UpdateView):
    model = Account
    template_name = "accounts/profile.html"
    context_object_name = "user"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("accounts:my-profile")

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_initial(self):
        return {"first_name": self.request.user.first_name, "last_name": self.request.user.last_name}

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@login_required
def change_password_view(request):
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')

        # Lấy ID của người dùng hiện tại
        user_id = request.user.id

        try:
            # Lấy người dùng từ cơ sở dữ liệu bằng ID
            user = Account.objects.get(id=user_id)

            # Đặt mật khẩu mới cho người dùng
            user.first_name = f_name
            user.last_name = l_name

            # Lưu lại thông tin người dùng
            user.save()
            
            messages.success(request, 'Password changed successfully.')
            context = {
                'messages': "hehehe",
            }
            return redirect(reverse_lazy("accounts:my-profile"),context)
        except Account.DoesNotExist:
            messages.error(request, 'User not found.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return redirect(reverse_lazy("accounts:my-profile"))

# from django.http import JsonResponse
# import stripe
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST

# stripe.api_key = 'your_stripe_secret_key'

# @csrf_exempt
# @require_POST
# def create_checkout_session(request):
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price': 'your_price_id',  # Thay đổi thành ID của giá cả bạn muốn sử dụng
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url='https://fb.com',  # Thay đổi thành URL thành công của bạn
#         cancel_url='https://fb.com',  # Thay đổi thành URL hủy bỏ của bạn
#     )

#     return JsonResponse({'id': session.id})