import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class GameState:
    def __init__(self, stones, player_score=0, com_score=0, current_player="player"):
        self.stones = stones
        self.player_score = player_score
        self.com_score = com_score
        self.current_player = current_player
        self._possible_next_states = None

    def game_over(self):
        return self.stones == 0

    def get_possible_moves(self):
        if self._possible_next_states is not None:
            return self._possible_next_states
        self._possible_next_states = []
        for move_amount in (2, 3):
            if self.stones >= move_amount:
                new_stone_count = self.stones - move_amount
                new_player_score = self.player_score
                new_com_score = self.com_score
                if new_stone_count % 2 == 0:
                    if self.current_player == "player":
                        new_player_score += 2
                    else:
                        new_com_score += 2
                else:
                    if self.current_player == "player":
                        new_player_score -= 2
                    else:
                        new_com_score -= 2
                next_player = "com" if self.current_player == "player" else "player"
                next_state = GameState(new_stone_count, new_player_score, new_com_score, next_player)
                self._possible_next_states.append(next_state)
        return self._possible_next_states

class StoneGameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stone Game")
        self.geometry("600x500")
        self.resizable(False, False)
        self.bg_image = ImageTk.PhotoImage(Image.open("image.jpg").resize((600, 500)))
        self.stones = 0
        self.current_state = None
        self.algorithm = "minimax"
        self.starting_player = "human"
        self.search_depth = 6
        self.nodes_visited = 0
        self.frames = {}
        for Screen in (StartScreen, SelectAlgorithmScreen, GameScreen):
            screen_instance = Screen(self)
            self.frames[Screen] = screen_instance
            screen_instance.place(relwidth=1, relheight=1)
        self.show_frame(StartScreen)

    def show_frame(self, screen_class):
        frame_to_show = self.frames[screen_class]
        frame_to_show.tkraise()

    def start_game(self, stones, starter, algorithm):
        self.stones = stones
        self.starting_player = starter
        self.algorithm = algorithm
        self.current_state = GameState(stones)
        game_screen = self.frames[GameScreen]
        game_screen.reset_controls()
        game_screen.update_display()
        self.show_frame(GameScreen)
        if self.starting_player == "computer":
            self.after(500, self.computer_move)

    def make_move(self, stones_taken):
        if self.current_state.stones < stones_taken:
            if all(self.current_state.stones < m for m in (2, 3)):
                self.frames[GameScreen].show_result()
            else:
                messagebox.showinfo("Invalid Move", f"You can't take {stones_taken} stones right now.")
            return
        for next_state in self.current_state.get_possible_moves():
            if self.current_state.stones - next_state.stones == stones_taken:
                self.current_state = next_state
                break
        self.frames[GameScreen].update_display()
        if self.current_state.game_over():
            self.frames[GameScreen].show_result()
        else:
            self.after(500, self.computer_move)

    def computer_move(self):
        self.nodes_visited = 0
        if self.algorithm == "minimax":
            _, best_option = self.minimax(self.current_state, True, self.search_depth)
        else:
            _, best_option = self.alpha_beta_search(self.current_state, True, float('-inf'), float('inf'), self.search_depth)
        self.current_state = best_option
        self.frames[GameScreen].update_display()
        if self.current_state.game_over():
            self.frames[GameScreen].show_result()

    def evaluate(self, state):
        return (
            2 * (state.com_score - state.player_score)
            + (1 if state.stones % 2 == 0 else -1)
            + (1 if state.current_player == "com" else -1)
        )

    def minimax(self, state, maximizing, depth):
        self.nodes_visited += 1
        if depth == 0 or state.game_over():
            return self.evaluate(state), state
        best_state = None
        if maximizing:
            best_score = float('-inf')
            for child in state.get_possible_moves():
                score, _ = self.minimax(child, False, depth - 1)
                if score > best_score:
                    best_score = score
                    best_state = child
            return best_score, best_state
        else:
            best_score = float('inf')
            for child in state.get_possible_moves():
                score, _ = self.minimax(child, True, depth - 1)
                if score < best_score:
                    best_score = score
                    best_state = child
            return best_score, best_state

    def alpha_beta_search(self, state, maximizing, alpha, beta, depth):
        self.nodes_visited += 1
        if depth == 0 or state.game_over():
            return self.evaluate(state), state
        best_state = None
        if maximizing:
            best_eval = float('-inf')
            for child in state.get_possible_moves():
                eval_child, _ = self.alpha_beta_search(child, False, alpha, beta, depth - 1)
                if eval_child > best_eval:
                    best_eval = eval_child
                    best_state = child
                alpha = max(alpha, eval_child)
                if beta <= alpha:
                    break
            return best_eval, best_state
        else:
            best_eval = float('inf')
            for child in state.get_possible_moves():
                eval_child, _ = self.alpha_beta_search(child, True, alpha, beta, depth - 1)
                if eval_child < best_eval:
                    best_eval = eval_child
                    best_state = child
                beta = min(beta, eval_child)
                if beta <= alpha:
                    break
            return best_eval, best_state

class StartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, image=master.bg_image).place(relwidth=1, relheight=1)
        container = tk.Frame(self, bg="lightblue")
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="Stone Game", font=("Arial", 24), bg="lightblue").pack(pady=10)
        tk.Label(container, text="Enter the number of stones to start (50–70):", bg="lightblue").pack()
        self.stone_entry = tk.Entry(container)
        self.stone_entry.pack(pady=5)
        tk.Label(container, text="Who goes first?", bg="lightblue").pack()
        self.starting_player_var = tk.StringVar(value="human")
        tk.Radiobutton(container, text="Human", variable=self.starting_player_var, value="human", bg="lightblue").pack()
        tk.Radiobutton(container, text="Computer", variable=self.starting_player_var, value="computer", bg="lightblue").pack()
        tk.Button(container, text="Next", command=self.go_to_select_algo).pack(pady=10)

    def go_to_select_algo(self):
        try:
            chosen_stones = int(self.stone_entry.get())
            if not (50 <= chosen_stones <= 70):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer between 50 and 70.")
            return
        next_screen = self.master.frames[SelectAlgorithmScreen]
        next_screen.stones = chosen_stones
        next_screen.starter = self.starting_player_var.get()
        self.master.show_frame(SelectAlgorithmScreen)

class SelectAlgorithmScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, image=master.bg_image).place(relwidth=1, relheight=1)
        container = tk.Frame(self, bg="lightblue")
        container.place(relx=0.5, rely=0.5, anchor="center")
        self.stones = 50
        self.starter = "human"
        tk.Label(container, text="Select an Algorithm", font=("Arial", 20), bg="lightblue").pack(pady=10)
        self.algorithm_choice = tk.StringVar(value="minimax")
        tk.Radiobutton(container, text="Minimax", variable=self.algorithm_choice, value="minimax", bg="lightblue").pack()
        tk.Radiobutton(container, text="Alpha-Beta Pruning", variable=self.algorithm_choice, value="alphabeta", bg="lightblue").pack()
        tk.Button(container, text="Start Game", command=self.launch_game).pack(pady=10)

    def launch_game(self):
        self.master.start_game(self.stones, self.starter, self.algorithm_choice.get())

class GameScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, image=master.bg_image).place(relwidth=1, relheight=1)
        self.info_label = tk.Label(self, font=("Courier", 16), bg="lightblue", justify="left")
        self.info_label.pack(pady=20)
        self.result_label = tk.Label(self, font=("Arial", 20), fg="darkgreen", bg="lightblue")
        self.result_label.pack(pady=10)
        self.btn_take2 = tk.Button(self, text="Take 2 Stones", command=lambda: master.make_move(2))
        self.btn_take3 = tk.Button(self, text="Take 3 Stones", command=lambda: master.make_move(3))
        self.btn_take2.pack(pady=5)
        self.btn_take3.pack(pady=5)

    def update_display(self):
        state = self.master.current_state
        display_text = (
            f"Stones Left: {state.stones}\n"
            f"Human Score: {state.player_score}\n"
            f"Computer Score: {state.com_score}\n"
            f"Current Turn: {state.current_player.upper()}"
        )
        self.info_label.config(text=display_text)
        self.result_label.config(text="")

    def show_result(self):
        state = self.master.current_state
        human_final_score = state.player_score + (state.stones if state.current_player == "player" else 0)
        com_final_score = state.com_score + (state.stones if state.current_player == "com" else 0)
        if human_final_score > com_final_score:
            final_text = "You Win! Hooray!"
        elif com_final_score > human_final_score:
            final_text = "Computer Wins! Better luck next time."
        else:
            final_text = "It's a Draw! So close..."
        self.result_label.config(text=final_text)
        self.btn_take2.config(state="disabled")
        self.btn_take3.config(state="disabled")

    def reset_controls(self):
        self.btn_take2.config(state="normal")
        self.btn_take3.config(state="normal")
        self.result_label.config(text="")

if __name__ == "__main__":
    app = StoneGameApp()
    app.mainloop()