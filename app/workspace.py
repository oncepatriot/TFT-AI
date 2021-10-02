import environments.teamfighttactics.teamfighttactics.envs.game_utils as game_utils
import environments.teamfighttactics.teamfighttactics.envs.game_engine as game_engine

players = []
for i in range(8):
	players.append(game_engine.Player(i))

gm = game_engine.GameManager(players)

for i in range(5):
	gm.print_board_state()
	gm.increment_stage_round()
	gm.simulate_combat_step()
	gm.distribute_income()
	gm.roll_all_players_shops()

print("\n\n\n\n\n")
for i in range(40):
	gm.players[3].gold = 99
	if gm.players[3].bench_is_full:
		gm.sell_champion_at_bench_index(gm.players[3], 4)
		gm.players[3].print_player()

	gm.purchase_champion_at_shop_index(gm.players[3],0)

	gm.roll_all_players_shops()

	gm.players[3].print_player()
