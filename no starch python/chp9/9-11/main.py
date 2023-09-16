from user import Admin, Privileges

john = Admin('John', 'wong', 'pewster', 'johntan@gmail.com', 'china')
john.describe_user()

john_privileges = [
    'can reset passwords',
    'can moderate discussions',
    'can suspend accounts',
    ]

john.privileges.privileges = john_privileges
john.privileges.show_privileges()
