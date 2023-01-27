class Question:
    def __init__(self, id, text, choice_a, choice_b, choice_c, correct_choice, difficulty):
        self._id = int(id)
        self._text = text
        self._choice_a = choice_a
        self._choice_b = choice_b
        self._choice_c = choice_c
        self._correct_choice = correct_choice
        self._difficulty = difficulty

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def choice_a(self):
        return self._choice_a

    @property
    def choice_b(self):
        return self._choice_b

    @property
    def choice_c(self):
        return self._choice_c
    
    @property
    def correct_choice(self):
        return self._correct_choice

    @property
    def difficulty(self):
        return self._difficulty

    def format_question(self):
        return f"\nQuestion {self.id}({self.difficulty}): {self.text.title()}?\n\t1) {self.choice_a}\n\t2) {self.choice_b}\n\t3) {self.choice_c}"

    def __str__(self):
        return f"{self.id};{self.text};{self.choice_a};{self.choice_b};{self.choice_c};{self.correct_choice};{self.difficulty}"

