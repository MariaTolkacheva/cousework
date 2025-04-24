from django.contrib import admin

from members.models import Answer, Question, Quiz, TextAnswer, UserScore


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quiz)
admin.site.register(UserScore)
admin.site.register(TextAnswer)
