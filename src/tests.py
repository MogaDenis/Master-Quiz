import unittest
from domain.domain import Question
from repository.repository import QuestionRepo, DuplicateQuestionException
from service.service import QuestionService


class TestRepo(unittest.TestCase):
    def setUp(self):
        self.repo = QuestionRepo(test_state=True)

    def test_add_question(self):
        new_question = Question(1, 'text', 1, 2, 3, 2, 'easy')

        # Add the created question to the repository. 
        self.repo.add_question(new_question)

        # Check if the last object is the one added. 
        self.assertEqual(new_question, self.repo.get_all()[-1])

        # Also check that if we try to add it again, we get an exception.
        self.assertRaises(DuplicateQuestionException, self.repo.add_question, new_question)


class TestService(unittest.TestCase):
    def setUp(self):
        self.repo = QuestionRepo(test_state=True)
        self.service = QuestionService(self.repo)

    def test_add_question(self):
        question_arguments = [1, 'text', 1, 2, 3, 2, 'easy']

        # The add method from the service returns the created object only when tested.
        new_question = self.service.add_question(question_arguments, test_state=True)

        # Check if the last object is the one added.
        self.assertEqual(new_question, self.service.get_all()[-1])

        # Also check that if we try to add it again, we get an exception.
        self.assertRaises(DuplicateQuestionException, self.service.add_question, question_arguments)

if __name__ == "__main__":
    unittest.main()

