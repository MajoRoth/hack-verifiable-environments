import re, random, copy
from typing import Any, Dict, Optional, Tuple, List

import textarena as ta
from textarena.envs.Sudoku.renderer import create_board_str


class SudokuEnv(ta.Env):
    def __init__(self, clues: int = 30, max_turns: Optional[int] = 100):
        """
        Args:
            clues (str): The number of clues.
            max_turns (int): The maximum number of moves allowed.
        """
        self.clues = clues
        self.max_turns = max_turns

    def get_board_str(self):
        return create_board_str(board=self.game_board)

    def _generate_board(self) -> List[List[int]]:
        full_grid = self._generate_full_grid()  ## generate a full grid
        puzzle_grid = self._remove_cells(full_grid, self.clues)  ## remove cells to create puzzle
        return full_grid, puzzle_grid

    def _find_empty(self, grid: List[List[int]]) -> Optional[Tuple[int, int]]:
        for i in range(9):
            for j in range(9):
                if grid[i][j] == -1:
                    return (i, j)
        return None

    def is_safe(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        # Check row
        if num in grid[row]: return False
        # Check column
        if num in [grid[i][col] for i in range(9)]: return False
        # Check subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False
        return True

    def reset(self, num_players: int, seed: Optional[int] = None):
        self.state = ta.SinglePlayerState(num_players=num_players, max_turns=self.max_turns, seed=seed,
                                          error_allowance=10)  ## intitialise the game state
        self.full_grid, self.game_board = self._generate_board()
        game_state = {"board": copy.deepcopy(self.game_board),
                      "rendered_board": self._get_grid_string_with_indices(self.game_board), "completed": False}
        self.state.reset(game_state=game_state, player_prompt_function=self._generate_player_prompt)
        self.state.add_observation(message=f"Game Board:\n{self._get_grid_string_with_indices()}",
                                   observation_type=ta.ObservationType.GAME_BOARD)

    def step(self, action: str) -> Tuple[bool, ta.Info]:
        player_id = self.state.current_player_id
        self.state.add_observation(from_id=player_id, to_id=-1, message=action,
                                   observation_type=ta.ObservationType.PLAYER_ACTION)  ## update the observation
        ## validate the actions
        ## extract the format [row column number] from the action
        action_search_pattern = re.compile(r"\[(\d+)\s(\d+)\s(\d+)\]")
        match = action_search_pattern.search(action)

        if not match:
            self.state.set_invalid_move(reward=self._get_percentage_completion(),
                                        reason=f"Invalid move format. Player {player_id} did not respond with valid 'row column number'. Negative reward applied.")
        else:
            row, col, num = map(int, match.groups())
            if row < 1 or row > 9 or col < 1 or col > 9 or num < 0 or num > 9:
                self.state.set_invalid_move(reward=self._get_percentage_completion(),
                                            reason=f"Invalid move. Player {player_id} attempted to place {num} at ({row}, {col}), which is out of bounds. Negative reward applied.")
            else:
                row_idx, col_idx = row - 1, col - 1
                ## check if the cell is already filled in the initial grid
                if self.state.game_state["board"][row_idx][col_idx] != -1:
                    self.state.set_invalid_move(reward=self._get_percentage_completion(),
                                                reason=f"Invalid move. Player {player_id} attempted to overwrite a pre-filled cell ({row}, {col}). Negative reward applied.")
                elif self._is_move_correct(row_idx, col_idx, num):
                    self.state.game_state["board"][row_idx][col_idx] = num  ## update the grid
                    self.state.add_observation(message=f"Board state: \n{self._get_grid_string_with_indices()}",
                                               observation_type=ta.ObservationType.GAME_BOARD)  ## update the observation
                else:
                    self.state.set_invalid_move(reward=self._get_percentage_completion(),
                                                reason=f"Invalid move. Player {player_id} attempted to place {num} at ({row}, {col}), which violates Sudoku rules. Negative reward applied.")

                ## check if the game is completed
                if self._is_puzzle_complete():
                    self.state.game_state["completed"] = True
                    self.state.set_outcome(reward=1,
                                           reason=f"Congratulations! Player {player_id} completed the Sudoku puzzle.")
                self.state.game_state["rendered_board"] = self._get_grid_string_with_indices(
                    self.state.game_state["board"])

        # check turn count
        if self.state.check_turn_limit() and not self.state.done:
            pct_complete = self._get_percentage_completion()
            self.state.set_outcome(reward=pct_complete,
                                   reason=f"The turn limit has been reached. You correctly filled {round(pct_complete * 100)}% of the empty cells.")
        return self.state.step()

    def _is_move_correct(self, row: int, col: int, num: int) -> bool:
        if num == 0:
            return True
        return self.full_grid[row][col] == num

    def _is_puzzle_complete(self) -> bool:
        for i in range(9):
            for j in range(9):
                num = self.state.game_state["board"][i][j]
                if num == -1:
                    return False
                if num == 0:
                    # Ignores 0 for debug env only
                    continue
                if not self._is_move_correct_complete(i, j, num):
                    return False
        return True

    def _is_move_correct_complete(self, row: int, col: int, num: int) -> bool:
        self.state.game_state["board"][row][col] = -1
        correct = self._is_move_correct(row, col, num)
        self.state.game_state["board"][row][col] = num
        return correct

