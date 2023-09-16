class User():
    """Represent a simple user profile."""

    def __init__(self, first_name, last_name, username, email, location):
        """Initialize the user."""
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.username = username
        self.email = email
        self.location = location.title()

    def describe_user(self):
        """Display a summary of the user's information."""
        print("\n" + self.first_name + " " + self.last_name)
        print("  Username: " + self.username)
        print("  Email: " + self.email)
        print("  Location: " + self.location)

    def greet_user(self):
        """Display a personalized greeting to the user."""
        print("\nWelcome back, " + self.username + "!")


class Admin(User):
    # represents a admin profile
    def __init__(self, first_name, last_name, username, email, location): #initalise the attributes of the parent class
        super().__init__(first_name, last_name, username, email, location)
        self.privileges = [ ] #declaring the list to store the input of privelleges

    def show_privileges(self):
        #print out the list of privileges
        print("\nThe privileges of the admin are:")
        for p in self.privileges:
            print("-" + p)

eric = Admin('eric', 'matthes', 'e_matthes', 'e_matthes@example.com', 'alaska')
eric.describe_user()
eric.greet_user()

eric.privileges = ["delete post", "modify post", "fly away"]
eric.show_privileges()