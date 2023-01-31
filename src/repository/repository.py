from domain.domain import Question


class DuplicateQuestionException(Exception):
    pass


class QuestionRepoIterator:
    def __init__(self, repo):
        self._repo = repo
        self._index = 0

    def __iter__(self):
        pass

    def __next__(self):
        if self._index >= len(self._repo):
            raise StopIteration

        self._index += 1

        return self._repo._list_of_questions[self._index - 1]


class QuestionRepo:
    def __init__(self, test_state=False):
        self._list_of_questions = []
        self._easy_count = 0
        self._medium_count = 0
        self._hard_count = 0
        self._total_count = 0
        if not test_state:
            self.load_file('src/master_list.txt')

    @property
    def total_count(self):
        return self._total_count

    @property
    def easy_count(self):
        return self._easy_count

    @property
    def medium_count(self):
        return self._medium_count

    @property
    def hard_count(self):
        return self._hard_count

    @total_count.setter
    def total_count(self, new_value):
        self._total_count = new_value

    @easy_count.setter
    def easy_count(self, new_value):
        self._easy_count = new_value

    @medium_count.setter
    def medium_count(self, new_value):
        self._medium_count = new_value

    @hard_count.setter
    def hard_count(self, new_value):
        self._hard_count = new_value

    def get_all(self):
        return self._list_of_questions[:]

    def add_question(self, new_question, test_state=False):
        """
            This method adds a question to the list. It checks if the given argument is a Question object, raises an Exception if not. 

        :param new_question: Object of class Question.
        :raises TypeError: If the given object is not a Question object.
        :raises DuplicateQuestionException: If there is a question with the same id already.
        """
        if not isinstance(new_question, Question):
            raise TypeError

        for question in self._list_of_questions:
            if question.id == new_question.id:
                raise DuplicateQuestionException

        if new_question.difficulty == 'easy':
            self.easy_count += 1
        elif new_question.difficulty == 'medium':
            self.medium_count += 1
        elif new_question.difficulty == 'hard':
            self.hard_count += 1

        self.total_count += 1

        self._list_of_questions.append(new_question)
        
        if not test_state:
            self.save_file('src/master_list.txt')

    def __iter__(self):
        return QuestionRepoIterator(self)

    def __len__(self):
        return len(self._list_of_questions)

    def save_file(self, filename):
        """
            This method saves the list of questions in the master list text file. 

        :param filename: The name of the file.
        """
        open_file = open(filename, 'w')

        for question in self._list_of_questions:
            open_file.write(str(question) + '\n')

        open_file.close()

    def load_file(self, filename):
        """
            This method loads the questions from the text file.

        :param filename: The name of the file.
        """
        open_file = open(filename, 'r')

        lines = open_file.readlines()

        for line in lines:
            arguments = line.strip().split(';')

            if len(arguments) == 7:
                new_question = Question(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5], arguments[6])

            if new_question.difficulty == 'easy':
                self.easy_count += 1
            elif new_question.difficulty == 'medium':
                self.medium_count += 1
            elif new_question.difficulty == 'hard':
                self.hard_count += 1

            self.total_count += 1

            self._list_of_questions.append(new_question)

        open_file.close()