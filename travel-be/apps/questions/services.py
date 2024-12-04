from .models import QuestionLikes

def check_like_question(user, question):
    count = QuestionLikes.objects.filter(user=user, question=question).count()
    return count > 0