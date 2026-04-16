import tkinter as tk
from tkinter import messagebox
from collections import deque
from bfs import bfs
from dfs_iterative import dfs_iterative
from dfs_modified import dfs_modified
from dfs_recursive import dfs_recursive

def restore_path(parent, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]

# ===================== ОКНО 1 =====================
class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск на графе")
        self.root.geometry("350x200")
        self.root.configure(bg="#f5f6fa")

        frame = tk.Frame(root, bg="#f5f6fa")
        frame.pack(expand=True)

        tk.Label(frame, text="Поиск на графе",
                 font=("Arial", 16, "bold"),
                 bg="#f5f6fa").pack(pady=10)

        tk.Label(frame, text="Количество вершин:",
                 font=("Arial", 12),
                 bg="#f5f6fa").pack()

        self.entry = tk.Entry(frame, justify="center", font=("Arial", 12))
        self.entry.pack(pady=5)
        self.entry.insert(0, "5")

        tk.Button(frame,
                  text="Далее",
                  font=("Arial", 11),
                  bg="#4CAF50",
                  fg="white",
                  width=15,
                  command=self.start).pack(pady=15)

    def start(self):
        try:
            n = int(self.entry.get())
            if n <= 0:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Введите корректное число")
            return

        self.root.destroy()
        GraphWindow(n)


# ===================== ОКНО 2 =====================
class GraphWindow:
    def __init__(self, n):
        self.n = n
        self.root = tk.Tk()
        self.root.title("Матрица смежности")
        self.root.configure(bg="#ecf0f1")

        main = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=10)
        main.pack()

        tk.Label(main, text="Матрица смежности",
                 font=("Arial", 14, "bold"),
                 bg="#ecf0f1").grid(row=0, column=0, columnspan=n+1, pady=10)

        self.entries = []

        for j in range(n):
            tk.Label(main, text=str(j), bg="#ecf0f1").grid(row=1, column=j+1)

        for i in range(n):
            tk.Label(main, text=str(i), bg="#ecf0f1").grid(row=i+2, column=0)
            row_entries = []
            for j in range(n):
                e = tk.Entry(main, width=3, justify="center")
                e.grid(row=i+2, column=j+1, padx=2, pady=2)
                e.insert(0, "0")
                row_entries.append(e)
            self.entries.append(row_entries)

        control = tk.Frame(main, bg="#ecf0f1")
        control.grid(row=n+2, column=0, columnspan=n+1, pady=10)

        tk.Label(control, text="Начальная:", bg="#ecf0f1").grid(row=0, column=0)
        self.start_entry = tk.Entry(control, width=5)
        self.start_entry.grid(row=0, column=1)

        tk.Label(control, text="Конечная:", bg="#ecf0f1").grid(row=0, column=2)
        self.goal_entry = tk.Entry(control, width=5)
        self.goal_entry.grid(row=0, column=3)

        tk.Button(control,
          text="Вставить матрицу",
          bg="#9b59b6",
          fg="white",
          command=self.open_paste_window).grid(row=0, column=5, padx=10)
        tk.Button(control,
                  text="Найти путь",
                  bg="#3498db",
                  fg="white",
                  command=self.run).grid(row=0, column=4, padx=10)

        result_frame = tk.LabelFrame(main,
                                    text="Результаты",
                                    font=("Arial", 11, "bold"),
                                    bg="#ecf0f1",
                                    padx=10,
                                    pady=10)

        result_frame.grid(row=n+3, column=0, columnspan=n+1, pady=10, sticky="we")

        self.bfs_label = tk.Label(result_frame, text="", anchor="w", bg="#ecf0f1")
        self.bfs_label.pack(fill="x")

        self.dfs_iter_label = tk.Label(result_frame, text="", anchor="w", bg="#ecf0f1")
        self.dfs_iter_label.pack(fill="x")

        self.dfs_rec_label = tk.Label(result_frame, text="", anchor="w", bg="#ecf0f1")
        self.dfs_rec_label.pack(fill="x")

        self.dfs_mod_label = tk.Label(result_frame, text="", anchor="w", bg="#ecf0f1")
        self.dfs_mod_label.pack(fill="x")

        self.root.mainloop()

    def get_graph(self):
        graph = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                val = self.entries[i][j].get()
                if val not in ("0", "1"):
                    raise ValueError
                row.append(int(val))
            graph.append(row)
        return graph

    def run(self):
        try:
            graph = self.get_graph()
            start = int(self.start_entry.get())
            goal = int(self.goal_entry.get())
        except:
            messagebox.showerror("Ошибка", "Проверь ввод")
            return

        bfs_path, bfs_steps = bfs(graph, start, goal)
        dfs_iter = dfs_iterative(graph, start, goal)
        dfs_mod = dfs_modified(graph, start, goal, set(), [], [0])

        
        steps_rec = [0]
        parent = {start: None}
        found = dfs_recursive(graph, start, goal, set(), parent, steps_rec)

        if found:
            dfs_rec = (restore_path(parent, goal), steps_rec[0])
        else:
            dfs_rec = None

        # BFS
        if bfs_path:
            self.bfs_label.config(
                text=f"Поиск в ширину: {' -> '.join(map(str, bfs_path))} | шагов: {bfs_steps}"
            )
        else:
            self.bfs_label.config(text=f"BFS: путь не найден | шагов: {bfs_steps}")

        # DFS итеративный
        if dfs_iter:
            path, steps = dfs_iter
            self.dfs_iter_label.config(
                text=f"Итерационный поиск в глубину: {' -> '.join(map(str, path))} | шагов: {steps}"
            )
        else:
            self.dfs_rec_label.config(text="DFS (итеративный): путь не найден")

        # DFS рекурсивный
        if dfs_rec:
            path, steps = dfs_rec
            self.dfs_rec_label.config(
                text=f"Рекурсивный поиск в глубину: {' -> '.join(map(str, path))} | шагов: {steps}"
            )
        else:
            self.dfs_rec_label.config(text="DFS (рекурсивный): путь не найден")

        # DFS модифицированный
        if dfs_mod:
            path, steps = dfs_mod
            self.dfs_mod_label.config(
                text=f"Модифицированный поиск в глубину: {' -> '.join(map(str, path))} | шагов: {steps}"
            )
        else:
            self.dfs_rec_label.config(text="DFS (модифицированный): путь не найден")
    
    def open_paste_window(self):
        win = tk.Toplevel(self.root)
        win.title("Вставка матрицы")

        tk.Label(win, text="Вставьте матрицу:").pack(pady=5)

        text = tk.Text(win, width=50, height=15)
        text.pack(padx=10, pady=10)

        # 🔥 ПКМ → вставить
        def paste(event):
            text.insert(tk.INSERT, win.clipboard_get())

        text.bind("<Button-3>", paste)

        def apply_matrix():
            try:
                raw = text.get("1.0", tk.END)
                matrix = self.parse_matrix(raw)

                if len(matrix) != self.n:
                    raise ValueError("Размер не совпадает")

                for i in range(self.n):
                    if len(matrix[i]) != self.n:
                        raise ValueError("Матрица должна быть квадратной")

                # заполняем UI
                for i in range(self.n):
                    for j in range(self.n):
                        self.entries[i][j].delete(0, tk.END)
                        self.entries[i][j].insert(0, str(matrix[i][j]))

                win.destroy()

            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        tk.Button(win, text="Применить", command=apply_matrix).pack(pady=5)
    def parse_matrix(self, raw):
        import re

        # убираем лишнее
        raw = raw.strip()

        # ищем строки вида [....]
        rows = re.findall(r'\[([0-9,\s]+)\]', raw)

        if not rows:
            raise ValueError("Не удалось распознать матрицу")

        matrix = []
        for row in rows:
            nums = [int(x.strip()) for x in row.split(",")]
            matrix.append(nums)

        return matrix
# ===================== ЗАПУСК =====================
root = tk.Tk()
app = StartWindow(root)
root.mainloop()