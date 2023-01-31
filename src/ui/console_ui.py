from domain.domain import Question
from repository.repository import QuestionRepo
from service.service import QuestionService, QuizNotPossibleException


class InvalidInputException(Exception):
    pass


class ConsoleUI:
    def __init__(self):
        self._repo = QuestionRepo()
        self._service = QuestionService(self._repo)

    def invalid_input_message(self):
        print("\nInvalid input!")

    def impossible_quiz_required(self):
        print("\nCould not create the requied quiz!")

    def quiz_not_existent(self):
        print("\nThe required quiz does not exist!")

    def execute_user_command(self):
        user_command = input("\n>> ").strip()

        tokens = user_command.split(' ')

        if tokens[0] not in ['add', 'create', 'start', 'exit']:
            raise InvalidInputException

        if tokens[0] == 'add':
            arguments = tokens[1].split(';')

            if len(arguments) != 7:
                raise InvalidInputException

            if not arguments[0].isnumeric():
                raise InvalidInputException

            if arguments[-1] not in ['easy', 'medium', 'hard']:
                raise InvalidInputException

            if arguments[-2] not in [arguments[-3], arguments[-4], arguments[-5]]:
                raise InvalidInputException

            self._service.add_question(arguments)

        elif tokens[0] == 'create':
            if len(tokens) != 4:
                raise InvalidInputException

            difficulty = tokens[1]
            number_of_questions = tokens[2]
            filename = tokens[3]

            if difficulty not in ['easy', 'medium', 'hard']:
                raise InvalidInputException

            if not number_of_questions.isnumeric():
                raise InvalidInputException

            try:
                self._service.create_quiz(difficulty, int(number_of_questions), filename)
            except QuizNotPossibleException:
                self.impossible_quiz_required()

        elif tokens[0] == 'start':
            # Take the quiz. 
            filename = tokens[1]

            score = 0

            try:
                open_file = open(f"src/{filename}", 'r')

                lines = open_file.readlines()

                quiz_list = []

                for line in lines:
                    arguments = line.strip().split(';')
                    if len(arguments) == 7:
                        new_question = Question(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5], arguments[6])
                        quiz_list.append(new_question)

                for question in quiz_list:
                    print(question.format_question())
                    user_choice = input("\nYour answer(the index): ").strip()

                    while user_choice not in ['1', '2', '3']:
                        self.invalid_input_message()
                        user_choice = input("\nYour answer(the index): ").strip()

                    user_answer = question.choice_a
                    if user_choice == '2':
                        user_answer = question.choice_b
                    elif user_choice == '3':
                        user_answer = question.choice_c

                    if user_answer == question.correct_choice:
                        if question.difficulty == 'easy':
                            score += 1
                        elif question.difficulty == 'medium':
                            score += 2
                        elif question.difficulty == 'hard':
                            score += 3

                print(f"\n\tYour score: {score}")
 
            except OSError:
                self.quiz_not_existent()

        elif tokens[0] == 'exit':
            return not None

    def start(self):
        while True:
            while True:
                try:
                    run = self.execute_user_command()
                    break
                except InvalidInputException:
                    self.invalid_input_message()

            if run is not None:
                break