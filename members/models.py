from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    is_bool = models.BooleanField(default=True)
    description = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.title + ' - ' + \
            str(self.is_bool) + ' - ' + self.description


class Question(models.Model):
    text = models.TextField()
    correct_answer = models.TextField(default="")
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class TextAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField()
    comparison_feedback = models.TextField()
    score = models.IntegerField(default=0, verbose_name="Балл")

    def __str__(self):
        return f"{self.question.text}"


class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"
