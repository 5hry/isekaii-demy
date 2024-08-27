from django import template
from courses.models import Lesson 
from django.db.models import Sum
from cart.models import Cart
register = template.Library()


@register.filter(name='subtract_one')
def subtract_one(value):
    return value - 1

@register.filter(name='get_raters')
def raters(value):
    return value*7//3 +5


@register.filter(name='minutes')
def total_minutes(course):
    lessons = Lesson.objects.filter(course_id = course.slug)
    # print(course)
    
    total = lessons.aggregate(total =Sum('duration'))['total']
    if total is not None:
        hours = int(total // 60)
        minutes =int( total % 60)
        return {"hours": hours, "minutes": minutes}
    else:
        # Trả về giá trị mặc định hoặc xử lý tùy ý khi total là None
        return {"hours": 0, "minutes": 0}
    # return 1

@register.filter(name='is_enrolled')
def is_enrolled(course, user):
    return course.enrolls.filter(user=user).exists()


@register.filter(name='is_in_wishlist')
def is_in_wishlist(course, user):
    return course.wishlist.filter(user=user).exists()

@register.filter(name='is_in_cart')
def is_in_cart(request,course):
    cart = Cart(request)
    return cart.has_course(course)