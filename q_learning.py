import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
import collections

style.use('ggplot')


class number_game:
    def __init__(self):
        self.first_digit = np.random.randint(1,51)

    def __sub__(self, other):
        return self.first_digit - other.first_digit

    def action(self, choice):
        if choice == 0:
            pass
        elif 0 < choice < 6:
            self.plus(choice)
        else:
            self.minus(choice-5)

    def minus(self,choice):
        self.first_digit -= choice

        if self.first_digit < 1:
            self.first_digit = 1

    def plus(self,choice):
        self.first_digit += choice

        if self.first_digit > 50:
            self.first_digit = 50


class q_learn:
    def __init__(self):
        self.EPISODES = 30000
        self.MOVE_PENALTY = -1
        self.ANSWER_REWARD = 50
        self.HALF_REWARD = 20
        self.epsilon = 0.9
        self.EPS_DECAY = 0.99998
        self.SHOW_EVERY = 500

        self.LEARNING_RATE = 0.001
        self.DISCOUNT = 0.95
        self.STEP = 600

    def main(self):
        q_table = collections.defaultdict(list)

        for d1 in range(-49, 50):
            q_table[d1] = [0 for _ in range(12)]

        episode_rewards = []

        for episode in range(self.EPISODES):
            player = number_game()
            answer = number_game()

            if episode % self.SHOW_EVERY == 0:
                print("# : %d, epsilon : %f" %(episode, self.epsilon))
                print(f'{self.SHOW_EVERY} ep mean {np.mean(episode_rewards[-self.SHOW_EVERY:])}')

            if episode % 1000 == 0 and episode != 0:
                show = True
            else:
                show = False

            episode_reward = 0
            for i in range(self.STEP):
                obs = player - answer
                if np.random.random() > self.epsilon:
                    choice = np.argmax(q_table[obs])
                else:
                    choice = np.random.randint(0,12)

                player.action(choice)
                if player.first_digit == answer.first_digit:
                    reward = self.ANSWER_REWARD
                else:
                    reward = self.MOVE_PENALTY

                new_obs = player - answer
                max_future_q = np.argmax(q_table[new_obs])
                current_q = q_table[obs][choice]

                if reward == self.ANSWER_REWARD:
                    new_q = self.ANSWER_REWARD
                else:
                    new_q = (1-self.LEARNING_RATE) * current_q + self.LEARNING_RATE * (reward+self.DISCOUNT*max_future_q)

                q_table[obs][choice] = new_q

                if show:
                    print(player.first_digit,answer.first_digit)

                episode_reward += reward
                if reward == self.ANSWER_REWARD:
                    break

            episode_rewards.append(episode_reward)
            self.epsilon *= self.EPS_DECAY

        print(q_table)

        moving_avg = np.convolve(episode_rewards, np.ones((self.SHOW_EVERY,)) / self.SHOW_EVERY, mode='valid')

        plt.plot([i for i in range(len(moving_avg))], moving_avg)
        plt.ylabel("reward %d" % self.SHOW_EVERY)
        plt.xlabel("episode #")
        plt.show()

        with open("q_table.pickle", "wb") as file:
            pickle.dump(q_table, file)