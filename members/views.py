import logging
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rag.query_data import compare_results
from .models import Quiz, Answer, UserScore
from .forms import QuizForm


def myfirst(request):
    return render(request, 'myfirst.html')


def testing(request):
    return render(request, 'testing.html', {'fruits': ['Apple', 'Banana', 'Cherry']})


@login_required
def quiz_view(request, quiz_id=None):
    if quiz_id:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()

        if request.method == 'POST':
            score = 0
            for question in questions:
                selected_answer_id = request.POST.get(f'question_{question.id}')
                if selected_answer_id:
                    selected_answer = Answer.objects.get(id=selected_answer_id)
                    logging.warning(
                        f'type(selected_answer) = {type(selected_answer)} {selected_answer.id}, {selected_answer}')
                    if selected_answer.is_correct:
                        score += 1

            UserScore.objects.create(user=request.user, quiz=quiz, score=score)
            return render(request, '../templates/result.html', {'score': score, 'total': questions.count()})

        return render(request, '../templates/quiz.html', {'quiz': quiz, 'questions': questions})
    else:
        quizzes = Quiz.objects.filter(is_bool=True)
        text_quizzes = Quiz.objects.filter(is_bool=False)
        return render(request, '../templates/all_quizes.html', {'quizzes': quizzes, 'text_quizzes': text_quizzes})


@login_required
def form_view(request, quiz_id=None):
    if quiz_id:
        total_score = 0
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        correct_answers = ''
        if request.method == 'POST':
            logging.warning('we are going on here 1')
            form = QuizForm(questions, request.POST)
            if form.is_valid():
                # Оцениваем каждый ответ
                for question in questions:
                    user_answer = form.cleaned_data[f'question_{question.id}']
                    correct_answers += compare_results(user_ans=user_answer,correct_ans=question.correct_answer)
                    correct_answers += question.correct_answer
                    if user_answer.lower() == question.correct_answer.lower():
                        total_score += 1  # Начисляем 1 балл за правильный ответ

                UserScore.objects.create(user=request.user, quiz=quiz, score=total_score)
                return render(request, '../templates/result.html',
                              {'answer': correct_answers, 'score': total_score, 'total': questions.count()})

        else:
            logging.warning(f'we are going on here {questions}')
            form = QuizForm(questions)
            logging.warning(form.fields)
            return render(request, 'form.html', {'quiz': quiz, 'form': form})
    else:
        quizzes = Quiz.objects.filter(is_bool=True)
        text_quizzes = Quiz.objects.filter(is_bool=False)
        return render(request, '../templates/all_quizes.html', {'quizzes': quizzes, 'text_quizzes': text_quizzes})


def survey(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'You need to be logged in to access this page.')
        return redirect('login')  # Redirect to home
    quizzes = Quiz.objects.filter(is_bool=True)
    text_quizzes = Quiz.objects.filter(is_bool=False)
    return render(request, 'all_quizes.html', {'quizzes': quizzes, 'text_quizzes': text_quizzes})


@login_required
def score_history(request):
    # Fetch the logged-in user's score history
    scores = UserScore.objects.filter(user=request.user).order_by('date_taken')

    # Prepare data for the chart
    labels = [score.date_taken.strftime('%Y-%m-%d %H:%M') for score in scores]  # Dates
    data = [score.score for score in scores]  # Scores

    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, '../templates/score_history.html', context)


@login_required
def score_history_by_id(request, quiz_id=None):
    # Fetch the logged-in user's score history
    scores = UserScore.objects.filter(user=request.user).filter(quiz_id=quiz_id).order_by('date_taken')

    # Prepare data for the chart
    labels = [score.date_taken.strftime('%Y-%m-%d %H:%M') for score in scores]  # Dates
    data = [score.score for score in scores]  # Scores

    quizzes = Quiz.objects.all()

    context = {
        'title': Quiz.objects.get(id=quiz_id).title,
        'labels': labels,
        'data': data,
        'quizzes': quizzes,
    }
    return render(request, '../templates/score_history.html', context)
