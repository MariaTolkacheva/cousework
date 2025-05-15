import logging

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from members.models import Quiz, UserScore
from rag.query_data import compare_results, query_rag
from rag.translate import Mode, translate


@shared_task
def process_compare_results(user_id, quiz_id, user_answers, date_taken):
    """Фоновая обработка ответов"""

    quiz = Quiz.objects.get(id=quiz_id)
    correct_answers = ""

    for question in quiz.questions.all():
        user_answer = user_answers.get(f"question_{question.id}", "")
        # correct_answers += compare_results(user_ans=user_answer,
        #                                   correct_ans=question.correct_answer)

    # Обновляем оценку в БД
    user_score = UserScore.objects.get(
        user_id=user_id, quiz=quiz, date_taken=date_taken)
    user_score.compare_result = correct_answers
    user_score.save()

    return correct_answers


@shared_task()
def long_task(user_id: int, quiz_id: int, user_answer: str, correct_answer: str):
    logging.info('we are inside long_running_api_task')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = get_object_or_404(User, id=user_id)

    feed_back = compare_results(user_ans=user_answer,
                                correct_ans=correct_answer)

    # Обновляем оценку в БД
    '''user_score = UserScore.objects.get(
        user_id=user_id, quiz=quiz, date_taken=date_taken)
    user_score.compare_result = correct_answers
    user_score.save()

    UserScore.objects.create(
        user=user, quiz=quiz, score=75
    )'''
    result = f"Результат для викторины {quiz} готов = {feed_back}"
    # 2. Отправка результата через WebSocket (Channels)
    channel_layer = get_channel_layer()
    # group_name = f"quiz_result_{user_id}_{quiz_id}"
    group_name = "quiz_result_1_1"
    logging.warning(
        f"[TASK] sending to group_name={group_name}, имя канала {channel_layer}")

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_result',
            'message': result
        }
    )
    logging.info('before return result long_task')
    return result


@shared_task()
def askllm_task(user_question: str, hash_token: str):
    """Task for asking LLM"""

    logging.info('Starting askllm_task')

    translated_question = str(
        translate(Mode.RUS_TO_ENG, user_question))

    feedback = query_rag(query_text=translated_question)
    translated_feedback = translate(Mode.ENG_TO_RUS,  feedback)
    logging.info(
        "Результат для запроса %s готов = %s и переведен в %s", hash_token, feedback, translated_feedback)

    channel_layer = get_channel_layer()
    group_name = f"askllm_{hash_token}"
    logging.info(
        "[askllm_task] sending to group_name=%s, имя канала %s", group_name, channel_layer)

    cache.set(f"task_status:{hash_token}", {"status": "done"})
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_result',
            'message': str(translated_feedback)
        }
    )
    logging.info('before return result askllm_task')
    return str(translated_feedback)
