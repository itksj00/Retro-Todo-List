import tkinter as tk
from tkinter import ttk
import calendar
import json

# 데이터 저장소
data = {}

# 메인 창
root = tk.Tk()
root.title("To-Do List")
root.geometry("700x500")

# JSON 데이터 저장/로드
def save_data():
    with open("todo_data.json", "w") as file:
        json.dump(data, file)

def load_data():
    global data
    try:
        with open("todo_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

# 특정 날짜의 To-Do 리스트 표시
def show_todo(year, month, day):
    for widget in main_frame.winfo_children():
        widget.destroy()

    date = f"{year}-{month:02d}-{day:02d}"
    tasks = data.get(date, [])

    ttk.Label(main_frame, text=f"To-Do List for {date}", font=("Arial", 14, "bold")).pack(pady=5)

    task_list = tk.Listbox(main_frame, height=10, width=40)
    task_list.pack(pady=5)
    for task in tasks:
        task_list.insert(tk.END, task)

    def add_task():
        task = task_entry.get().strip()
        if task:
            data.setdefault(date, []).append(task)
            task_list.insert(tk.END, task)
            task_entry.delete(0, tk.END)
            save_data()

    def delete_task():
        selected = task_list.curselection()
        if selected:
            task_index = selected[0]
            task_list.delete(task_index)
            del data[date][task_index]
            save_data()

    # 입력 필드 및 버튼
    task_entry = ttk.Entry(main_frame, width=40)
    task_entry.pack(pady=5)
    add_button = ttk.Button(main_frame, text="Add Task", command=add_task)
    add_button.pack(pady=2)
    delete_button = ttk.Button(main_frame, text="Delete Task", command=delete_task)
    delete_button.pack(pady=2)

    # 뒤로 가기 버튼
    back_button = ttk.Button(main_frame, text="Back to Days", command=lambda: show_days(year, month))
    back_button.pack(pady=10)

# 특정 월의 일 표시 (월화수목금토일 형식)
def show_days(year, month):
    for widget in main_frame.winfo_children():
        widget.destroy()

    ttk.Label(main_frame, text=f"{calendar.month_name[month]} {year}", font=("Arial", 16, "bold")).pack(pady=10)

    # 요일 헤더
    day_header = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_frame = tk.Frame(main_frame)
    header_frame.pack()
    for day in day_header:
        ttk.Label(header_frame, text=day, width=10, anchor="center").pack(side="left")

    # 달력 표시
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        week_frame = tk.Frame(main_frame)
        week_frame.pack()
        for day in week:
            if day != 0:
                day_button = ttk.Button(week_frame, text=str(day), command=lambda d=day: show_todo(year, month, d), width=8)
                day_button.pack(side="left", padx=2, pady=2)
            else:
                ttk.Label(week_frame, text="", width=10).pack(side="left")  # 빈 칸 처리

    # 뒤로 가기 버튼
    back_button = ttk.Button(main_frame, text="Back to Months", command=show_months)
    back_button.pack(pady=10)

# 월 표시
def show_months():
    for widget in main_frame.winfo_children():
        widget.destroy()

    ttk.Label(main_frame, text="Select a Month", font=("Arial", 16, "bold")).pack(pady=10)

    for month in range(1, 13):
        month_button = ttk.Button(main_frame, text=calendar.month_name[month], command=lambda m=month: show_days(2025, m))
        month_button.pack(pady=2)

# 메인 프레임
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# 초기화면
load_data()
show_months()

root.mainloop()
