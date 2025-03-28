from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
import hashlib
import db
from setting import password_salt
import datetime


class App():

    def __init__(self):
        
        root = Tk()
        root.title("Приложение на Tkinter")
        root.geometry("1280x720")
        # root.attributes("-fullscreen", True)

        self.root= root
    
        # self.test_screen()
        self.main_screen()

    def test_screen(self):
        w = int(self.root.winfo_screenwidth())
        h = int(self.root.winfo_screenheight())

        self.main_cont = Frame(self.root, width=w, height=h)
        self.main_cont.pack(fill=BOTH)
        self.head_frame = Frame(self.main_cont, width=w, height=h)
        self.head_frame.pack(anchor=E, fill=X)
        self.main_frame = Frame(self.main_cont, width=w, height=h)
        self.main_frame.pack(anchor=CENTER)

        self.account_screen()

    def main_screen(self):

        w = int(self.root.winfo_screenwidth())
        h = int(self.root.winfo_screenheight())

        print(w,h)

        self.main_cont = Frame(self.root, width=w, height=h)
        self.main_cont.pack(fill=BOTH)
        self.head_frame = Frame(self.main_cont, width=w, height=h)
        self.head_frame.pack(anchor=E, fill=X)
        self.main_frame = Frame(self.main_cont, width=w, height=h)
        self.main_frame.pack(anchor=CENTER)
        
        Button(self.head_frame, text="Выход", command=self.root.destroy, width=10, height=2).pack(anchor=E)
        # exit_button.place(x=w*0.95, y=0)
        Button(self.main_frame ,text="Вход", command= self.user, width=40, height=5).pack(anchor=CENTER)
        # client_button.place(x=w/2-150, y=h/2-100)
        Button(self.main_frame, text="Регистрация", command=self.register, width=40, height=5).pack(anchor=CENTER, pady=10)


    def clear_window(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    
    def default_login_screen(self, frame):
        back_button = Button(self.head_frame, text="Назад", command=self.back_func, width=10, height=2)
        back_button.pack(anchor=E)
        Label(frame, text="ФИО:", font=('Arial 18')).grid(sticky=W, row=0, column=0, columnspan=3)
        Entry(frame, name="fio", width=30, font=('Arial 22')).grid(row=1, column=0)
        Label(frame, text="Логин:", font=('Arial 18')).grid(sticky=W, row=2, column=0, columnspan=3)
        Entry(frame, name="login_value", width=30, font=('Arial 22')).grid(row=3, column=0, columnspan=2)
        Label(frame, text="Пароль:", font=('Arial 18')).grid(sticky=W,row=4, column=0, columnspan=3)
        Entry(frame, name="password", width=30, font=('Arial 22'), show="*").grid(row=5, column=0, columnspan=2)
        Button(frame, width=3, height=1, command=self.hide_password).grid(padx=5, row=5, column=2)
        

    def user(self):
        self.clear_window()
        user_frame = Frame(self.main_frame, name="user_login")
        user_frame.pack(anchor=CENTER)
        self.default_login_screen(user_frame)

        Button(user_frame, text="Вход", width=20, height=3, command=self.user_authentication).grid(pady=20, row=6, column=0, columnspan=2)

    def register(self):
        self.clear_window()
        register_frame= Frame(self.main_frame, name="register")
        register_frame.pack(anchor=CENTER)
        self.default_login_screen(register_frame)

        Label(register_frame, text="Повторите пароль:", font=('Arial 18')).grid(sticky=W,row=6, column=0, columnspan=3)
        Entry(register_frame, name="repeat_password", width=30, font=('Arial 22'), show="*").grid(row=7, column=0, columnspan=2)
        Button(register_frame, text="регистрация", width=20, height=3, command=self.register_user).grid(pady=20, row=9, column=0, columnspan=2)

    def hide_password(self):
        login_window = self.main_frame.children.get("worker_login") or self.main_frame.children.get("user_login") or self.main_frame.children.get("register")
        for password_key in ["password", "repeat_password"]:
            password = login_window.children.get(password_key)
            if password:
                print(password.cget('show'))
                if password.cget('show') == '':
                    password.config(show="*")
                else:
                    password.config(show="")
            else:
                continue
                # raise Exception("ERRRRRROOOOR")

    def user_authentication(self):
        get_value = self.main_frame.children.get("user_login")
        login_value = get_value.children.get("login_value").get()
        password_value = get_value.children.get("password").get()
        fio_value = get_value.children.get("fio").get()
        password_value = hashlib.sha256((password_value+password_salt).encode('utf-8')).hexdigest()
        if db.search_user_for_login(login_value, password_value):
            self.user_fio = db.search_user_for_fio(login_value, password_value, fio_value)
            self.account_screen()
        else:
            print('not')
            messagebox.showinfo(title="Ошибка входа", message="Неправильный логин или пароль")

        db.check_log_in()
        

    def register_user(self):
        get_value = self.main_frame.children.get("register")
        login_value = get_value.children.get("login_value").get()
        password_value = get_value.children.get("password").get()
        repeat_password = get_value.children.get("repeat_password").get()
        fio_value = get_value.children.get("fio").get()
        if "wr_" in login_value:
            pass
        if password_value == repeat_password:
            password_value = hashlib.sha256((password_value+password_salt).encode('utf-8')).hexdigest()
            print(login_value, password_value)
            if not db.check_and_get_user(login_value):
                db.insert_value(login_value, password_value, fio_value)
                self.user_fio = db.search_user_for_fio(login_value, password_value, fio_value)
                self.account_screen()
            else:
                messagebox.showwarning(title='nini', message='пользователь с таким логином есть')
        else:
            messagebox.showwarning(title='nini', message='пароли не совпадают')
        db.check_log_in()
        
    def admin_account_screen(self):
        print("admin_account")
        self.clear_window()
        

    def account_screen(self):
        # очистка main_frame
        self.clear_window()
        # очистка head_frame 
        for widget in self.head_frame.winfo_children():
            widget.destroy()
        search_frame = Frame(self.head_frame, name="search_frame")
        search_frame.pack(anchor=CENTER)
        request_frame = Frame(self.main_frame, name="request_frame")
        request_frame.pack(anchor=N)

        self.main_menu = Menu()
        self.acc_menu = Menu()
        self.main_menu.add_cascade(label="Акк", menu=self.acc_menu)
        self.acc_menu.add_command(label=f"{self.user_fio}")
        self.acc_menu.add_command(label="Выйти из аккаунта", command=self.back_func)
        self.acc_menu.add_command(label="Выйти из приложения", command=self.root.destroy)
        
        Button(request_frame, text="Подать заявку", name="gg", width=40, height=3, command=self.new_request_screen).grid(row=0, column=0, pady=30)
        Button(request_frame, text="Мои заявки", name="my_request", width=40, height=3, command=self.user_request_screen).grid(row=0, column=1)

        self.root.config(menu=self.main_menu)

    def new_request_screen(self):
        self.clear_window()
        for widget in self.head_frame.winfo_children():
            widget.destroy()

        equipment_list = ["ПК","Ноутбук","Телефон"]
        defect_list = ["a","b", "c"]

        self.date = datetime.date.today()

        request_frame = Frame(self.main_frame, name="request_screen_frame")
        request_frame.pack()

        back_button = Button(self.head_frame, text="Назад", command=self.account_screen, width=10, height=2)
        back_button.pack(anchor=E)

        Label(request_frame, name="date_label", text="Дата:", font=('Arial 14')).grid(row=1, column=0, sticky=W)
        Label(request_frame, name="date", text=f"{self.date}", font=("Arial 14")).grid(row=1, column=1, sticky=E)

        Label(request_frame, name="equipment_type_label", text="Тип обрудования:", font=('Arial 14')).grid(row=2, column=0, sticky=W)
        ttk.Combobox(request_frame, name="equipment_combobox", values=equipment_list, state="readonly", width=40, font=('Arial 14')).grid(row=3, column=0, sticky=W)

        Label(request_frame, name="defect_type_label", text="Тип неисправности:", font=("Arial 14")).grid(row=4, column=0, sticky=W)
        ttk.Combobox(request_frame, name="defect_type_combobox", values=defect_list, state="readonly", width=40, font=('Arial 14')).grid(row=5, column=0, sticky=W)

        Label(request_frame, name="defect_description_label", text="Описание проблемы:", font=("Arial 14")).grid(row=6, column=0, sticky=W)
        Text(request_frame, name="defect_description", width=45, height=8, wrap="word", font=("Arial 14")).grid(row=7, column=0, sticky=W)

        Label(request_frame, name="client_label", text="Клиент:", font=("Arial 14")).grid(row=8, column=0, sticky=W)
        Label(request_frame, name="client", text=f"{self.user_fio}", font=("Arial 14")).grid(row=8, column=1, sticky=E)

        Button(request_frame, name="send_request", text="Отправить заявку", command=self.request_to_db, width=30, height=2).grid(row=9, column=1)

    def request_to_db(self):
        get_value = self.main_frame.children.get("request_screen_frame")
        equipment_value = get_value.children.get("equipment_combobox").get()
        defect_value = get_value.children.get("defect_type_combobox").get()
        description_value = get_value.children.get("defect_description").get(1.0, 'end-1c')
        db.send_request(self.date, equipment_value, defect_value, description_value, self.user_fio)
        messagebox.showwarning(title='congrat', message='Ваша заявка принята')
        self.account_screen()
    
    def back_func(self):
        try:
            self.main_menu.destroy()
            self.acc_menu.destroy()
        except Exception as error:
            print(f"[ERROR]: {error}")

        self.main_cont.pack_forget()
        self.head_frame.pack(anchor=E, fill=X)
        self.main_screen()

    def user_request_screen(self):
        self.clear_window()
        for widget in self.head_frame.winfo_children():
            widget.destroy()
        
        user_request_frame = Frame(self.main_frame, name="user_request_screen", borderwidth=1, relief=SOLID)
        user_request_frame.pack()

        back_button = Button(self.head_frame, text="Назад", command=self.account_screen, width=10, height=2)
        back_button.pack(anchor=E)

        request_data = db.request_from_db(self.user_fio)
        if not request_data:
            Label(user_request_frame, name="none_request_label", text="Заявок нет", font=("Arial 14")).grid(row=0, column=0)
        else:
            columns = ("1","2","3","4","5")
            columns_text = ("Номер заявки","Дата","Тип оборудования","Тип неисправности","Описание проблемы")
            self.tree = ttk.Treeview(user_request_frame, show="headings", columns=columns)

            for i in zip(columns, columns_text):
                self.tree.heading(i[0], text=i[1])

            for i in request_data:
                self.tree.insert("", END, values=i)

            self.tree.bind("<<TreeviewSelect>>", self.edit_request_screen)
            self.tree.pack()
    
    def edit_request_screen(self, event):
        print(event )
        edit_frame = Frame(self.main_frame, name="edit_frame")
        edit_frame.pack()

        equipment_list = ["ПК","Ноутбук","Телефон"]
        defect_list = ["a","b", "c"]

        Label(edit_frame, name="edit_equipment_type_label", text="Тип обрудования:", font=('Arial 14')).grid(row=2, column=0, sticky=W)
        ttk.Combobox(edit_frame, name="edit_equipment_combobox", values=equipment_list, state="readonly", width=40, font=('Arial 14')).grid(row=3, column=0, sticky=W)

        Label(edit_frame, name="edit_defect_type_label", text="Тип неисправности:", font=("Arial 14")).grid(row=4, column=0, sticky=W)
        ttk.Combobox(edit_frame, name="edit_defect_type_combobox", values=defect_list, state="readonly", width=40, font=('Arial 14')).grid(row=5, column=0, sticky=W)

        Label(edit_frame, name="edit_defect_description_label", text="Описание проблемы:", font=("Arial 14")).grid(row=6, column=0, sticky=W)
        Text(edit_frame, name="edit_defect_description", width=45, height=8, wrap="word", font=("Arial 14")).grid(row=7, column=0, sticky=W)

        Button(self.main_frame, name="edit_button", text="Редактировать", command=self.edit_request).pack()

    def edit_request(self):

        get_value = self.main_frame.children.get("edit_frame")
        queipment_value = get_value.children.get("edit_equipment_combobox",{}).get()
        defect_value = get_value.children.get("edit_defect_type_combobox",{}).get()
        description_value = get_value.children.get("edit_defect_description",{}).get(1.0, 'end-1c')

        curItem = self.tree.focus()
        if curItem:
            request_id = self.tree.item(curItem)["values"][0]

        db.update_values(request_id, queipment_value, defect_value, description_value)

        self.user_request_screen()

    

    def run(self):
        self.root.mainloop()
    
a = App()
a.run()