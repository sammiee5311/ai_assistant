import numpy as np
import pickle


class number_game:
    def __init__(self):
        self.first_digit = np.random.randint(1, 51)

    def __sub__(self, other):
        return self.first_digit - other.first_digit

    def action(self, choice):
        if choice == 0:
            pass
        elif 0 < choice < 6:
            self.plus(choice)
        else:
            self.minus(choice - 5)

    def minus(self, choice):
        self.first_digit -= choice

        if self.first_digit < 1:
            self.first_digit = 1

    def plus(self, choice):
        self.first_digit += choice

        if self.first_digit > 50:
            self.first_digit = 50


class q_learning:
    def __init__(self, ROUND=1, CHANCES=20):
        self.ROUND = ROUND
        self.CHANCES = CHANCES
        self.computer = None
        self.answer = None
        self.q_table = None

    def guess_number(self):
        with open('q_table.pickle', "rb") as file:
            self.q_table = pickle.load(file)

        for episode in range(self.ROUND):
            self.computer = number_game()
            self.answer = number_game()

            # for i in range(self.CHANCES):
            #     obs = self.player - self.answer
            #     choice = np.argmax(self.q_table[obs])
            #
            #     self.player.action(choice)
            #
            #     print(self.player.first_digit, self.answer.first_digit)

if __name__ == '__main__':
    q = q_learning()

    q.guess_number()