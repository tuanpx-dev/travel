from .services import check_like_answer
from .serializers import AnswerSerializer

class UserAnswer(object):
    def __init__(self, user, answer):
        self.user = user
        self.answer = answer
        self.like = check_like_answer(user, answer)

    def data(self):
        serializer = AnswerSerializer(self.answer)
        result = serializer.data
        result['like'] = self.like

        return result

class UserAnswers(object):
    def __init__(self, user, answers):
        self.user = user
        self.answers = answers

    def data(self):
        return [UserAnswer(self.user, answer).data() for answer in self.answers]
