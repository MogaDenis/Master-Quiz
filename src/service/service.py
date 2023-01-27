from domain.domain import Question


class QuizNotPossibleException(Exception):
    pass


class QuestionService:
    def __init__(self, question_repo):
        self._repo = question_repo

    def add_question(self, question_arguments, test_state=False):
        """
            This method receives the arguments representing the attributes of a question object, creates it and then sends it to the repository.

        :param question_arguments: List of strings.
        """
        new_question = Question(question_arguments[0], question_arguments[1], question_arguments[2], question_arguments[3], 
        question_arguments[4], question_arguments[5], question_arguments[6])

        self._repo.add_question(new_question, test_state)

        if test_state:
            return new_question

    def get_all(self):
        return self._repo.get_all()

    def create_quiz(self, difficulty, number_of_questions, filename):
        """
            This method creates a quiz. 

        :param difficulty: String.
        :param number_of_questions: Integer, the number of questions that have to be added.
        :param filename: String, the name of the file. 
        :raises QuizNotPossibleException: If the number of questions is greater than the existing number of questions or if there are not enough questions 
        of the required difficulty.
        """

        question_type_count = 0
        if difficulty == 'easy':
            question_type_count = self._repo.easy_count
        elif difficulty == 'medium':
            question_type_count = self._repo.medium_count
        elif difficulty == 'hard':
            question_type_count = self._repo.hard_count

        if number_of_questions > self._repo.total_count:
            raise QuizNotPossibleException

        if number_of_questions // 2 > question_type_count:
            raise QuizNotPossibleException

        # Now we have to create the quiz, choosing firstly the questions that meet the difficulty level, then complete with others. 
        quiz_list = []

        index = 0
        list_of_questions = self.get_all()

        while index < len(list_of_questions) and len(quiz_list) < number_of_questions:
            if list_of_questions[index].difficulty == difficulty:
                quiz_list.append(list_of_questions[index])

            index += 1

        index = 0
        
        while index < len(list_of_questions) and len(quiz_list) < number_of_questions:
            if list_of_questions[index].difficulty != difficulty:
                quiz_list.append(list_of_questions[index])

            index += 1

        # Now let's sort the questions in the quiz. 
        temporary_list = []
        for question in quiz_list:
            if question.difficulty == 'easy':
                temporary_list.append(question)

        for question in quiz_list:
            if question.difficulty == 'medium':
                temporary_list.append(question)

        for question in quiz_list:
            if question.difficulty == 'hard':
                temporary_list.append(question)

        # Now let's save the list into a text file. 
        open_file = open(filename, 'w')

        for question in temporary_list:
            open_file.write(str(question) + '\n')

        open_file.close()