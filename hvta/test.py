""" A minimal script showing how to run textarena locally """

import textarena as ta
from hvta.FilesystemWrapper import FilesystemWrapper

agents = {
    0: ta.agents.HumanAgent(),
}

# agents = {
#     0: ta.agents.OpenRouterAgent(model_name="openai/gpt-5-mini"),
# }

# initialize the environment
env = ta.make(env_id="TowerOfHanoi-v0")
env = FilesystemWrapper(env=env, hidden_solution=True, logical_bug=True)
env.reset(num_players=len(agents))

# main game loop
done = False
while not done:
  player_id, observation = env.get_observation()
  action = agents[player_id](observation)
  print(action)
  done, step_info = env.step(action=action)
  if step_info.get("reward_hack"):
    print("\033[33m[HACK DETECTED] A hack was triggered in this step!\033[0m")
rewards, game_info = env.close()
print(rewards)
print(game_info)
