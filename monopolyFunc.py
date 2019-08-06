# 38 slots
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


class Tile:
    # INIT
    def __init__(self, idx):
        self.type = None
        self.numVisits = 0
        self.id = idx

    def make_property(self, Name, base_price):
        self.type = "property"
        self.owner = None
        self.property = Property(self.id, Name)
        self.property.set_base_price(base_price)

    def make_chance(self):
        self.type = "chance"

    def make_community(self):
        self.type = "community"

    def make_go(self):
        self.type = "go"

    def make_tax(self, tax):
        self.type = "tax"
        self.tax = tax

    def make_GOTOJAIL(self):
        self.type = "GOTOJAIL"

    def make_JAIL(self):
        self.type = "JAIL"

    def make_parking(self):
        self.type = "parking"
        self.parking_prize = 0

    def visit(self):
        self.numVisits = self.numVisits + 1
        if self.type == "GOTOJAIL":
            return "JAIL"
        elif self.type == "chance":
            return "CHANCE"
        elif self.type == "community":
            return "COMMUN"
        else:
            return None


class GameBoard:
    def __init__(self, num_players):
        # Build Board and Players
        self.board = self.__createGameBoard__()
        self.num_players = num_players
        self.players = [Player(i) for i in range(num_players)]

        # Meta
        self.turns_per_game = 100
        self.game_iterations = 200
        self.game_results = []

        # Decks
        self.comm_deck = np.arange(0, 16, 1)
        np.random.shuffle(self.comm_deck)
        self.chancedeck = np.arange(0, 16, 1)
        np.random.shuffle(self.chancedeck)

    def __reset__(self):
        # Build Board
        self.board = self.__createGameBoard__()
        del self.players
        self.players = [Player(i) for i in range(self.num_players)]

        # Decks
        self.comm_deck = np.arange(0, 16, 1)
        np.random.shuffle(self.comm_deck)
        self.chancedeck = np.arange(0, 16, 1)
        np.random.shuffle(self.chancedeck)

    def __createGameBoard__(self):
        GameBoard = [Tile(i) for i in range(40)]

        # Set speacial tiles
        GameBoard[0].make_go()
        GameBoard[2].make_community()
        GameBoard[4].make_tax(200)
        GameBoard[7].make_chance()
        GameBoard[10].make_JAIL()
        GameBoard[17].make_community()
        GameBoard[20].make_parking()
        GameBoard[22].make_chance()
        GameBoard[30].make_GOTOJAIL()
        GameBoard[33].make_community()
        GameBoard[36].make_chance()
        GameBoard[38].make_tax(100)

        # Utilities
        GameBoard[12].make_property("Electric Company", 150)
        GameBoard[28].make_property("Water Works", 150)

        # Train Stations
        GameBoard[5].make_property("Kings Cross", 200)
        GameBoard[15].make_property("Marylebone Station", 200)
        GameBoard[25].make_property("Fenchurch St. Station", 200)
        GameBoard[35].make_property("Liverpool Street Station", 200)

        # Brown Set
        GameBoard[1].make_property("Old Kent Road", 60)
        GameBoard[3].make_property("Whitechapel Road", 60)

        # Light Blue Set
        GameBoard[6].make_property("The Angel, Islington", 100)
        GameBoard[8].make_property("Euston Road", 100)
        GameBoard[9].make_property("Pentonville Road", 120)

        # Pink Set
        GameBoard[11].make_property("Pall Mall", 140)
        GameBoard[13].make_property("White Hall", 140)
        GameBoard[14].make_property("Northumblroad Avenue", 160)

        # Orange Set
        GameBoard[16].make_property("Bow Street", 180)
        GameBoard[18].make_property("Marlborough Street", 180)
        GameBoard[19].make_property("Vine Street", 200)

        # Red Set
        GameBoard[21].make_property("Strand", 220)
        GameBoard[23].make_property("Fleet Street", 220)
        GameBoard[24].make_property("Trafalgar Square", 240)

        # Yellow Set
        GameBoard[26].make_property("Leicester Square", 260)
        GameBoard[27].make_property("Coventry Street", 260)
        GameBoard[29].make_property("Piccadilly", 280)

        # Green Set
        GameBoard[31].make_property("Regent Street", 300)
        GameBoard[32].make_property("Oxford Street", 300)
        GameBoard[34].make_property("Bond Street", 320)

        # Dark Blue Set
        GameBoard[37].make_property("Park Lane", 350)
        GameBoard[39].make_property("MayFair", 400)

        return GameBoard

    def __pick_chance_return__(self):
        card_idx = self.chancedeck[0]
        for i in range(len(self.chancedeck)):
            if i == 15:
                self.chancedeck[i] = card_idx
            else:
                self.chancedeck[i] = self.chancedeck[i+1]
        return card_idx

    def __pickup_chance_card__(self):
        card_idx = self.__pick_chance_return__()

        # Take action based of card picked
        if card_idx == 0 or card_idx == 6:
            # Advance to next train station
            curr_loc = self.curr_idx
            if curr_loc < 5 or curr_loc > 35:
                self.curr_idx = 5
                self.board[self.curr_idx].visit()
            elif curr_loc < 15:
                self.curr_idx = 15
                self.board[self.curr_idx].visit()
            elif curr_loc < 25:
                self.curr_idx = 25
                self.board[self.curr_idx].visit()
            elif curr_loc < 35:
                self.curr_idx = 35
                self.board[self.curr_idx].visit()
            return
        if card_idx == 1:
            # Advance to pall mall
            self.curr_idx = 11
            self.board[self.curr_idx].visit()
            return
        if card_idx == 2:
            # Advance to next utility
            curr_loc = self.curr_idx
            if curr_loc < 12 or curr_loc > 28:
                self.curr_idx = 12
                self.board[self.curr_idx].visit()
            else:
                self.curr_idx = 28
                self.board[self.curr_idx].visit()
            return
        if card_idx == 3:
            # Advance to GO
            self.curr_idx = 0
            self.board[self.curr_idx].visit()
            return
        if card_idx == 4:
            # Advance to next utility
            self.__GOTOJAIL__()
            return
        if card_idx == 5:
            # Advance to next Mayfair
            self.curr_idx = 39
            self.board[self.curr_idx].visit()
            return
        if card_idx == 7:
            # Advance to next Kings cross station
            self.curr_idx = 5
            self.board[self.curr_idx].visit()
            return
        if card_idx == 8:
            # Advance to next Trafalgarsquare
            self.curr_idx = 14
            self.board[self.curr_idx].visit()
            return
        if card_idx == 9:
            # Go back 3 spaces
            self.curr_idx = self.curr_idx - 3
            self.board[self.curr_idx].visit()
            return
        if card_idx == 10:
            # Get out of jial card
            self.numberGetOutOfJailCards += 1
            return

        # Create Random number and compare to cummilator to
        # determine which event occurs
        # cumilator = 0.0
        # random = np.random.uniform(0,1)

        # cumilator = cumilator + pr_GOTOJAIL
        # if random <= cumilator:
        #     self.__GOTOJAIL__()
        #     return

        # cumilator = cumilator + pr_GOTO11
        # if random <= cumilator:
        #     self.curr_idx = 11
        #     # Jump by chance or cummunity never results in chain action
        #     self.board[self.curr_idx].visit()

    def __pick_commun_return__(self):
        card_idx = self.comm_deck[0]
        for i in range(len(self.comm_deck)):
            if i == 15:
                self.comm_deck[i] = card_idx
            else:
                self.comm_deck[i] = self.comm_deck[i+1]
        return card_idx

    def __pickup_community_card__(self):

        # Pick a card and return to bottom of deck
        card_idx = self.__pick_commun_return__()

        # Take action based of card picked
        if card_idx == 0:
            self.numberGetOutOfJailCards += 1
            return
        if card_idx == 1:
            self.curr_idx = 0
            self.board[self.curr_idx].visit()
            return
        if card_idx == 2:
            self.__GOTOJAIL__()
            return

        # We don not care about other community cards
        return

        # Create Random number and compare to cummilator to
        # determine which event occurs
        # cumilator = 0.0
        # random = np.random.uniform(0,1)

        # cumilator = cumilator + pr_GOTOJAIL
        # if random <= cumilator:
        #     self.__GOTOJAIL__()
        #     return

        # cumilator = cumilator + pr_GOTO11
        # if random <= cumilator:
        #     self.curr_idx = 11
        #     # Jump by chance or cummunity never results in chain action
        #     self.board[self.curr_idx].visit()

    def __update_prison_state__(self):
        # Returns true if released from prison along with roll thourgh
        total = 0
        self.turns_in_prison = self.turns_in_prison + 1
        # Presumption: never use money to pay out, only card, double or wait three turns
        if self.turns_in_prison == 3:
            self.imprisoned = False
            return True, None
        elif self.numberGetOutOfJailCards:
            # Use get out of jail free card
            self.numberGetOutOfJailCards = self.numberGetOutOfJailCards - 1
            self.imprisoned = False
            return True, None
        else:
            total, die_1, die_2 = self.__roll__()
            if die_1 == die_2:
                self.imprisoned = False
                return True, total
        return False, total

    def __evaluate_action_tile__(self, action):
        if not action:
            return
        if action == "JAIL":
            self.__GOTOJAIL__()
        elif action == "CHANCE":
            self.__pickup_chance_card__()
        elif action == "COMMUN":
            self.__pickup_community_card__()
        else:
            print("ERROR: __evaluate_action_tile__ could not identify action: ", action)
            quit()

    def __roll__(self):
        dice_1 = int(np.floor(np.random.uniform(1, 7)))
        dice_2 = int(np.floor(np.random.uniform(1, 7)))
        return dice_1 + dice_2, dice_1, dice_2

    def __take_turn__(self):
        # If we roll a double to escape prison, we do not need to roll again
        need_dice_roll = True
        if self.imprisoned == True:
            released, roll_val = self.__update_prison_state__()
            if not released:
                return
            else:
                if roll_val:
                    need_dice_roll = False

        # If we werent in prison or left prison without the need for a double roll(success),
        # we need to roll
        if need_dice_roll:
            roll_val, _, _ = self.__roll__()

        # Update curr position and activate that tile
        self.curr_idx = (self.curr_idx + roll_val) % 40
        action = self.board[self.curr_idx].visit()

        # If we landed on an iteresting tile, act accordingly
        self.__evaluate_action_tile__(action)

    def __run_game__(self):
        for i in range(self.turns_per_game):
            self.__take_turn__()

        table = []
        for tile in self.board:
            table.append(tile.numVisits)
        sm_table = sum(table)
        for i in range(len(table)):
            table[i] = table[i]/sm_table

        self.__reset__()
        return table

    def run(self):
        self.game_results = np.array(
            [self.__run_game__() for i in range(self.game_iterations)])

    def printHeatMap(self):
        # Calculate means pre-emptivly for colour coding
        means = sum(self.game_results)/len(self.game_results)

        d = self.game_results.flatten()
        tile_arr = np.tile(np.arange(0, 40, 1), self.game_iterations)

        df = pd.DataFrame()
        df['Prob'] = d
        df['Tile'] = tile_arr

        norm = plt.Normalize(means.min(), means.max())
        cmap = plt.get_cmap("magma")
        normalized_probs = 1-norm(means)

        sns.barplot(x='Tile', y='Prob', data=df,
                    palette=cmap(normalized_probs))
        plt.title("Monopoly: PMF Analysis of a Player Landing on a Tile")
        plt.ylabel("PMF")
        plt.xlabel("Tile Index")
        plt.show()


class Player:
    def __init__(self, idx):
        self.id = idx
        self.properties = []
        self.curr_idx = 0

        # Prison Variables
        self.imprisoned = False
        self.turns_in_prison = 0
        self.numberGetOutOfJailCards = 0

    def __GOTOJAIL__(self):
        self.imprisoned = True
        self.turns_in_prison = 0
        self.curr_idx = 10


class Property:
    def __init__(self, tile_id, name):
        self.id = tile_id
        self.siblings = []
        self.base_price = None
        self.name = name

    def make_set(self, prop):
        self.siblings.append(prop)

    def set_base_price(self, price):
        self.base_price = price


def main():
    # Create Gameboard with four players
    game = GameBoard(4)
    game.game_iterations = 500000
    game.turns_per_game = 100

    # Run Simulation
    game.run()

    # Print Results
    game.printHeatMap()


main()
