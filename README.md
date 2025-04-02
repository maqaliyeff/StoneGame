# Stone Age Game

A strategic turn-based game implemented in Python with Tkinter.

![image](https://github.com/user-attachments/assets/690f2e3e-b0cc-4db3-9a64-a9d552586c4a)

## Game Overview

Stone Age is a strategic game where players take turns removing stones from a pile. The unique scoring mechanism adds depth to the seemingly simple gameplay:

- Players can remove either 2 or 3 stones on their turn
- If the remaining number of stones is even, the player gets +2 points
- If the remaining number is odd, the player loses 2 points
- The game continues until no stones remain
- The player with the highest score wins

## Features

- **Single-player Mode**: Play against the computer
- **AI Algorithms**: Choose between Minimax or Alpha-Beta Pruning
- **Customizable Settings**: Adjust the starting number of stones
- **Turn Selection**: Choose who starts first (player or computer)
- **Visual Interface**: Clean, intuitive Tkinter GUI

## Installation

### Prerequisites
- Python 3.x
- Pillow (PIL Fork)

### Setup
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/stone-age-game.git
   ```

2. Install required packages:
   ```
   pip install pillow
   ```

3. Navigate to the project directory:
   ```
   cd stone-age-game
   ```

4. Make sure you have an image named "image.jpg" in the same directory to use as background

5. Run the game:
   ```
   python game.py
   ```

## Game Logic

The game uses a tree-based approach to model possible game states:

- `GameState` class represents a specific state of the game (stones left, scores, turn)
- `GameTree` class builds a tree of possible moves to a specified depth
- The computer player uses this tree to determine optimal moves

The implementation includes:
- Game state evaluation
- Scoring mechanism
- Turn management
- Win condition checking

## User Interface

The game features a multi-screen interface:
1. Start screen with game title and play/exit options
2. Player selection screen (who starts first)
3. Algorithm selection screen with stone count adjustment
4. Main game screen showing:
   - Current stone count
   - Player scores
   - Turn indicator
   - Take 2/Take 3 buttons
   - Game result when finished

## Game Tree Implementation

```python
class GameTree:
    def __init__(self, root_state):
        self.root = root_state

    def build_tree(self, node, depth):
        if node.is_terminal() or depth == 0:
            return
        for move in [2, 3]:
            if node.stones >= move:
                new_stones = node.stones - move
                if new_stones % 2 == 0:
                    new_pscore = node.player_score + (2 if node.turn == "player" else 0)
                    new_cscore = node.computer_score + (2 if node.turn == "computer" else 0)
                else:
                    new_pscore = node.player_score - (2 if node.turn == "player" else 0)
                    new_cscore = node.computer_score - (2 if node.turn == "computer" else 0)
                next_turn = "computer" if node.turn == "player" else "player"
                child = GameState(new_stones, new_pscore, new_cscore, next_turn)
                node.children.append(child)
                self.build_tree(child, depth - 1)
```

## Screenshots

![Start Screen](
![image](https://github.com/user-attachments/assets/690f2e3e-b0cc-4db3-9a64-a9d552586c4a)

![Game Screen](
![image](https://github.com/user-attachments/assets/5362ce24-f7ba-4313-bd27-62b43a8b29cf)

## Acknowledgments

- Inspired by classic turn-based strategy games
- Built as a demonstration of game tree algorithms in Python
