class A:
    def __init__(self, name, email, login, parol):
        self.name = name
        self.email = email
        self.login = login
        self.parol = parol
class B(A):
    def __init__(self, name, email, login, parol):
        A.__init__(self, name, email, login, parol)
class C(A):
    def __init__(self, name, email, login, parol):
        A.__init__(self, name, email, login, parol)