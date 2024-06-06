class CreateQuestionException(Exception):
    """Ошибка обработки или формирования вопросов"""

    def __init__(self, *args) -> object:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:

        if self.message:
            return 'QuestionError, {0} '.format(self.message)
        else:
            return ''


class CreateSurveyException(Exception):
    """Ошибка формирования анкеты"""

    def __init__(self, *args) -> object:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:

        if self.message:
            return 'SurveyError, {0} '.format(self.message)
        else:
            return ''
