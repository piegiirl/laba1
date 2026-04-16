import tkinter as tk
from tkinter import messagebox
import random
from bfs_puzzle import bfs
from dfs_puzzle import dfs
from puzzle_logic import get_neighbors, is_solvable

SIZE = 4

def shuffle_board(steps=10):
    board = list(range(1, 16)) + [0]
    prev = None

    for _ in range(steps):
        neighbors = get_neighbors(tuple(board))

        # убираем состояние, из которого пришли (анти-откат)
        if prev and prev in neighbors:
            neighbors.remove(prev)

        next_state = random.choice(neighbors)
        prev = tuple(board)
        board = list(next_state)

    return board

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Пятнашки")

        self.bg_main = "#e9ecef"
        self.bg_board = "#dfe6e9"
        self.tile_color = "#ffffff"

        self.root.configure(bg=self.bg_main)

        self.board = list(range(1, 16)) + [0]
        self.initial_board = self.board.copy()
        self.goal = tuple(self.board)
        self.path = None
        self.current_step = 0

        self.create_ui()
        self.update_ui()

    def create_ui(self):
        main = tk.Frame(self.root, bg=self.bg_main)
        main.pack(padx=10, pady=10)

        boards_frame = tk.Frame(main, bg=self.bg_main)
        boards_frame.pack()

        left_container = tk.Frame(boards_frame, bg=self.bg_main)
        left_container.grid(row=0, column=0, padx=10, sticky="n")

        right_container = tk.Frame(boards_frame, bg=self.bg_main)
        right_container.grid(row=0, column=1, padx=10, sticky="n")

        self.left_buttons = self.create_labeled_board(left_container, "Начальное состояние")
        self.right_buttons = self.create_labeled_board(right_container, "Решение")

        # === КНОПКИ СЛЕВА ===
        btn_frame = tk.Frame(left_container, bg=self.bg_main)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Ввести", command=self.input_state)\
            .pack(side="left", expand=True, fill="x", padx=5)

        tk.Button(btn_frame, text="Перемешать", command=self.shuffle)\
            .pack(side="left", expand=True, fill="x", padx=5)

        # === МЕТОД ===
        method_frame = tk.Frame(left_container, bg=self.bg_main)
        method_frame.pack(pady=5)

        tk.Label(method_frame, text="Метод:", bg=self.bg_main).pack(side="left")

        self.method_var = tk.StringVar(value="bfs")

        tk.Radiobutton(method_frame, text="BFS", variable=self.method_var,
                    value="bfs", bg=self.bg_main,
                    command=self.reset_solution).pack(side="left", padx=5)

        tk.Radiobutton(method_frame, text="DFS", variable=self.method_var,
                    value="dfs", bg=self.bg_main,
                    command=self.reset_solution).pack(side="left")

        # === КНОПКИ СПРАВА ===
        right_ctrl = tk.Frame(right_container, bg=self.bg_main)
        right_ctrl.pack(pady=10)

        tk.Button(right_ctrl, text="Старт", command=self.start_animation,
                  bg="#4CAF50", fg="white").pack(side="left", padx=5)

        tk.Button(right_ctrl, text="Предыдущий шаг", command=self.prev_step)\
            .pack(side="left", padx=5)

        tk.Button(right_ctrl, text="Следующий шаг", command=self.next_step)\
            .pack(side="left", padx=5)

        # === СПИСОК ХОДОВ ===
        moves_panel = tk.Frame(boards_frame, bg=self.bg_main)
        moves_panel.grid(row=0, column=2, padx=15, sticky="n")

        tk.Label(moves_panel, text="Ходы", font=("Arial", 12, "bold"),
                 bg=self.bg_main).pack(pady=(0, 5))

        self.moves_list = tk.Listbox(moves_panel, width=28, height=18)
        self.moves_list.pack()

        self.status = tk.Label(main, text="Готово", bg=self.bg_main)
        self.status.pack(pady=8)
    def reset_solution(self):
        self.path = None
        self.moves_list.delete(0, tk.END)
        self.status.config(text="Готово")
    def create_labeled_board(self, parent, title):
        frame = tk.Frame(parent, bg=self.bg_board)
        frame.pack()

        tk.Label(frame, text=title, bg=self.bg_board,
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=5, pady=10)

        tk.Label(frame, text="", bg=self.bg_board).grid(row=1, column=0)

        cols = ["A", "B", "C", "D"]
        for j, col in enumerate(cols):
            tk.Label(frame, text=col, bg=self.bg_board).grid(row=1, column=j + 1)

        buttons = []
        for i in range(SIZE):
            tk.Label(frame, text=str(i + 1), bg=self.bg_board).grid(row=i + 2, column=0)

            row = []
            for j in range(SIZE):
                btn = tk.Label(frame, width=6, height=3,
                               bg=self.tile_color, relief="ridge", bd=2,
                               font=("Arial", 14, "bold"))
                btn.grid(row=i + 2, column=j + 1, padx=3, pady=3)
                row.append(btn)
            buttons.append(row)
        return buttons

    def update_ui(self):
        for i in range(SIZE):
            for j in range(SIZE):
                val = self.initial_board[i * SIZE + j]
                self.left_buttons[i][j]["text"] = str(val) if val != 0 else ""

        for i in range(SIZE):
            for j in range(SIZE):
                val = self.board[i * SIZE + j]
                self.right_buttons[i][j]["text"] = str(val) if val != 0 else ""

    # ===== ВВОД МАТРИЦЕЙ =====
    def input_state(self):
        win = tk.Toplevel(self.root)
        win.title("Ввод состояния")

        entries = []

        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                e = tk.Entry(win, width=3, font=("Arial", 14), justify="center")
                e.grid(row=i, column=j, padx=5, pady=5)
                row.append(e)
            entries.append(row)

        def submit():
            try:
                nums = []
                for i in range(SIZE):
                    for j in range(SIZE):
                        val = int(entries[i][j].get())
                        nums.append(val)

                if len(nums) != 16 or set(nums) != set(range(16)):
                    raise ValueError

                if not is_solvable(nums):
                    messagebox.showerror("Ошибка", "Нерешаемое состояние")
                    return

                self.initial_board = nums[:]
                self.board = nums[:]

                self.moves_list.delete(0, tk.END)
                self.path = None
                self.update_ui()
                win.destroy()

            except:
                messagebox.showerror("Ошибка", "Неверный ввод")

        tk.Button(win, text="ОК", command=submit)\
            .grid(row=SIZE, column=0, columnspan=SIZE, pady=10)

    def shuffle(self):
        self.initial_board = shuffle_board()
        self.board = self.initial_board.copy()

        self.moves_list.delete(0, tk.END)
        self.path = None
        self.update_ui()

        if not is_solvable(self.board):
            messagebox.showerror("Ошибка", "Нерешаемое состояние")
        return

    def compute_solution(self):
        start = tuple(self.initial_board)

        if self.method_var.get() == "bfs":
            path, steps = bfs(start, self.goal)
        else:
            path, steps = dfs(start, self.goal, 30)

        if path is None:
            self.status.config(text="Нет решения")
            return

        # ✅ ВЫВОД ШАГОВ
        self.status.config(
            text=f"Шагов поиска: {steps} | Длина решения: {len(path) - 1}"
        )

        self.path = path
        self.moves = [self.get_move(path[k], path[k + 1]) for k in range(len(path) - 1)]

        self.moves_list.delete(0, tk.END)
        for move in self.moves:
            self.moves_list.insert(tk.END, move)

        self.moves_list.selection_clear(0, tk.END)

        self.current_step = 0
        self.board = list(path[0])
        self.update_ui()
    def start_animation(self):
        if self.path is None:
            self.compute_solution()
            if self.path is None:
                messagebox.showwarning("Внимание", "Решение не найдено")
                return

        def step(i):
            if i >= len(self.path):
                return

            self.board = list(self.path[i])
            self.update_ui()

            if i > 0:
                self.moves_list.selection_clear(0, tk.END)
                self.moves_list.selection_set(i - 1)
                self.moves_list.see(i - 1)

            self.root.after(250, lambda: step(i + 1))

        step(0)

    def next_step(self):
        if self.path and self.current_step < len(self.path) - 1:
            self.current_step += 1
            self.board = list(self.path[self.current_step])
            self.update_ui()

            self.moves_list.selection_clear(0, tk.END)
            self.moves_list.selection_set(self.current_step - 1)
            self.moves_list.see(self.current_step - 1)

    def prev_step(self):
        if self.path and self.current_step > 0:
            self.current_step -= 1
            self.board = list(self.path[self.current_step])
            self.update_ui()

            self.moves_list.selection_clear(0, tk.END)
            if self.current_step > 0:
                self.moves_list.selection_set(self.current_step - 1)
                self.moves_list.see(self.current_step - 1)

    def get_move(self, s1, s2):
        i1 = s1.index(0)
        i2 = s2.index(0)
        x1, y1 = divmod(i1, SIZE)
        x2, y2 = divmod(i2, SIZE)
        cols = ["A", "B", "C", "D"]
        return f"{cols[y1]}{x1 + 1} → {cols[y2]}{x2 + 1}"


root = tk.Tk()
app = PuzzleGUI(root)
root.mainloop()