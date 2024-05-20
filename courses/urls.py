from django.urls import path
from django.contrib.auth.decorators import login_required

from courses.views import HomeView,CourseListView, CourseDetailView,LessonDetailView, SearchView, create_class, create_subject, create_lesson
from users.views import grades

app_name = 'courses'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('courses/<int:category>', CourseListView, name='course_list'),
    path('courses/<slug>/', login_required(CourseDetailView.as_view()), name='course_detail'),
    path('courses/<course_slug>/<lesson_slug>/', login_required(LessonDetailView.as_view()), name='lesson_detail'),
    path('search/', SearchView, name='search_course'),
    path('create/class/', create_class, name='create_class'),
    path('create/subject/', create_subject, name='create_subject'),
    path('create/lesson/', create_lesson, name='create_lesson'),
]
