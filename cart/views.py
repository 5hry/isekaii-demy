from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from courses.models import Course
from account_courses.models import Enroll, Wishlist
from .models import Cart


@require_POST
def cart_add(request, slug):
    cart = Cart(request)  # create a new cart object passing it the request object
    course = get_object_or_404(Course, slug=slug)
    cart.add(course=course, quantity=1, update_quantity=False)
    return redirect('cart:cart_detail')


def cart_remove(request, slug):
    cart = Cart(request)
    course = get_object_or_404(Course, slug=slug)
    cart.remove(course)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@login_required(login_url='/login')
def cart_checkout(request):
    carts = Cart(request)
    for cart in carts:
        course = cart['course']
        # course = get_object_or_404(Course, slug=course.slug)
        Enroll.objects.create(course=course, user_id=request.user.id)
        Wishlist.objects.filter(user_id=request.user.id, course=course).delete()
    messages.success(request, 'Successfully checked out!')
    carts.clear()
    return render(request, 'cart/checkout.html')


@login_required(login_url='/login')
def add_to_wishlist(request, slug):
    user = request.user
    course = get_object_or_404(Course, slug=slug)

    # # Kiểm tra xem đã tồn tại trong wishlist chưa
    if not Wishlist.objects.filter(user=user, course=course).exists():
        Wishlist.objects.create(user=user, course=course)
    # cart = Cart(request)  # create a new cart object passing it the request object
    # print(1)
    # course = get_object_or_404(Course, slug=slug)
    # cart.add(course=course, quantity=1, update_quantity=False)
    return redirect('accounts:wishlist-courses')