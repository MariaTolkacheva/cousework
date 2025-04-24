import logging
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from members.forms import AskLLMForm, QuizForm
from members.models import Answer, Quiz, UserScore
from members.tasks import askllm_task, long_task, process_compare_results


def render_quizes_by_type(request):
    quizzes = Quiz.objects.filter(is_bool=True)
    text_quizzes = Quiz.objects.filter(is_bool=False)
    return render(request, 'all_quizes.html', {
                  'quizzes': quizzes, 'text_quizzes': text_quizzes})


def myfirst(request):
    return render(request, 'myfirst.html')


@login_required
def start_quiz_processing(request, quiz_id):
    logging.info('Starting quiz processing for user=%d', request.user.id)
    user_id = request.user.id

    numb = long_task.delay(user_id=1, quiz_id=1)  # Отправка задачи в Celery
    logging.info('we have sent the task to celery %s', numb)
    return render(request, 'waiting_page.html', {'quiz_id': quiz_id})


def askllm_view(request):
    '''Ask LLM and get a view with an answer pretrained on provided resourses'''
    if request.method == 'POST':
        hash_token: str = uuid.uuid4().hex
        form = AskLLMForm(request.POST)
        if form.is_valid():
            user_question = form.cleaned_data["question"]
            logging.info(
                'Asking LLM for user=%d, with question: %s and hash=%s', request.user.id, user_question, hash_token)

            numb = askllm_task.delay(user_question, hash_token)
            logging.info('askllm_view sent the task to celery %s', numb)
            cache.set(f"task_status:{hash_token}", {
                      "status": "pending"}, timeout=3600)
            return render(request, 'askllm.html', {'hash_token': str(hash_token)})
        logging.critical('the form is invalid')
    else:
        logging.info('Generating AskLLMForm')
        form = AskLLMForm()
        return render(request, 'askllm_form.html', {'form': form})


@login_required
def quiz_view(request, quiz_id=None):
    if quiz_id:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()

        if request.method == 'POST':
            score = 0
            for question in questions:
                selected_answer_id = request.POST.get(
                    f'question_{question.id}')
                if selected_answer_id:
                    selected_answer = Answer.objects.get(id=selected_answer_id)
                    logging.warning(
                        f'type(selected_answer) = {type(selected_answer)} {selected_answer.id}, {selected_answer}')
                    if selected_answer.is_correct:
                        score += 1

            UserScore.objects.create(user=request.user, quiz=quiz, score=score)
            return render(request, '../templates/result.html',
                          {'score': score, 'total': questions.count()})

        return render(request, '../templates/quiz.html',
                      {'quiz': quiz, 'questions': questions})
    else:
        return render_quizes_by_type(request)


@login_required
def check_compare_results(request, quiz_id):
    """Проверяем, обработан ли `compare_results()`"""
    user_score = UserScore.objects.get(user=request.user, quiz_id=quiz_id)
    if user_score.compare_result:
        return JsonResponse(
            {"done": True, "compare_result": user_score.compare_result})
    return JsonResponse({"done": False})


@login_required
def form_view(request, quiz_id=None):
    if quiz_id:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        correct_answers = ''
        if request.method == 'POST':
            form = QuizForm(questions, request.POST)
            if form.is_valid():
                user_answers: {str} = {}
                correct_answers: {str} = {}

                for question in questions:
                    user_answer = form.cleaned_data[f"question_{question.id}"]
                    user_answers[f"question_{question.id}"] = user_answer
                #     correct_answers[f"question_{question.id}"] = question.correct_answer

                user_answer = form.cleaned_data[f"question_{question.id}"]
                correct_answer = question.correct_answer

                logging.warning(
                    'we got user_answers=%s with correct_answers=%s', user_answers, correct_answers)
                logging.info(
                    'Starting quiz processing for user=%d', request.user.id)
                user_id = request.user.id

                # Отправка задачи в Celery

                numb = long_task.delay(user_id=user_id, quiz_id=quiz_id,
                                       user_answer=user_answer, correct_answer=correct_answer)
                '''process_compare_results.delay(
                    request.user.id, quiz_id, user_answers, user_score.date_taken)'''
                logging.info('we have sent the task to celery %s', numb)
                return render(request, 'waiting_page.html', {'quiz_id': quiz_id})

            else:
                logging.critical('the form is invalid')
        else:
            logging.info(
                'we are generating form for quiz_id=%s with questions=%s', quiz_id, questions)
            form = QuizForm(questions)
            return render(request, 'form.html', {'quiz': quiz, 'form': form})
    else:
        return render_quizes_by_type(request)


def survey(request):
    if not request.user.is_authenticated:
        messages.warning(
            request,
            'You need to be logged in to access this page.')
        return redirect('login')  # Redirect to home
    return render_quizes_by_type(request)


@login_required
def score_history(request):
    '''Fetch the logged-in user's score history'''
    scores = UserScore.objects.filter(user=request.user).order_by('date_taken')

    # Prepare data for the chart
    labels = [score.date_taken.strftime(
        '%Y-%m-%d %H:%M') for score in scores]  # Dates
    data = [score.score for score in scores]  # Scores

    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, '../templates/score_history.html', context)


@login_required
def score_history_by_id(request, quiz_id=None):
    '''Fetch the logged-in user's score history by quiz id'''
    scores = UserScore.objects.filter(
        user=request.user).filter(
        quiz_id=quiz_id).order_by('date_taken')

    # Prepare data for the chart
    labels = [score.date_taken.strftime(
        '%Y-%m-%d %H:%M') for score in scores]  # Dates
    data = [score.score for score in scores]  # Scores

    quizzes = Quiz.objects.all()

    context = {
        'title': Quiz.objects.get(id=quiz_id).title,
        'labels': labels,
        'data': data,
        'quizzes': quizzes,
    }
    return render(request, '../templates/score_history.html', context)
