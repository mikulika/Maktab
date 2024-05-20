from django import forms
from django.contrib.auth.models import User
from .models import Klasa, Lendet, Lesson

class KlasaForm(forms.ModelForm):
    class Meta:
        model = Klasa
        fields = '__all__'
        help_texts = {
            'title': 'For example Class 11 or Computer Class',
            'description':'Enter a short description of the class',
            'image':'You can put a picture of the class or you can leave it blank'
        }

class LendetForm(forms.ModelForm):
    class Meta:
        model = Lendet
        fields = ['creator','slug', 'title', 'klasa', 'description', 'image_subject']
        help_texts = {
            'title': 'For example Mathematics, Geography, etc',
            'description':'Enter a short description of the subject',
            'classroom':'Select the classroom for which you will create the topic',
            'image_subject':'You can put a picture of the item or you can leave it blank'
        }
        labels = {
            'title':'Subject title'
        }
        widgets = {'creator': forms.HiddenInput(), 'slug': forms.HiddenInput()}


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson 
        fields = ['slug','title', 'subject', 'video_id', 'position', ]
        help_texts = {
            'title':'Enter the title of the lesson',
            'subject':'Choose the subject to which this lesson belongs',
            'video_id':'Enter the ID of the video from YouTube that you will upload (<a href="/media/youtube_help.png">where can i find the id</a>)',
            'position':'Enter the position number or teaching sequence '
        }
        widgets = {
            'slug': forms.HiddenInput()
        }