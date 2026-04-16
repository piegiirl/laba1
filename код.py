import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import time

class EightPuzzleSearch:
    """Класс, который содержит все алгоритмы поиска для игры в 8"""
    def __init__(self):
        self.goal = None                     # целевое состояние

    def set_goal(self, goal_state):
        """Устанавливаем целевое состояние (фиксированное)"""
        self.goal = self.tuple_state(goal_state)

    @staticmethod
    def tuple_state(state):
        """Превращаем матрицу 3x3 в кортеж (чтобы можно было хранить в set)"""
        return tuple(tuple(row) for row in state)

    @staticmethod
    def find_blank(state):
        """Находим координаты пустой клетки (0) — нужно для генерации ходов"""
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return None

    def get_successors(self, state):
        """Генерируем все возможные следующие состояния (до 4 ходов)"""
        state_list = [list(row) for row in state]
        i, j = self.find_blank(state_list)
        successors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # вверх, вниз, влево, вправо
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_state = [row[:] for row in state_list]
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                successors.append(self.tuple_state(new_state))
        return successors

    @staticmethod
    def reconstruct_path(parent, goal):
        """Восстанавливаем полный путь от начального состояния до цели"""
        path = []
        while goal is not None:
            path.append(goal)
            goal = parent.get(goal)
        return path[::-1]                    # разворачиваем путь

    def breadth_search(self, start, goal):
        """Поиск в ширину (BFS) — находит кратчайшее решение"""
        open_list = deque([start])
        visited = set()
        parent = {start: None}
        steps = 0
        while open_list:
            current = open_list.popleft()
            visited.add(current)
            steps += 1
            for neighbor in self.get_successors(current):
                if current == goal:
                    return True, self.reconstruct_path(parent, current), steps
                if neighbor not in visited and neighbor not in open_list:
                    parent[neighbor] = current
                    open_list.append(neighbor)
        return False, None, steps

    def depth_search_iter(self, start, goal, max_depth=30):
        """Поиск в глубину (итерационный) с ограничением глубины"""
        stack = [(start, 0)]                 # стек + текущая глубина
        visited = set()
        parent = {start: None}
        steps = 0
        while stack:
            current, depth = stack.pop()
            steps += 1
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                return True, self.reconstruct_path(parent, current), steps
            if depth >= max_depth:           # защита от слишком глубокого поиска
                continue
            for neighbor in reversed(self.get_successors(current)):
                if neighbor not in visited:
                    parent[neighbor] = current
                    stack.append((neighbor, depth + 1))
        return False, None, steps

class PuzzleApp(tk.Tk):
    """Главный класс окна программы"""

    def __init__(self):
        super().__init__()
        self.title("Игра в 8 — Лабораторная работа 2")
        self.geometry("1150x680")
        self.resizable(True, True)
        self.style = ttk.Style()
        self.style.map("TEntry",
                       foreground=[("disabled", "black")],
                       fieldbackground=[("disabled", "white")]
                       )
        self.search = EightPuzzleSearch()
        self.default_initial = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
        self.default_goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
        self.current_initial = [row[:] for row in self.default_initial]
        self.current_goal = [row[:] for row in self.default_goal]
        self.search.set_goal(self.current_goal)
        self.solution_path = None
        self.current_step = 0
        self.create_widgets()

    def create_widgets(self):
        """Создаём весь интерфейс программы"""
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Левая колонка — настройка
        input_f = ttk.LabelFrame(main_frame, text="Настройка задачи", padding=10)
        input_f.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        ttk.Label(input_f, text="Начальное состояние:").pack(anchor="w", pady=(0, 5))
        self.initial_entries_grid = self.create_puzzle_grid(input_f, self.current_initial, editable=True)

        ttk.Label(input_f, text="Целевое состояние:").pack(anchor="w", pady=(15, 5))
        self.goal_entries_grid = self.create_puzzle_grid(input_f, self.current_goal, editable=False)

        ttk.Button(input_f, text="Применить настройки", command=self.apply_settings).pack(pady=8, fill=tk.X)

        # Средняя колонка — поиск
        ctrl_f = ttk.LabelFrame(main_frame, text="Поиск решения", padding=12)
        ctrl_f.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        ttk.Button(ctrl_f, text="Поиск в ширину", command=self.run_bfs).pack(pady=8, fill=tk.X)

        dfs_f = ttk.Frame(ctrl_f)
        dfs_f.pack(pady=15, fill=tk.X)
        ttk.Label(dfs_f, text="Поиск в глубину:").pack(anchor="w")
        ttk.Label(dfs_f, text="Макс. глубина:").pack(anchor="w")
        self.max_depth_var = tk.IntVar(value=30)
        ttk.Entry(dfs_f, textvariable=self.max_depth_var, width=10).pack(pady=5)
        ttk.Button(dfs_f, text="Запустить поиск в глубину", command=self.run_dfs).pack(fill=tk.X)

        self.result_label = ttk.Label(ctrl_f, text="Результат: —", font=("Arial", 12))
        self.result_label.pack(pady=20)

        # Правая колонка — визуализация решения
        sol_f = ttk.LabelFrame(main_frame, text="Решение (нажмите «Следующий»)", padding=10)
        sol_f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.board_canvas = tk.Canvas(sol_f, width=350, height=350, bg="#f8f9fa", highlightthickness=0)
        self.board_canvas.pack()

        nav = ttk.Frame(sol_f)
        nav.pack(fill=tk.X, pady=8)
        ttk.Button(nav, text="◀ Предыдущий", command=self.prev_step).pack(side=tk.LEFT)
        self.step_label = ttk.Label(nav, text="Шаг 0 / 0", font=("Arial", 11))
        self.step_label.pack(side=tk.LEFT, padx=30)
        ttk.Button(nav, text="Следующий ▶", command=self.next_step).pack(side=tk.LEFT)

        ttk.Button(sol_f, text="Очистить решение", command=self.clear_solution).pack(pady=5)

        # Нижняя строка статуса
        self.status = ttk.Label(self, text="Готово к работе", relief=tk.SUNKEN, anchor="w", padding=(5, 1))
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def create_puzzle_grid(self, parent, values, editable=True):
        """Создаёт поле 3x3. editable=False — поле нельзя редактировать"""
        frame = ttk.Frame(parent)
        frame.pack(pady=5)
        entries = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                e = ttk.Entry(frame, width=5, justify="center", font=("Arial", 24, "bold"))
                e.grid(row=i, column=j, padx=3, pady=3)
                e.insert(0, str(values[i][j]))
                if not editable:
                    e.config(state="disabled")
                entries[i][j] = e
        return entries

    def show_status(self, text):
        """Выводит сообщение в нижнюю строку"""
        self.status.config(text=text)
        self.update_idletasks()

    def apply_settings(self):
        init = self.get_state_from_grid(self.initial_entries_grid)
        if init is None:
            return False
        self.current_initial = init
        self.search.set_goal(self.current_goal)
        self.show_status("Начальное состояние обновлено")
        return True

    def get_state_from_grid(self, grid):
        """Читаем состояние из полей ввода"""
        state = []
        for row in grid:
            r = []
            for e in row:
                val = e.get().strip()
                if not val.isdigit() or int(val) > 8:
                    messagebox.showerror("Ошибка", "Значения должны быть от 0 до 8!")
                    return None
                r.append(int(val))
            state.append(r)
        return state

    def draw_board(self, state):
        """Рисует текущее состояние игры на холсте"""
        self.board_canvas.delete("all")
        offset = 8
        cell = 110
        for i in range(3):
            for j in range(3):
                x1 = offset + j * cell
                y1 = offset + i * cell
                self.board_canvas.create_rectangle(x1, y1, x1 + cell, y1 + cell,
                                                   fill="#ecf0f1", outline="#2c3e50", width=5)
                val = state[i][j]
                if val != 0:
                    self.board_canvas.create_text(x1 + cell / 2, y1 + cell / 2,
                                                  text=str(val), font=("Arial", 48, "bold"), fill="#2c3e50")

    def run_bfs(self):
        """Запуск поиска в ширину"""
        if not self.apply_settings():
            return
        self.show_status("Идет поиск...")
        self.update()
        start = self.search.tuple_state(self.current_initial)
        start_t = time.time()
        found, path, steps = self.search.breadth_search(start, self.search.goal)
        elapsed = time.time() - start_t
        if found:
            self.solution_path = path
            self.current_step = 0
            self.update_solution_display()
            self.result_label.config(text=f"Поиск в ширину: Решение найдено!\nШагов: {steps}\nВремя: {elapsed:.3f} сек")
        else:
            self.result_label.config(text="Поиск в ширину: Решение НЕ найдено")

    def run_dfs(self):
        """Запуск поиска в глубину"""
        if not self.apply_settings():
            return
        self.show_status("Идет поиск...")
        self.update()
        start = self.search.tuple_state(self.current_initial)
        max_d = self.max_depth_var.get()
        start_t = time.time()
        found, path, steps = self.search.depth_search_iter(start, self.search.goal, max_d)
        elapsed = time.time() - start_t
        if found:
            self.solution_path = path
            self.current_step = 0
            self.update_solution_display()
            self.result_label.config(
                text=f"Поиск в глубину: Решение найдено!\nШагов: {steps}\nГлубина: {max_d}\nВремя: {elapsed:.3f} сек")
        else:
            self.result_label.config(text=f"Поиск в глубину: Решение НЕ найдено\n(увеличьте макс. глубину)")

    def update_solution_display(self):
        """Обновляет картинку решения при перелистывании шагов"""
        if not self.solution_path:
            return
        state = self.solution_path[self.current_step]
        self.draw_board(state)
        self.step_label.config(text=f"Шаг {self.current_step} / {len(self.solution_path) - 1}")

    def prev_step(self):
        if self.solution_path and self.current_step > 0:
            self.current_step -= 1
            self.update_solution_display()

    def next_step(self):
        if self.solution_path and self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.update_solution_display()

    def clear_solution(self):
        """Очищает текущее решение"""
        self.solution_path = None
        self.current_step = 0
        self.board_canvas.delete("all")
        self.step_label.config(text="Шаг 0 / 0")
        self.result_label.config(text="Результат: —")

if __name__ == "__main__":
    app = PuzzleApp()
    app.mainloop()