from django.shortcuts import render, redirect, get_object_or_404
from course.models import Course
from .models import Review
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.contrib.auth import get_user_model


def course_reviews(request, course_id):
    course = Course.objects.get(id=course_id)
    reviews = Review.objects.filter(course=course)
    course.num_reviews = len(reviews)
    course.avg_rating = sum([review.rating for review in reviews]) / course.num_reviews if course.num_reviews > 0 else 0
    users = get_user_model().objects.all()
    instructors = [user for user in users if course in user.courses.all() and user.user_type == 'I']
    instructor = instructors[0] if len(instructors) > 0 else None
    return render(request, 'feedback/reviews.html', {'course': course, 'reviews': reviews, 'instructor': instructor})


@login_required
def add_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    users = get_user_model().objects.all()
    instructors = [user for user in users if course in user.courses.all() and user.user_type == 'I']
    instructor = instructors[0] if len(instructors) > 0 else None
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        user = get_user_model().objects.get(id=request.user.id)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = user
            review.rating = 5 - review.rating + 1
            review.save()
            return redirect('feedback:review', course_id=course.id)
        else:
            return render(request, 'feedback/add_review.html', {'course': course, 'form': form, 'instructor': instructor})
    else:
        form = ReviewForm()

    return render(request, 'feedback/add_review.html', {'course': course, 'form': form, 'instructor': instructor})
