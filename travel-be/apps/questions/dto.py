from .services import check_like_question
from .serializers import QuestionSerializer

class UserQuestion(object):
    def __init__(self, user, question):
        self.user = user
        self.question = question
        self.like = check_like_question(user, question)

    def data(self):
        serializer = QuestionSerializer(self.question)
        result = serializer.data
        result['like'] = self.like

        return result

class UserQuestions(object):
    def __init__(self, user, questions):
        self.user = user
        self.questions = questions

    def data(self):
        return [UserQuestion(self.user, question).data() for question in self.questions]
