import environments.teamfighttactics.teamfighttactics.envs.game_utils as game_utils
import environments.teamfighttactics.teamfighttactics.envs.game_engine as game_engine

players = []
for i in range(8):
	players.append(game_engine.Player(i))

gm = game_engine.GameManager(players)

for i in range(40):
	gm.increment_stage_round()
	gm.simulate_combat_step()
	gm.distribute_income()
	gm.roll_all_players_shops()
	gm.print_board_state()

