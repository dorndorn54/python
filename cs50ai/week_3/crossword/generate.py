import sys
import random

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
        # copy the dictionary to iterate
        iter_domain = self.domains.copy()
        # iterate over the key
        for variable in iter_domain.key():
            # iterate over the values associated with the key
            for value in iter_domain[variable]:
                # check the value associated with the key match
                if len(variable) != value:
                    # if no match then remove
                    self.domains[variable].remove(value)

    def check_overlap(self, x_iter, y_iter, x, y):
        """_return false if nothing to check
            returns a tuple of (i, j) x, y if math_

        Args:
            x_iter (_type_): _position of x_
            y_iter (_type_): _position of y_
        """
        if self.crossword.overlaps[x, y] is None:
            return True
        else:
            # check if they match
            if x[x_iter] == y[y_iter]:
                return True
            else:
                return False

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        to_del = set()

        for x_iter in self.domains[x]:
            for y_iter in self.domains[y]:
                # True if no overlap or no mismatch
                # False if mismatch
                if self.check_overlap(x_iter, y_iter, x, y) is False:
                    to_del.add(x_iter)
                    revised = True

        for word in to_del:
            self.domains[x].remove(word)

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = list()
        # if empty then form an arc with every other thing
        if arcs is None:
            for x_val in self.domains:
                for y_val in self.domains:
                    if x_val != y_val:
                        queue.append((x_val, y_val))
        # if there is already arcs then just transfer to the queue
        # avoid using assignment as it will then point to the orignal copy
        else:
            queue = arcs.copy()

        while len(queue) > 0:
            (x_val, y_val) = queue.pop()
            if self.revise(x_val, y_val):
                if len(x_val) == 0:
                    return False
                for x_neighbours in (self.crossword.neighbours(x_val) - y_val):
                    queue.insert(0, (x_neighbours, x_val))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for word in assignment.values():
            if len(word) == 0:
                return False
            else:
                return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.

        all values are distinct
        every value is the correct length
        no conflicts between neighbouring values
        """
        # check if they are distinct no match
        dict_values = assignment.values()
        if len(dict_values) != len(set(dict_values)):
            return False
        # check if they are correct length
        # the variable must match the string length
        for keys, values in assignment.items():
            if len(keys) != len(values):
                return False
        # check if they conflict
        # checker to prevent entering same values
        for variables in assignment.keys():
            # collect the neighbours data
            neighbours = self.crossword.neighbors(variables)
            # iterate through the neighbours and obtain
            for neighbour in neighbours:
                pos_1, pos_2 = self.crossword.overlaps[variables, neighbour]
                if variables[pos_1] != neighbour[pos_2]:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.

        var is a list of words that can fit inside the variable
        meant to iterate through var and check against empty neighbours
        if neighbour is in assignment then skip
        if not then check against the the values in the neighbour
        if they do not match then eliminate the value
        """
        # use a dictionary to sort words of var and their elimination count
        elim_words = dict()
        # obtain the neighburs of var
        neighbours = self.crossword.neighbors(var)
        # iterate through a list of the var
        for word in self.domains[var]:
            elim = 0
            for neighbour in neighbours:
                if neighbour in assignment.keys():
                    continue
                else:
                    # calculate overlap point
                    var_overlap, neighbour_overlap = self.crossword.overlaps[var, neighbour]
                    # iterate through the potential neighbour words to check
                    for neighbour_word in self.domains[neighbour]:
                        # if mismatch then add to elim value
                        if word[var_overlap] != neighbour_word[neighbour_overlap]:
                            elim += 1
            # append the word and the associated elim counter value to the dict
            elim_words[word] = elim
        # sort the dictionary values and convert it to a list
        sorted_elim = (sorted(elim_words, key=lambda x: elim_words[x])).keys()
        # return the dict
        return sorted_elim

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        lowest_value = None
        lowest_variable = list()

        # iterate through the assignment dict
        for key, value in assignment.items():
            if lowest_value is None or len(value) < lowest_value:
                lowest_value = len(value)
                lowest_variable = key
            elif len(value) == lowest_value:
                # calculate the degree
                current_degree = len(self.crossword.neighbors(lowest_value))
                incoming_degree = len(self.crossword.neighbors(key))
                # if incoming more degree then replace
                if current_degree < incoming_degree:
                    lowest_variable = key
                # if they are the same let random choose arbitrarily
                elif current_degree == incoming_degree:
                    lowest_variable = random.choice([lowest_variable, key])
        # send the lowest word back
        return lowest_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if assignment:
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            # assign a value first to test
            assignment[var] = value
            if self.consistent(assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                assignment.pop(var)
        return None


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
