class REST:
    # class of a restaurant
    def __init__(self, name, cuisine):
        self.name = name.title()
        self.cuisine = cuisine.title()

    def d_r(self):
        print(self.name + " is now selling " + self.cuisine + ".")
    def o_r(self):
        print("the restaurant " + self.name +" is open.")

rest_1 = REST('wing wong', 'chinese')
rest_2 = REST('ding dong', 'american')
rest_3 = REST('ling long', 'russian')

print(rest_1.name)
print(rest_1.cuisine)

rest_1.d_r()
rest_2.d_r()
rest_3.d_r()
