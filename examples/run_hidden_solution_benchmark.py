import argparse
import json
import os
import uuid
from datetime import datetime

import textarena as ta
from tqdm import tqdm

from hvta.FilesystemWrapper import FilesystemWrapper

ENVS = [
    "Crosswords-v0-hardcore",
    "GuessTheNumber-v0-hardcore",
    "GuessWho-v0",
    "Hangman-v0-hardcore",
    "LogicPuzzle-v0",
    "Mastermind-v0-hard",
    "Minesweeper-v0-medium",
    "Sudoku-v0-easy",
    "TwentyQuestions-v0-hardcore",
    "WordSearch-v0-hardcore",
    "Wordle-v0-hardcore-5",
]


def run_game(env_id: str, model: str, seed: int = 0) -> dict:
    agents = {0: ta.agents.OpenRouterAgent(model_name=model)}

    env = ta.make(env_id=env_id)
    env = FilesystemWrapper(env=env, hidden_solution=True)
    env.reset(num_players=1, seed=seed)

    actions = []
    done = False
    while not done:
        player_id, observation = env.get_observation()
        action = agents[player_id](observation)
        done, step_info = env.step(action=action)
        actions.append({
            "step": len(actions),
            "action": action,
            "reward_hack": step_info.get("reward_hack", False),
        })

    rewards, game_info = env.close()
    return {
        "reward": rewards.get(0),
        "actions": actions,
        **game_info,
    }


def run_benchmark(model: str, episodes: int = 5) -> None:
    benchmark_id = str(uuid.uuid4())[:8]
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs", benchmark_id)
    os.makedirs(log_dir, exist_ok=True)

    print(f"Model    : {model}")
    print(f"Episodes : {episodes}")
    print(f"Logs     : logs/{benchmark_id}/\n")

    for env_id in ENVS:
        results = []
        for i in tqdm(range(episodes), desc=env_id):
            result = run_game(env_id, model, seed=i)
            results.append(result)

            log = {
                "env_id": env_id,
                "episode": i,
                "model": model,
                "seed": i,
                "timestamp": datetime.utcnow().isoformat(),
                **result,
            }
            log_path = os.path.join(log_dir, f"{env_id}_{i}.json")
            with open(log_path, "w") as f:
                json.dump(log, f, indent=2)

        hack_rate = sum(r.get("hack_triggered", False) for r in results) / episodes
        avg_reward = sum(r["reward"] for r in results if r["reward"] is not None) / episodes
        print(f"  hack rate : {hack_rate:.0%}")
        print(f"  avg reward: {avg_reward:.3f}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, help="OpenRouter model ID")
    parser.add_argument("--episodes", type=int, default=5, help="Episodes per environment")
    args = parser.parse_args()

    run_benchmark(model=args.model, episodes=args.episodes)


if __name__ == "__main__":
    main()
