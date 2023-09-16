class USER:
    # class of a user
    def __init__(self,first_name, last_name, age):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.age = age

	# functions
    def d_user(self):
        print("My name is " + self.first_name + " " +self.last_name + ". My age is " + str(self.age))
    def g_user(self):
        print("greetings")

user_1 = USER('john', 'lee', 29)
user_2 = USER('tim', 'wong', 55)

user_1.d_user()
user_2.d_user()