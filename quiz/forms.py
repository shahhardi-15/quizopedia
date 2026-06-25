from django import forms
from .models import Quiz, Question, Option, Subject, CustomUser


class QuizForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
        required=False
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
        required=False
    )

    class Meta:
        model = Quiz
        fields = ['title', 'subject', 'description', 'time_limit_minutes', 'start_time', 'end_time', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Quiz Title'}),
            'subject': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Optional description...'}),
            'time_limit_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'question_text', 'question_type', 'difficulty', 'image', 'marks']
        widgets = {
            'quiz': forms.Select(attrs={'class': 'form-input'}),
            'question_text': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Type the question here...'}),
            'question_type': forms.Select(attrs={'class': 'form-input'}),
            'difficulty': forms.Select(attrs={'class': 'form-input'}),
            'marks': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option_text', 'is_correct']
        widgets = {
            'option_text': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter option text'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'branch', 'proctor', 'cgpa', 'attendance']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'branch': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Computer Science'}),
            'proctor': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Prof. Smith'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0', 'max': '10'}),
            'attendance': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'max': '100'}),
        }
