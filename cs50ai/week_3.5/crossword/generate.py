import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
<<<<<<< HEAD
        # iterate through the value of x
        # check against the key to ensure the same length
        for domain in self.domains:
            to_del = list()
            for value in self.domains[domain]:
                if domain.length != len(value):
                    to_del.append(value)
            for delete in to_del:
                self.domains[domain].remove(delete)
=======
        # iterate through the dict
        # compare the sets of values with the variable
        for domain in self.domains.keys():
            to_remove = list()
            for value in self.domains[domain]:
                if domain.length != len(value):
                    to_remove.append(value)
            # iterate through the remove list and remove from main list
            for rem in to_remove:
                self.domains[domain].remove(rem)
        # no need to return anything               
        
    def check_overlap(x, y, x_val, y_val):
             
>>>>>>> ab8827e7cafa9c00802c726a9808f7f1067b42d6

    def check_overlap(self, x, y, x_variable, y_variable):
        # if no overlap return False
        if not self.crossword.overlaps[x, y]:
            return True
        # if overlap and they match return False
        else:
            x_pos, y_pos = self.crossword.overlaps[x, y]
            # no match
            if x_variable[x_pos] != y_variable[y_pos]:
                return True
            else:
                return False
        # if overlap and they dont match return True
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
<<<<<<< HEAD
        to_del = set()
        for x_variable in self.domains[x]:
            consistent = True
            for y_variable in self.domains[y]:
                if x_variable != y_variable and self.check_overlap(x, y, x_variable, y_variable):
                    consistent = False
                    break
            if not consistent:
                to_del.add(x_variable)
                revised = True

        self.domains[x] -= to_del
        return revised
=======
        to_remove = set()
        
        for x_value in self.domains[x]:
            consistent = False
            for y_value in self.domains[y]:
                if x_value !- y_value and self.check_overlap(x, y, x_val, y_val)
                
        raise NotImplementedError
>>>>>>> ab8827e7cafa9c00802c726a9808f7f1067b42d6

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = list()
        # if the arcs are none
        if arcs is None:
            for x_domain in self.domains:
                for y_domain in self.domains:
                    if x_domain != y_domain:
                        queue.append((x_domain, y_domain))
        else:
            queue = arcs
            while len(queue) != 0:
                (x_val, y_val) = queue.pop()
                if self.revise(x_val, y_val ):
                    if len(self.domains[x_val]) == 0:
                        return False
                    for x_neighbours in self.crossword.neighbours(x_val) - {y_val}:
                    queue.append((x_neighbours, x_val))

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in assignment:
            if len(assignment[variable]) == 0:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        used_variables = list()
        
        for variable in assignment:
            value = assignment[variable]
            
            if value in used_variables:
                return False
            used_variables.append(value)

            if len(value) != variable.length:
                return False

            for variable_y in self.crossword.neigbors(variable):
                if variable_y in assignment:
                    value_y = assignment[variable_y]
                    
                    if not self.check_overlap(variable, variable_y, value, value_y):
                        return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
