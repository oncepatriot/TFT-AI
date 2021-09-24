
import gym
import numpy as np

import config

from stable_baselines import logger

from .classes import *


ACTIONS_MAP = {
    "BUY_SHOP_POS_1": 0,
    "BUY_SHOP_POS_2": 1,
    "BUY_SHOP_POS_3": 2,
    "BUY_SHOP_POS_4": 3,
    "BUY_SHOP_POS_5": 4,
    "SELL_BENCH_POS_1": 5,
    "SELL_BENCH_POS_2": 6,
    "SELL_BENCH_POS_3": 7,
    "SELL_BENCH_POS_4": 8,
    "SELL_BENCH_POS_5": 9,
    "SELL_BENCH_POS_6": 10,
    "SELL_BENCH_POS_7": 11,
    "SELL_BENCH_POS_8": 12,
    "SELL_BENCH_POS_9": 13,
    "SELL_CHAMPION_POS_1": 14,
    "SELL_CHAMPION_POS_2": 15,
    "SELL_CHAMPION_POS_3": 16,
    "SELL_CHAMPION_POS_4": 17,
    "SELL_CHAMPION_POS_5": 18,
    "SELL_CHAMPION_POS_6": 19,
    "SELL_CHAMPION_POS_7": 20,
    "SELL_CHAMPION_POS_8": 21,
    "SELL_CHAMPION_POS_9": 22,
    "REROLL": 23,
    "BUY_EXP": 24,
    "READY_NEXT_STAGE": 25,
}

ACTIONS_MAP_2 = {
    1: "BUY_SHOP_POS_1",
    2: "BUY_SHOP_POS_2",
    3: "BUY_SHOP_POS_3",
    4: "BUY_SHOP_POS_4",
    5: "BUY_SHOP_POS_5",
    6: "SELL_BENCH_POS_1",
    7: "SELL_BENCH_POS_2",
    8: "SELL_BENCH_POS_3",
    9: "SELL_BENCH_POS_4",
    10: "SELL_BENCH_POS_5",
    11: "SELL_BENCH_POS_6",
    12: "SELL_BENCH_POS_7",
    13: "SELL_BENCH_POS_8",
    14: "SELL_BENCH_POS_9",
    15: "SELL_CHAMPION_POS_1",
    16: "SELL_CHAMPION_POS_2",
    17: "SELL_CHAMPION_POS_3",
    18: "SELL_CHAMPION_POS_4",
    19: "SELL_CHAMPION_POS_5",
    20: "SELL_CHAMPION_POS_6",
    21: "SELL_CHAMPION_POS_7",
    22: "SELL_CHAMPION_POS_8",
    23: "SELL_CHAMPION_POS_9",
    24: "REROLL",
    25: "BUY_EXP",
    26: "FINISHED_WITH_ACTIONS_AND_READY_FOR_NEXT_STAGE",
}



class TeamfightTacticsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(TeamfightTacticsEnv, self).__init__()
        self.name = 'sushigo'
        self.manual = manual

        self.n_players = 8
        self.action_space = gym.spaces.Discrete(len(ACTIONS_MAP.keys()))
        self.observation_space = gym.spaces.Box([])

        # self.players is defined in base class
        # self.current_player_num is defined in base class

        self.verbose = verbose

    @property
    def observation(self):
        """The `observation` function returns a numpy array 
        that can be fed as input to the PPO policy network. It should 
        return a numeric representation of the current game state, 
        from the perspective of the current player, where each element
         of the array is in the range `[-1,1]`.
        """
        
        return "TODO"


    def step(self, action):
        """The `step` method accepts an `action` from the current active player and performs the
        necessary steps to update the game environment. It should also it should 
        update the `current_player_num` to the next player, and check to see if 
        an end state of the game has been reached.

        Arguments:
            action - int - Action integer that maps to an action in the action space
        """

        done = False

        # VALIDATE ACTIONS... Money to buy, If ready cant perform any actions.
        # punish taking actions that are invalid

        if self.legal_actions[action] == 0:
            reward = [1.0/(self.n_players-1)] * self.n_players
            reward[self.current_player_num] = -1

        if action == ACTION_MAPS['READY_NEXT_STAGE']:
            self.current_player.ready = True
        else:
            # PERFORM ACTIONS
            if action in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]:
                print('performing', action)
                print('todo: implement the action...')

        # Update current player to the next player
        self.current_player_num = (self.current_player_num + 1) % self.n_players

        # IF ALL PLAYERS ARE READY:
        # Calculate "combat math" based on all players current boards.
        # Matchmake players against one another, subtract healths
        # Eliminate dead players
        # End game if last player standing
        if all([True if player.ready else False for player in self.players]):
            print('all players are set to ready... TODO: do something.')


        return self.observation, reward, done, {}

    def reset(self):
        """The `reset` method is called to reset the game to the starting state, 
        ready to accept the first action.
        """
        self.current_player_num = 0

        self.players = [
            Player('1'),
            Player('2'),
            Player('3'),
            Player('4'),
            Player('5'),
            Player('6'),
            Player('7'),
            Player('8')
        ]

        self.hero_pool = []


        self.done = False

        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation

    def render(self, mode='human', close=False):
        """The `render` function is called to output a visual or human readable
         summary of the current game state to the log file.
        """
        print("RENDER called")
        print("current player:" , self.current_player)

    def calculate_combat_step_and_update_player_health():
        return

    @property
    def legal_actions(self):
        """The `legal_actions` function returns a numpy vector of the 
        same length as the action space, where 1 indicates that the action is valid 
        and 0 indicates that the action is invalid.
        """
        legal_actions = np.zeros(self.action_space.n)

        legal_actions = np.ones(self.action_space.n)

        return legal_actions




