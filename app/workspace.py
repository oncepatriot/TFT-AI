import environments.teamfighttactics.teamfighttactics.envs.game_utils as game_utils
import environments.teamfighttactics.teamfighttactics.envs.game_engine as game_engine

players = []
for i in range(8):
	players.append(game_engine.Player(i))

gm = game_engine.GameManager(players)

for i in range(80):
	gm.increment_stage_round()
	gm.simulate_combat_step()
	gm.distribute_income()
	gm.roll_all_players_shops()
	for p in players:
		gm.execute_agent_action(p, 0) # purchase champ at shop 1
	gm.print_board_state()

