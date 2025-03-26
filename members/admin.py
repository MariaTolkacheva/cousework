from django.contrib import admin
from .models import Question, Answer, Quiz, UserScore, TextAnswer

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quiz)
admin.site.register(UserScore)
admin.site.register(TextAnswer)