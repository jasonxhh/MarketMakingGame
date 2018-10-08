import numpy as np
import select
import sys


# Class for user input timeout exception
class TimeoutExpired(Exception):
    pass

# Basic game, get one inefficiently priced market price and user gets unlimited time to either buy or sell
class basic:
    # Input the number of unknown numbers, as well as the range of possible numbers to sample from
    def __init__(self, num_unknowns, range_of_numbers):
        self.unknowns = num_unknowns
        self.numbers = range_of_numbers

    # Method to get a random subset of size number of unknowns from the list of possible numbers
    def get_nums(self):
        random_nums = self.numbers
        np.random.shuffle(random_nums)
        return [random_nums[0:(self.unknowns)], sum(random_nums[0:(self.unknowns)])]

    # Method to return the list of possible numbers, given a number from the unknowns is revealed
    def get_possible_unknown_nums(self, numbers_possible, revealed_number):
        possible_unknowns = list()
        for x in numbers_possible:
            if x != revealed_number:
                possible_unknowns.append(x)
        return possible_unknowns

    # Method to get user decision of whether to buy or sell
    def user_decision(self):
        decision = input("Buy or Sell? Enter 'b' to Buy or 's' to sell\n")
        return decision

    # Method to play the game
    def play(self):
        information = self.get_nums()
        profit = 0
        numbers = information[0]
        value = information[1]
        reveals_left = self.unknowns
        price = np.mean(self.numbers) * self.unknowns + np.random.normal(scale = 0.5)
        print("Current market price: ", price)
        stop = False
        while not stop:
            decision = self.user_decision()
            if decision == "b":
                profit += (value - price)
                stop = True
            elif decision == "s":
                profit += (price - value)
                stop = True
            else:
                print("You failed to make a transaction! Try again!")
        possible_unknowns = self.numbers
        for i in range(0, self.unknowns-1):
            print("Revealed number: ", numbers[reveals_left-1])
            possible_unknowns = self.get_possible_unknown_nums(possible_unknowns, numbers[reveals_left-1])
            expected_value = sum(numbers[reveals_left-1:self.unknowns]) + (reveals_left-1)*np.mean(possible_unknowns)
            price = expected_value + np.random.normal(scale = 0.5)
            print("Current market price: ", price)
            stop = False
            while not stop:
                decision = self.user_decision()
                if decision == "b":
                    profit += (value - price)
                    stop = True
                elif decision == "s":
                    profit += (price - value)
                    stop = True
                else:
                    print("You failed to make a transaction! Try Again!")
            reveals_left -= 1
        print("Final number: ", numbers[reveals_left - 1])
        print("Your net profit is: ", profit)
        return None

class advanced:
    # Input the number of unknown numbers, as well as the range of possible numbers to sample from
    def __init__(self, num_unknowns, range_of_numbers):
        self.unknowns = num_unknowns
        self.numbers = range_of_numbers
        self.out_of_time = False

    # Method to get a random subset of size number of unknowns from the list of possible numbers
    def get_nums(self):
        random_nums = self.numbers
        np.random.shuffle(random_nums)
        return [random_nums[0:(self.unknowns)], sum(random_nums[0:(self.unknowns)])]

    # Method to return the list of possible numbers, given a number from the unknowns is revealed
    def get_possible_unknown_nums(self, numbers_possible, revealed_number):
        possible_unknowns = list()
        for x in numbers_possible:
            if x != revealed_number:
                possible_unknowns.append(x)
        return possible_unknowns

    # Function to get user input with time limit
    # Source: https://stackoverflow.com/questions/15528939/python-3-timed-input
    def input_with_timeout(self, timeout):
        sys.stdout.flush()
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready:
            return sys.stdin.readline().rstrip('\n')  # expect stdin to be line-buffered
        raise TimeoutExpired

    # Method to play the game
    def play(self):
        information = self.get_nums()
        profit = 0
        numbers = information[0]
        value = information[1]
        reveals_left = self.unknowns
        expected_value = np.mean(self.numbers) * self.unknowns
        print("Starting expected value: ", expected_value, "\n")
        print("For all quotes; Enter 'b' to Buy or 's' to sell\n")
        possible_unknowns = self.numbers
        for i in range(0, self.unknowns-1):
            for i in range(1, 5):
                try:
                    noise = np.sqrt(10 - i) * np.random.normal(scale=0.25)
                    bid = expected_value + noise - abs(np.random.normal(scale=0.25))
                    ask = expected_value + noise + abs(np.random.normal(scale=0.25))
                    print("Bid: ", bid, "Ask: ", ask)
                    decision = self.input_with_timeout(10)
                    if decision == "b":
                        profit += (value - ask)
                    elif decision == "s":
                        profit += (bid - value)
                    else:
                        print("You failed to make a transaction due to liquidity!")
                except TimeoutExpired:
                    continue
            print("\nRevealed number: ", numbers[reveals_left-1], "\n")
            possible_unknowns = self.get_possible_unknown_nums(possible_unknowns, numbers[reveals_left-1])
            expected_value = sum(numbers[reveals_left-1:self.unknowns]) + (reveals_left-1)*np.mean(possible_unknowns)
            for j in range(1, 5):
                try:
                    noise = np.sqrt(5 - i) * np.random.normal(scale=0.25)
                    bid = expected_value + noise - abs(np.random.normal(scale=0.25))
                    ask = expected_value + noise + abs(np.random.normal(scale=0.25))
                    print("Bid: ", bid, "Ask: ", ask)
                    decision = self.input_with_timeout(10)
                    if decision == "b":
                        profit += (value - ask)
                    elif decision == "s":
                        profit += (bid - value)
                    else:
                        print("You failed to make a transaction due to liquidity!")
                except TimeoutExpired:
                    continue
            reveals_left -= 1
        print("\n\nFinal number: ", numbers[reveals_left - 1])
        print("Your net profit is: ", profit)
        return None
