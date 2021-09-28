import gym
import numpy as np
import config
from stable_baselines import logger
from .classes import *



class TeamfightTacticsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(TeamfightTacticsEnv, self).__init__()
        self.name = 'teamfighttactics'
        self.manual = manual        
        self.n_players = 8

        # Vector of all actions available to an agent
        self.action_space = gym.spaces.Discrete(len(ACTIONS_MAP.keys()))

        # For now, agent only sees all of their tft "board" state such as
        # gold, champion bench, shop, champions. More advanced implementation
        # would allow each agent to see all player's board states.
        self.observation_space = gym.spaces.Box(0, 1, (44,))

        # self.players is defined in base class
        self.current_player_num = 0
        self.verbose = verbose

        # Game state initialized on reset()
        self.game_manager = None
        self.champion_pool = []

    @property
    def observation(self):
        """The `observation` function returns a numpy array 
        that can be fed as input to the PPO policy network. It should 
        return a numeric representation of the current game state, 
        from the perspective of the current player, where each element
        of the array is in the range `[-1,1]`.
        """
        health = self.current_player.health
        gold = self.current_player.gold
        level = self.current_player.level
        experience = self.current_player.experience

        shop_list = self.current_player.shop
        bench = self.current_player.bench
        board = self.current_player.board

        return np.zeros(44)

    def step(self, action):
        """The `step` method accepts an `action` from the current active player and performs the
        necessary steps to update the game environment. It should also it should 
        update the `current_player_num` to the next player, and check to see if 
        an end state of the game has been reached.

        Arguments:
            action - int - Action integer that maps to an action in the action space
        """
        done = False

        reward = [0.0] * self.n_players


        # VALIDATE ACTIONS... Money to buy, If ready cant perform any actions.
        # punish taking actions that are invalid

        if self.legal_actions[action] == 0:
            reward = [1.0/(self.n_players-1)] * self.n_players
            reward[self.current_player_num] = -1
        else:
            self.game_manager.execute_agent_action(self.current_player, action)
     
        # Update current player to the next player
        self.current_player_num = (self.current_player_num + 1) % self.n_players

        # IF ALL PLAYERS ARE READY:
        # Calculate "combat math" based on all players current boards.
        # Matchmake players against one another, subtract healths
        # Eliminate dead players
        # End game if last player standing
        if all([True if player.ready else False for player in self.players]):
            self.game_manager.stage += 1
            self.game_manager.simulate_combat_step()
            self.game_manager.distribute_stage_income()
            self.game_manager.roll_all_players_shops()

            if self.game_manager.check_game_over():
                print("GAME OVER")
                done = True

        return self.observation, reward, done, {}

    def reset(self):
        """The `reset` method is called to reset the game to the starting state, 
        ready to accept the first action.
        """
        print("CALLED RESET")
        self.current_player_num = 0
        self.players = [
            Player('0'),
            Player('1'),
            Player('2'),
            Player('3'),
            Player('4'),
            Player('5'),
            Player('6'),
            Player('7')
        ]
        self.game_manager = GameManager(self.players)
        self.game_manager.create_champion_pool()

        self.done = False

        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation

    def render(self, mode='human', close=False):
        """The `render` function is called to output a visual or human readable
         summary of the current game state to the log file.
        """
        return

    @property
    def legal_actions(self):
        """The `legal_actions` function returns a numpy vector of the 
        same length as the action space, where 1 indicates that the action is valid 
        and 0 indicates that the action is invalid.
        """
        legal_actions = np.zeros(self.action_space.n)

        current_player = self.current_player
        gold = current_player.gold
        shop = current_player.shop
        bench = current_player.bench
        board = current_player.bench
        level = current_player.level

        # Buy shop slot is legal if affordable
        legal_actions[0] = 1 if shop[0] and shop[0].cost <= gold else 0
        legal_actions[1] = 1 if shop[1] and shop[1].cost <= gold else 0
        legal_actions[2] = 1 if shop[2] and shop[2].cost <= gold else 0
        legal_actions[3] = 1 if shop[3] and shop[3].cost <= gold else 0
        legal_actions[4] = 1 if shop[4] and shop[4].cost <= gold else 0

        # Sell Bench legal if bench slot is occupied
        num_bench_units = len(bench)
        legal_actions[5] = 1 if bench[0] else 0
        legal_actions[6] = 1 if bench[1] else 0
        legal_actions[7] = 1 if bench[2] else 0
        legal_actions[8] = 1 if bench[3] else 0
        legal_actions[9] = 1 if bench[4] else 0
        legal_actions[10] = 1 if bench[5] else 0
        legal_actions[11] = 1 if bench[6] else 0
        legal_actions[12] = 1 if bench[7] else 0
        legal_actions[13] = 1 if bench[8] else 0

        # Sell Champion on board legal if board spot is occupied
        legal_actions[14] = 1 if board[0] else 0
        legal_actions[15] = 1 if board[1] else 0
        legal_actions[16] = 1 if board[2] else 0
        legal_actions[17] = 1 if board[3] else 0
        legal_actions[18] = 1 if board[4] else 0
        legal_actions[19] = 1 if board[5] else 0
        legal_actions[20] = 1 if board[6] else 0
        legal_actions[21] = 1 if board[7] else 0
        legal_actions[22] = 1 if board[8] else 0

        # TODO: Move champ from bench to board is legal if board
        # has an unoccupied space and bench spot is occupied
        legal_actions[23] = 0
        legal_actions[24] = 0
        legal_actions[25] = 0
        legal_actions[26] = 0
        legal_actions[27] = 0
        legal_actions[28] = 0
        legal_actions[29] = 0
        legal_actions[30] = 0
        legal_actions[31] = 0

        # TODO: Move champ from board to bench is legal if 
        # has unoccupied space on bench
        legal_actions[32] = 0
        legal_actions[33] = 0
        legal_actions[34] = 0
        legal_actions[35] = 0
        legal_actions[36] = 0
        legal_actions[37] = 0
        legal_actions[38] = 0
        legal_actions[39] = 0
        legal_actions[40] = 0

        # Reroll is legal if can afford
        legal_actions[41] = 1 if gold >= 2 else 0

        # Buy exp is legal if can afford
        legal_actions[42] = 1 if gold >= 4 else 0

        # Ready for next stage legal:
        legal_actions[43] = 1

        return legal_actions

    @property
    def current_player(self):
        return self.players[self.current_player_num]