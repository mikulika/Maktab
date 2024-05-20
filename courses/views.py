from django.urls import reverse
import secrets
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,DetailView,View
from courses.models import Lendet,Lesson,Klasa
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import KlasaForm, LendetForm, LessonForm
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Klasa.objects.all()
        context['category'] = category
        return context


def CourseListView(request, category):
    courses = Lendet.objects.filter(klasa=category)
    context = {
        'courses':courses,
        'kategori':category
    }
    return render(request, 'courses/course_list.html', context)


class CourseDetailView(DetailView):
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'
    model = Lendet

class LessonDetailView(View,LoginRequiredMixin):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Lendet, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        context = {'lesson': lesson}
        return render(request, "courses/lesson_detail.html", context)


@login_required
def SearchView(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        results = Lesson.objects.filter(title__contains=search)
        context = {
            'results':results
        }
        return render(request, 'courses/search_result.html', context)

@login_required
def create_class(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'Your account does not have access to this url, only teacher accounts!')
        return redirect('courses:home')
    if request.method == 'POST':
        form = KlasaForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your class was created.')
            return redirect(reverse('users:index'))
    else:
        form = KlasaForm()
    context = {
        'form':form
    }
    return render(request, 'courses/create_class.html', context)


@login_required
def create_subject(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'Your account does not have access to this url, only teacher accounts!')
        return redirect('courses:home')
    if request.method == 'POST':
        form = LendetForm(request.POST)
        if form.is_valid():
            form.save()
            klasa = form.cleaned_data['klasa']
            slug = klasa.id
            messages.success(request, f'Your thread has been created.')
            return redirect('/courses/' + str(slug))
    else:
        form = LendetForm(initial={'creator':request.user.id, 'slug':secrets.token_hex(nbytes=16)})
    context = {
        'form':form
    }
    return render(request, 'courses/create_subject.html', context)


@login_required
def create_lesson(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'Your account does not have access to this url, only teacher accounts!')
        return redirect('courses:home')
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            subject = form.cleaned_data['subject']
            slug = subject.slug
            messages.success(request, f'Your lesson has been created.')
            return redirect('/courses/' + str(slug) )
    else:
        form = LessonForm(initial={'slug':secrets.token_hex(nbytes=16)})
    context = {
        'form':form
    }
    return render(request, 'courses/create_lesson.html', context)

def view_404(request, exception):
    return render(request, '404.html')

def view_403(request, exception):
    return render(request, '403.html')

def view_500(request):
    return render(request, '500.html')
