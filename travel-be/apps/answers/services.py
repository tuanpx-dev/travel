from .models import AnswerLikes

def check_like_answer(user, answer):
    count = AnswerLikes.objects.filter(user=user, answer=answer).count()
    return count > 0