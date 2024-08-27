from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('users/', include([
        path('my-courses/enrolled_courses', views.EnrolledCoursesListView.as_view(), name='enrolled-courses'),
        path('my-courses/wishlist', views.WishlistCoursesListView.as_view(), name='wishlist-courses'),
        path('my-courses/<slug:slug>/view', views.StartLessonView.as_view(), name='course-lessons'),
        path('my-courses/<slug:slug>/lessons/<int:id>', views.LessonView.as_view(), name='course-lessons-single'),
        path('profile', views.ProfileUpdateView.as_view(), name='my-profile'),
        path('password', views.ProfileUpdateView.as_view(), name='change_pass'),
        path('change_password/', views.change_password_view, name='change_password'),
        # path('save_note/', views.save_note, name='save_note'),
        # path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    ])),
]
