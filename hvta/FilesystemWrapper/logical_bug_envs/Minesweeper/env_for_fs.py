import re, random
from collections import deque
from typing import Optional, Tuple, List, Dict, Any

import textarena as ta
from textarena.envs.Minesweeper.renderer import create_board_str


class MinesweeperEnv(ta.Env):
    def __init__(self, rows: int = 8, cols: int = 8, num_mines: int = 10, max_turns: int = 100):
        """
        Args:
            rows (int): the number of rows
            cols (int): the number of columns
            num_mines (int): the number of mines
        """
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.max_turns = max_turns

    def get_board_str(self):
        return create_board_str(self.grid, self.revealed, self.flags)

    def reset(self, num_players: int, seed: Optional[int] = None):
        self.state = ta.SinglePlayerState(num_players=num_players, seed=seed,
                                          max_turns=self.max_turns)  ## initialize the game state

        ## initialize the game state
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.first_move = True  # Track if it's the first move to ensure playability

        ## reset the game state
        game_state = {
            "grid": self.grid,
            "revealed": self.revealed,
            "first_move": self.first_move,
            "rendered_board": self._render_board()}
        self.state.reset(game_state=game_state, player_prompt_function=self._generate_player_prompt)
        self.state.add_observation(message=f"Game Board:\n\n{self._render_board()}",
                                   observation_type=ta.ObservationType.GAME_BOARD)


    def step(self, action: str) -> Tuple[bool, ta.Info]:
        self.state.add_observation(from_id=self.state.current_player_id, message=action,
                                   observation_type=ta.ObservationType.PLAYER_ACTION)  ## Update the observation
        match = re.compile(r"\[(\d+)\s(\d+)\]").search(action)  # e.g. [3 2]
        if match is None:
            self.state.set_invalid_move(reward=self._get_percentage_completion(),
                                        reason="You did not respond with valid coordinates in square brackets.")
        else:
            row, col = int(match.group(1)), int(match.group(2))
            if not (0 <= row < self.rows and 0 <= col < self.cols):
                self.state.set_invalid_move(reward=self._get_percentage_completion(),
                                            reason="The specified row and column coordinates are out of bounds.")
            else:
                if self.revealed[row][col]:
                    self.state.add_observation(
                        message=f"Repeated Move done, implement raise error | debug, GT GRID: {self.grid}",
                        observation_type=ta.ObservationType.GAME_ACTION_DESCRIPTION
                    )
                else:
                    if self.first_move:  ## Handle the first move
                        self.clear_all_flags()
                        self.setup_mines(row, col)
                        self.initial_move_pos = (row, col)  # Store the initial move position
                        self.first_move = False

                    queue = deque([(row, col)])  # Start with the initial cell in the queue
                    self.revealed[row][col] = True  # Mark the initial cell as revealed immediately
                    while queue:
                        current_row, current_col = queue.popleft()
                        # Check if it's a mine
                        if self.grid[current_row][current_col] == -1:
                            pct_complete = self._get_percentage_completion()
                            self.revealed[row][col] = False  # Unmark the initial cell as revealed immediately
                            self.state.set_invalid_move(reward=pct_complete,
                                                        reason=f"You hit a mine at ({current_row}, {current_col}).")

                        # If the cell has no adjacent mines, add its neighbors to the queue
                        if self.grid[current_row][current_col] == 0:
                            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                                neighbor_row, neighbor_col = current_row + dr, current_col + dc
                                # Only add to the queue if within bounds and not revealed
                                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                                    if not self.revealed[neighbor_row][neighbor_col]:
                                        self.revealed[neighbor_row][
                                            neighbor_col] = True  # Mark as revealed when adding to queue
                                        queue.append((neighbor_row, neighbor_col))

                    self.state.add_observation(
                        message=f"You revealed the cell at ({row}, {col}).",
                        observation_type=ta.ObservationType.GAME_ACTION_DESCRIPTION
                    )
                    # self.state.add_observation(message=f"Game Board:\n{self._render_board()}", observation_type=ta.ObservationType.GAME_BOARD)

        self.state.game_state["rendered_board"] = self._render_board()  ## Update the rendered board

        ## Check if the game is terminated
        if self._is_solved():
            self.state.set_outcome(reward=1,
                                   reason=f"Congratulations! You have successfully cleared the Minesweeper board.")
        elif self.state.check_turn_limit():
            pct_complete = self._get_percentage_completion()
            self.state.set_outcome(reward=pct_complete,
                                   reason=f"The turn limit has been reached. You successfully uncovered {round(pct_complete * 100)}% of the safe cells.")

        self._observe_current_state()  ## Add the current state to the observations

        return self.state.step()


    def setup_mines(self, safe_row: int, safe_col: int):
        mines = set()
        while len(mines) < self.num_mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            # Avoid placing mines in the safe zone
            if (r, c) not in mines and (r < safe_row - 1 or r > safe_row + 1 or c < safe_col - 1 or c > safe_col + 1):
                mines.add((r, c))
                self.grid[r][c] = -1  # -1 represents a mine
        self.calculate_adjacent_numbers()


    def clear_all_flags(self):
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def _is_solved(self) -> bool:
        # Win condition: all non-mine cells are revealed
        return all(self.revealed[r][c] for r in range(self.rows) for c in range(self.cols) if self.grid[r][c] != -1)