import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("650x500")
        
        self.expenses = self.load_data()
        self.create_widgets()
        self.update_table()

    def load_data(self):
        try:
            with open('expenses.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self):
        with open('expenses.json', 'w', encoding='utf-8') as f:
            json.dump(self.expenses, f, indent=4, ensure_ascii=False)

    def create_widgets(self):
        # Поля ввода
        frame_input = tk.LabelFrame(self.root, text="Добавить расход", padx=10, pady=10)
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Сумма:").grid(row=0, column=0)
        self.ent_amount = tk.Entry(frame_input)
        self.ent_amount.grid(row=0, column=1)

        tk.Label(frame_input, text="Категория:").grid(row=0, column=2)
        self.cb_category = ttk.Combobox(frame_input, values=["Еда", "Транспорт", "Развлечения", "Жилье", "Прочее"])
        self.cb_category.grid(row=0, column=3)

        tk.Label(frame_input, text="Дата (ДД.ММ.ГГГГ):").grid(row=1, column=0)
        self.ent_date = tk.Entry(frame_input)
        self.ent_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.ent_date.grid(row=1, column=1)

        btn_add = tk.Button(frame_input, text="Добавить расход", command=self.add_expense, bg="lightgreen")
        btn_add.grid(row=1, column=2, columnspan=2, sticky="we", padx=5)

        # Фильтры
        frame_filter = tk.LabelFrame(self.root, text="Фильтрация и Итоги", padx=10, pady=10)
        frame_filter.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filter, text="Категория:").grid(row=0, column=0)
        self.filter_cat = ttk.Combobox(frame_filter, values=["Все"] + ["Еда", "Транспорт", "Развлечения", "Жилье", "Прочее"])
        self.filter_cat.current(0)
        self.filter_cat.grid(row=0, column=1)

        btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=self.update_table)
        btn_filter.grid(row=0, column=2, padx=5)

        self.lbl_total = tk.Label(frame_filter, text="Итого: 0", font=("Arial", 10, "bold"))
        self.lbl_total.grid(row=0, column=3, padx=20)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Категория", "Сумма"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_expense(self):
        amount = self.ent_amount.get()
        category = self.cb_category.get()
        date_str = self.ent_date.get()

        # Валидация
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность суммы (>0) и даты (ДД.ММ.ГГГГ)")
            return

        if not category:
            messagebox.showwarning("Внимание", "Выберите категорию")
            return

        self.expenses.append({"date": date_str, "category": category, "amount": amount})
        self.save_data()
        self.update_table()
        self.ent_amount.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        filter_c = self.filter_cat.get()
        total = 0
        
        for exp in self.expenses:
            if filter_c == "Все" or exp['category'] == filter_c:
                self.tree.insert("", "end", values=(exp['date'], exp['category'], exp['amount']))
                total += exp['amount']
        
        self.lbl_total.config(text=f"Итого: {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
