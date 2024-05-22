class CreateQuestionException(Exception):
    """Ошибка обработки или формирования вопросов"""
    pass


class NotFileException(Exception):
    """Ошибка открытия файла с анкетой"""
    pass
