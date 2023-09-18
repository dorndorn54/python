import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    # cells is the count of the number of cells
    # count is the count of the number of mines in the cell

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # only known to be safe if the count is 0 only then are they safe
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # check to see if cell is one of the cells included in the sentence
        if cell in self.cells:
            # if inside then update to remove it
            self.cells.remove(cell)
            # ensure that the count is logically correct
            self.count -= 1
        # no action if cell is not inside

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # check to see if cell is one of the cells included in the sentence
        if cell in self.cells:
            # if inside then need to remove it
            self.cells.remove(cell)
            # no need to subtract from count as the count is the mine count
        # no action taken if the cell is not inside


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) store cell clicked as a move
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) get the neighbours back remmove all safes and moves made if any
        # then create the knowledge base

        # store the tuple in a list
        neighbours = set()
        countmines = 0
        # unpack the tuple
        (i, j) = cell
        # parameters
        surrounding_rows, surrounding_col = range(i-1, i+2), range(j-1, j+2)
        height_lim, width_lim = range(self.height), range(self.width)

        for row in surrounding_rows:
            if row in height_lim:
                for col in surrounding_col:
                    if col in width_lim:
                        if (row, col) in self.mines:
                            countmines += 1
                        neighbours.add((row, col))

        neighbours -= (self.moves_made | self.safes | self.mines)

        # initalise the sentence class
        new_sentence = Sentence(neighbours, count - countmines)
        self.knowledge.append(new_sentence)

        # if known to be a mine
        for sen in self.knowledge:
            # if empty then remove it 
            if len(sen.cells) == 0:
                self.knowledge.remove(sen)
            if sen.known_mines():
                for cell in sen.known_mines().copy():
                    self.mark_mine(cell)
            if sen.known_safes():
                for cell in sen.known_safes().copy():
                    self.mark_safe(cell)

        # need to check if the new sentence is a subset of the original set
        for sen in self.knowledge:
            if new_sentence.cells.issubset(sen.cells) and sen.count > 0 and new_sentence.count > 0 and new_sentence != sen:
                new_subset = sen.cells.difference(new_sentence.cells)
                new_subset_sentence = Sentence(list(new_subset), sen.count - new_sentence.count)
                self.knowledge.append(new_subset_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # generate all potential moves
        all_moves = set(tuple((i, j)) for i in range(self.height) for j in range(self.width))
        # remove already chosen and mine identified cells
        potential_moves = list(all_moves.difference(self.mines, self.moves_made))
        # if there is no moves return None
        if len(potential_moves) != 0:
            return random.choice(potential_moves)
        # if there are moves return a random one
        else:
            return None
