from django.contrib import admin
from .models import CustomUser, Subject, Quiz, Question, Option, QuizAttempt, StudentAnswer, ContactQuery

admin.site.register(CustomUser)
admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuizAttempt)
admin.site.register(StudentAnswer)
admin.site.register(ContactQuery)