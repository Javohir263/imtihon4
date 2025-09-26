class User:
    def __init__(self, name, email, login, parol):
        self.name = name
        self.email = email
        self.login = login
        self.parol = parol


class Admin(User):
    def __init__(self, name, email, login, parol):
        super().__init__(name, email, login, parol)
        self.teachers = []
        self.students = []
        self.groups = []

    # TEACHER CRUD
    def teacher_create(self):
        name = input("Teacher ismi: ")
        email = input("Email: ")
        login = input("Login: ")
        parol = input("Parol: ")
        subject = input("Fan: ")
        teacher = Teacher(name, email, login, parol, subject)
        self.teachers.append(teacher)
        print("Teacher qo‘shildi")

    def teacher_view(self):
        if not self.teachers:
            print(" Teacher yo‘q")
            return
        for t in self.teachers:
            print(t.view_profile())

    def teacher_delete(self):
        if not self.teachers:
            print(" Teacher yo‘q")
            return
        print("O‘qituvchilar ro‘yxati:")
        for i, t in enumerate(self.teachers):
            print(f"{i + 1}. {t.name} - {t.subject}")
        tanlov = int(input("Qaysi teacherni o‘chiramiz? "))
        try:
            teacher = self.teachers.pop(tanlov - 1)
            # Shu teacherga tegishli guruhlardan ham olib tashlash
            self.groups = [g for g in self.groups if g["teacher"] != teacher]
            print(f"{teacher.name} o‘chirildi va tegishli guruhlardan olib tashlandi")
        except IndexError:
            print("Xato tanlov!")

    # GROUP CRUD
    def group_create(self):
        name = input("Guruh nomi: ")
        fan = input("Fan: ")
        if not self.teachers:
            print(" Avval teacher yarating!")
            return

        print("O‘qituvchilar ro‘yxati:")
        for i, t in enumerate(self.teachers):
            print(f"{i + 1}. {t.name} - {t.subject}")
        tanlov = int(input("Qaysi o‘qituvchiga biriktiramiz? "))
        teacher = self.teachers[tanlov - 1]

        group = {"name": name, "fan": fan, "students": [], "teacher": teacher, "homeworks": []}
        self.groups.append(group)
        print(" Guruh qo‘shildi!")

    def group_view(self):
        if not self.groups:
            print(" Guruh yo‘q")
            return
        for g in self.groups:
            print(
                f"Guruh: {g['name']} | Fan: {g['fan']} | Studentlar: {len(g['students'])} | Teacher: {g['teacher'].name}")

    def group_delete(self):
        if not self.groups:
            print(" Guruh yo‘q")
            return
        print("Guruhlar ro‘yxati:")
        for i, g in enumerate(self.groups):
            print(f"{i + 1}. {g['name']} - {g['fan']}")
        tanlov = int(input("Qaysi guruhni o‘chiramiz? "))
        try:
            group = self.groups.pop(tanlov - 1)
            print(f"{group['name']} guruh o‘chirildi")
        except IndexError:
            print("Xato tanlov!")

    # STUDENT CRUD
    def student_create(self):
        name = input("Student ismi: ")
        email = input("Email: ")
        login = input("Login: ")
        parol = input("Parol: ")
        student = Student(name, email, login, parol)

        if not self.groups:
            print(" Avval guruh yarating!")
            return

        print("Guruhlar ro‘yxati:")
        for i, g in enumerate(self.groups):
            print(f"{i + 1}. {g['name']} - {g['fan']}")
        tanlov = int(input("Studentni qaysi guruhga qo‘shamiz? "))
        self.groups[tanlov - 1]['students'].append(student)
        self.students.append(student)
        print(" Student qo‘shildi!")


    def student_delete(self):
        if not self.students:
            print(" Student yo‘q")
            return
        print("Studentlar ro‘yxati:")
        for i, s in enumerate(self.students):
            print(f"{i + 1}. {s.name}")
        tanlov = int(input("Qaysi studentni o‘chiramiz? "))
        try:
            student = self.students.pop(tanlov - 1)
            # Studentni guruhlardan ham olib tashlash
            for g in self.groups:
                if student in g["students"]:
                    g["students"].remove(student)
            print(f"{student.name} o‘chirildi va guruhlardan olib tashlandi")
        except IndexError:
            print("Xato tanlov!")


class Teacher(User):
    def __init__(self, name, email, login, parol, subject):
        super().__init__(name, email, login, parol)
        self.subject = subject

    def view_profile(self):
        return f" Teacher: {self.name} | Fan: {self.subject} | Login: {self.login}"

    def teacher_groups(self, admin):
        guruhlar = [g for g in admin.groups if g["teacher"] == self]  # list comprehension
        if not guruhlar:
            print(" Sizda guruh yo‘q")
            return
        for g in guruhlar:
            print(f"Guruh: {g['name']} | Fan: {g['fan']} | Studentlar: {len(g['students'])}")

    def give_homework(self, admin):
        guruhlar = [g for g in admin.groups if g["teacher"] == self]
        if not guruhlar:
            print("Sizda guruh yo‘q")
            return
        for i, g in enumerate(guruhlar):
            print(f"{i + 1}. {g['name']}")
        tanlov = int(input("Qaysi guruhga vazifa beramiz? "))
        homework = input("Vazifa matni: ")
        guruhlar[tanlov - 1]["homeworks"].append(homework)
        print(f" {guruhlar[tanlov - 1]['name']} guruhiga uyga vazifa berildi")

    def put_grade(self, admin):
        guruhlar = [g for g in admin.groups if g["teacher"] == self]
        if not guruhlar:
            print("Sizda guruh yo‘q")
            return
        for i, g in enumerate(guruhlar):
            print(f"{i + 1}. {g['name']}")
        tanlov = int(input("Qaysi guruhdan studentga baho qo‘yamiz? "))
        guruh = guruhlar[tanlov - 1]

        if not guruh["students"]:
            print("Guruhda student yo‘q")
            return

        for i, s in enumerate(guruh["students"]):
            print(f"{i+1}. {s.name}")
        try:
            st_tanlov = int(input("Qaysi student? "))
            baho = int(input("Bahoni kiriting: "))
            guruh["students"][st_tanlov-1].grades.append(baho)
            print("Baho qo‘yildi")
        except (IndexError, ValueError):
            print("Xato tanlov!")


class Student(User):
    def __init__(self, name, email, login, parol):
        super().__init__(name, email, login, parol)
        self.grades = []

    def view_profile(self):
        return f"Student: {self.name} | Login: {self.login} | Email: {self.email}"

    def view_grades(self):
        if not self.grades:
            return " Sizda hali baho yo‘q"
        return f" Sizning baholaringiz: {self.grades}"

    def view_homeworks(self, admin):
        topildi = False
        for g in admin.groups:
            if self in g["students"]:
                topildi = True
                if not g["homeworks"]:
                    print(f" {g['name']} guruhida uyga vazifa yo‘q")
                else:
                    print(f"{g['name']} guruhining uyga vazifalari:")
                    for h in g["homeworks"]:
                        print("-", h)
        if not topildi:
            print(" Siz hech qaysi guruhga biriktirilmagansiz")


def login_system():
    admin = Admin("Super Admin", "admin@gmail.com", "admin", "1234")  # default admin
    users = [admin]

    while True:
        tanlov = input("\n1. Login\n2. Exit\n>>> ")
        if tanlov == "1":
            login = input("Login: ")
            parol = input("Parol: ")


            # Admin login
            if login == admin.login and parol == admin.parol:
                print("\nAdmin paneliga xush kelibsiz!")
                while True:
                    menu = input(
                        "\n1. Teacher qo‘shish\n"
                        "2. Teacher ko‘rish\n"
                        "3. Teacher o‘chirish\n"
                        "4. Guruh qo‘shish\n"
                        "5. Guruh ko‘rish\n"
                        "6. Guruh o‘chirish\n"
                        "7. Student qo‘shish\n"
                        "8. Student ko‘rish\n"
                        "9. Student o‘chirish\n"
                        "0. Logout\n>>> "
                    )
                    if menu == "1":
                        admin.teacher_create()
                        users.extend(admin.teachers)
                    elif menu == "2":
                        admin.teacher_view()
                    elif menu == "3":
                        admin.teacher_delete()
                    elif menu == "4":
                        admin.group_create()
                    elif menu == "5":
                        admin.group_view()
                    elif menu == "6":
                        admin.group_delete()
                    elif menu == "7":
                        admin.student_create()
                        users.extend(admin.students)
                    elif menu == "8":
                        for s in admin.students:
                            print(s.view_profile())
                    elif menu == "9":
                        admin.student_delete()
                    elif menu == "0":
                        break

            # Teacher login
            for t in admin.teachers:
                if login == t.login and parol == t.parol:
                    print(f"\nTeacher paneliga xush kelibsiz {t.name}!")
                    while True:
                        menu = input(
                            "\n1. O‘z guruhlarini ko‘rish\n"
                            "2. Studentlarga uyga vazifa berish\n"
                            "3. Studentga baho qo‘yish\n"
                            "0. Logout\n>>> "
                        )
                        if menu == "1":
                            t.teacher_groups(admin)
                        elif menu == "2":
                            t.give_homework(admin)
                        elif menu == "3":
                            t.put_grade(admin)
                        elif menu == "0":
                            break

            # Student login
            for s in admin.students:
                if login == s.login and parol == s.parol:
                    print(f"\nStudent paneliga xush kelibsiz {s.name}!")
                    while True:
                        menu = input(
                            "\n1. Profilni ko‘rish\n"
                            "2. Baholarni ko‘rish\n"
                            "3. Uyga vazifalarni ko‘rish\n"
                            "0. Logout\n>>> "
                        )
                        if menu == "1":
                            print(s.view_profile())
                        elif menu == "2":
                            print(s.view_grades())
                        elif menu == "3":
                            s.view_homeworks(admin)
                        elif menu == "0":
                            break

        elif tanlov == "2":
            print("Dastur tugadi.")
            break
        else:
            print(" Xato buyruq")


login_system()
