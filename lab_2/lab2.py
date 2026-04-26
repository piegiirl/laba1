import tkinter as tk
from tkinter import messagebox
from bfs_puzzle import bfs
from dfs_puzzle import dfs
from dfs_modified_puzzle import dfs_modified
from dfs_recursive_puzzle import dfs_recursive
from puzzle_logic import shuffle_board

SIZE = 4


def restore_path(parent, goal):
    # Восстанавливает полный путь от старта до цели по словарю родителей
    path = []
    while goal is not None:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]


def parity_signature(board):
    # Вычисляет сигнатуру чётности (инверсии + строка пустой клетки)
    arr = [x for x in board if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1

    zero_row_from_top = board.index(0) // SIZE
    return (inv + zero_row_from_top) % 2


def is_reachable(start, goal):
    # Проверяет, решаема ли головоломка (правило чётности)
    return parity_signature(start) == parity_signature(goal)


class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Пятнашки")

        # Цветовая схема приложения
        self.bg_main = "#e9ecef"
        self.bg_board = "#dfe6e9"
        self.tile_color = "#ffffff"

        self.root.configure(bg=self.bg_main)

        # Доски
        self.initial_board = list(range(1, 16)) + [0]
        self.goal_board = list(range(1, 16)) + [0]
        self.board = self.initial_board.copy()

        self.goal = tuple(self.goal_board)
        self.path = None          # список состояний — найденное решение
        self.moves = []           # список строк с описанием ходов
        self.current_step = 0

        # Результаты работы алгоритмов
        self.results_dict = {
            "bfs": None,
            "dfs": None,
            "dfs_recursive": None,
            "dfs_modified": None
        }

        self.create_ui()
        self.update_ui()
        self.update_results_view()

    def create_ui(self):
        # Создание основного интерфейса
        main = tk.Frame(self.root, bg=self.bg_main)
        main.pack(padx=10, pady=10)

        boards_frame = tk.Frame(main, bg=self.bg_main)
        boards_frame.pack()

        left_container = tk.Frame(boards_frame, bg=self.bg_main)
        left_container.grid(row=0, column=0, padx=10, sticky="n")

        middle_container = tk.Frame(boards_frame, bg=self.bg_main)
        middle_container.grid(row=0, column=1, padx=10, sticky="n")

        right_container = tk.Frame(boards_frame, bg="#cfd8dc",
                                   highlightbackground="#4EE5D8", highlightthickness=3)
        right_container.grid(row=0, column=2, padx=10, sticky="n")

        self.left_buttons = self.create_labeled_board(left_container, "Начальное состояние")
        self.middle_buttons = self.create_labeled_board(middle_container, "Целевое состояние")
        self.right_buttons = self.create_labeled_board(right_container, "Решение", background="#cfd8dc")

        # Кнопки управления начальным состоянием
        btn_frame = tk.Frame(left_container, bg=self.bg_main)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Ввести", command=self.input_state).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(btn_frame, text="Перемешать", command=self.shuffle).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(btn_frame, text="Цель", command=self.input_goal_state).pack(side="left", expand=True, fill="x", padx=5)

        # Выбор алгоритма поиска
        method_frame = tk.Frame(left_container, bg=self.bg_main)
        method_frame.pack(pady=5)

        tk.Label(method_frame, text="Метод:", bg=self.bg_main).pack(side="left")
        self.method_var = tk.StringVar(value="bfs")

        for text, value in [("BFS", "bfs"), ("DFS", "dfs"),
                            ("DFS Modified", "dfs_modified"), ("DFS Recursive", "dfs_recursive")]:
            tk.Radiobutton(method_frame, text=text, variable=self.method_var,
                           value=value, bg=self.bg_main, command=self.reset_solution)\
                .pack(side="left", padx=5)

        # Поле для максимальной глубины DFS
        depth_frame = tk.Frame(left_container, bg=self.bg_main)
        depth_frame.pack(pady=5, fill="x")
        tk.Label(depth_frame, text="Макс. глубина DFS:", bg=self.bg_main).pack(side="left")
        self.depth_var = tk.IntVar(value=15)
        tk.Entry(depth_frame, textvariable=self.depth_var, width=5, justify="center").pack(side="left", padx=5)

        # Кнопки управления анимацией
        right_ctrl = tk.Frame(right_container, bg="#cfd8dc")
        right_ctrl.pack(pady=10)

        tk.Button(right_ctrl, text="Старт", command=self.start_animation,
                  bg="#4EE5D8", fg="white").pack(side="left", padx=5)
        tk.Button(right_ctrl, text="Предыдущий шаг", command=self.prev_step).pack(side="left", padx=5)
        tk.Button(right_ctrl, text="Следующий шаг", command=self.next_step).pack(side="left", padx=5)

        # Панель ходов и статистики
        moves_panel = tk.Frame(boards_frame, bg=self.bg_main)
        moves_panel.grid(row=0, column=3, padx=15, sticky="n")

        tk.Label(moves_panel, text="Ходы", font=("Arial", 12, "bold"), bg=self.bg_main).pack(pady=(0, 5))
        self.moves_list = tk.Listbox(moves_panel, width=28, height=18)
        self.moves_list.pack()

        tk.Label(moves_panel, text="Результаты", font=("Arial", 12, "bold"), bg=self.bg_main).pack(pady=(10, 0))
        self.results_text = tk.Text(moves_panel, width=28, height=12, font=("Courier New", 10))
        self.results_text.pack()
        self.results_text.config(state="disabled")

        self.status = tk.Label(main, text="Готово", bg=self.bg_main)
        self.status.pack(pady=8)

    def update_results_view(self):
        # Обновляет таблицу результатов всех алгоритмов
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)

        names = {
            "bfs": "BFS",
            "dfs": "DFS (итер.)",
            "dfs_recursive": "DFS (рек.)",
            "dfs_modified": "DFS (мод.)"
        }

        for key in ["bfs", "dfs", "dfs_recursive", "dfs_modified"]:
            res = self.results_dict[key]
            name = names[key]

            if res:
                steps, length = res
                line = f"{name}\n  шаги: {steps:6}   длина: {length:3}\n\n"
            else:
                line = f"{name}\n  —\n\n"

            self.results_text.insert(tk.END, line)

        self.results_text.config(state="disabled")

    def reset_solution(self):
        # Полный сброс текущего решения
        self.path = None
        self.moves = []
        self.current_step = 0
        self.board = self.initial_board.copy()
        self.moves_list.delete(0, tk.END)
        self.update_ui()
        self.status.config(text="Готово")

    def create_labeled_board(self, parent, title, background=None):
        # Создаёт рамку с заголовком и сеткой 4x4
        frame = tk.Frame(parent, background=(background or self.bg_board))
        frame.pack()

        tk.Label(frame, text=title, bg=(background or self.bg_board),
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=5, pady=10)

        cols = ["A", "B", "C", "D"]
        for j, col in enumerate(cols):
            tk.Label(frame, text=col, bg=(background or self.bg_board)).grid(row=1, column=j + 1)

        buttons = []
        for i in range(SIZE):
            tk.Label(frame, text=str(i + 1), bg=(background or self.bg_board)).grid(row=i + 2, column=0)
            row = []
            for j in range(SIZE):
                btn = tk.Label(frame, width=6, height=3, bg=self.tile_color,
                               relief="ridge", bd=2, font=("Arial", 14, "bold"))
                btn.grid(row=i + 2, column=j + 1, padx=3, pady=3)
                row.append(btn)
            buttons.append(row)
        return buttons

    def draw_board(self, buttons, board_values):
        # Отрисовывает числа на плитках
        for i in range(SIZE):
            for j in range(SIZE):
                val = board_values[i * SIZE + j]
                buttons[i][j]["text"] = str(val) if val != 0 else ""

    def update_ui(self):
        # Обновляет все три доски на экране
        self.draw_board(self.left_buttons, self.initial_board)
        self.draw_board(self.middle_buttons, self.goal_board)
        self.draw_board(self.right_buttons, self.board)

    # ======================== ЛОГИКА ========================

    def open_board_dialog(self, title, initial_values):
        # Открывает окно для ручного ввода состояния 4x4
        win = tk.Toplevel(self.root)
        win.title(title)
        win.transient(self.root)
        win.grab_set()

        entries = []
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                e = tk.Entry(win, width=3, font=("Arial", 14), justify="center")
                e.grid(row=i, column=j, padx=5, pady=5)
                e.insert(0, str(initial_values[i * SIZE + j]))
                row.append(e)
            entries.append(row)

        result = {"board": None}

        def submit():
            try:
                nums = [int(entries[i][j].get()) for i in range(SIZE) for j in range(SIZE)]
                if len(nums) != 16 or set(nums) != set(range(16)):
                    raise ValueError
                result["board"] = nums
                win.destroy()
            except Exception:
                messagebox.showerror("Ошибка", "Неверный ввод")

        tk.Button(win, text="ОК", command=submit).grid(row=SIZE, column=0, columnspan=SIZE, pady=10)

        self.root.wait_window(win)
        return result["board"]

    def input_state(self):
        # Ввод начального состояния пользователем
        nums = self.open_board_dialog("Ввод начального состояния", self.initial_board)
        if nums is None:
            return
        self.initial_board = nums[:]
        self.board = nums[:]
        self.reset_solution()
        self.update_ui()

    def input_goal_state(self):
        # Ввод целевого состояния
        nums = self.open_board_dialog("Ввод целевого состояния", self.goal_board)
        if nums is None:
            return
        self.goal_board = nums[:]
        self.goal = tuple(self.goal_board)
        self.reset_solution()
        self.update_ui()

    def shuffle(self):
        # Перемешивание начальной доски
        self.initial_board = shuffle_board()
        self.board = self.initial_board.copy()

        self.reset_solution()
        self.results_dict = {key: None for key in self.results_dict}
        self.update_results_view()

    def compute_solution(self):
        # Основной метод решения: проверка + запуск выбранного алгоритма
        if not is_reachable(self.initial_board, self.goal_board):
            self.status.config(text="Состояние не достижимо")
            messagebox.showerror("Ошибка", "Начальное состояние нельзя преобразовать в выбранное целевое")
            self.reset_solution()
            return

        start = tuple(self.initial_board)
        self.goal = tuple(self.goal_board)

        try:
            max_depth = int(self.depth_var.get())
            if max_depth < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Максимальная глубина должна быть неотрицательным числом")
            return

        method = self.method_var.get()

        # Запуск выбранного алгоритма
        if method == "bfs":
            path, steps = bfs(start, self.goal)

        elif method == "dfs":
            path, steps = dfs(start, self.goal, max_depth)

        elif method == "dfs_modified":
            steps_box = [0]
            result = dfs_modified(start, self.goal, set(), [], steps_box, 0, max_depth)
            path, steps = result if result else (None, steps_box[0])

        elif method == "dfs_recursive":
            steps_rec = [0]
            parent = {start: None}
            found = dfs_recursive(start, self.goal, set(), parent, steps_rec, 0, max_depth)
            path = restore_path(parent, self.goal) if found else None
            steps = steps_rec[0]

        else:
            path, steps = None, 0

        # Обработка результата
        if path is None:
            self.path = None
            self.moves = []
            self.current_step = 0
            self.board = self.initial_board.copy()
            self.update_ui()

            if method == "bfs":
                self.status.config(text=f"Нет решения | Шагов: {steps}")
            else:
                self.status.config(text=f"Нет решения в пределах глубины {max_depth} | Шагов: {steps}")

            self.results_dict[method] = (steps, 0)
            self.update_results_view()
            return

        # Решение найдено
        self.status.config(
            text=f"Шагов поиска: {steps} | Длина решения: {len(path) - 1}"
        )

        self.results_dict[method] = (steps, len(path) - 1)
        self.update_results_view()

        self.path = path
        self.moves = [self.get_move(path[k], path[k + 1]) for k in range(len(path) - 1)]

        self.moves_list.delete(0, tk.END)
        for move in self.moves:
            self.moves_list.insert(tk.END, move)

        self.current_step = 0
        self.board = list(path[0])
        self.update_ui()

    def start_animation(self):
        # Запуск автоматической анимации решения
        if self.path is None:
            self.compute_solution()
            if self.path is None:
                return

        def step(i):
            if i >= len(self.path):
                return
            self.current_step = i
            self.board = list(self.path[i])
            self.update_ui()

            self.moves_list.selection_clear(0, tk.END)
            if i > 0:
                self.moves_list.selection_set(i - 1)
                self.moves_list.see(i - 1)

            self.root.after(350, lambda: step(i + 1))

        step(0)

    def next_step(self):
        # Переход к следующему шагу вручную
        if self.path and self.current_step < len(self.path) - 1:
            self.current_step += 1
            self.board = list(self.path[self.current_step])
            self.update_ui()

            self.moves_list.selection_clear(0, tk.END)
            self.moves_list.selection_set(self.current_step - 1)
            self.moves_list.see(self.current_step - 1)

    def prev_step(self):
        # Переход к предыдущему шагу вручную
        if self.path and self.current_step > 0:
            self.current_step -= 1
            self.board = list(self.path[self.current_step])
            self.update_ui()

            self.moves_list.selection_clear(0, tk.END)
            if self.current_step > 0:
                self.moves_list.selection_set(self.current_step - 1)
                self.moves_list.see(self.current_step - 1)

    def get_move(self, s1, s2):
        # Возвращает текстовое описание одного хода 
        i1 = s1.index(0)
        i2 = s2.index(0)
        x1, y1 = divmod(i1, SIZE)
        x2, y2 = divmod(i2, SIZE)
        cols = ["A", "B", "C", "D"]
        return f"{cols[y1]}{x1 + 1} → {cols[y2]}{x2 + 1}"


# ======================== ЗАПУСК ========================
root = tk.Tk()
app = PuzzleGUI(root)
root.mainloop()