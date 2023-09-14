from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# a knight tells the truth
# a knave tells a lie

# setup a knowledge base that will be true for all circumstance
KnowledgeBase = And(
    # A can either be a knight or a knave but not both
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
    # B can either be a knight or a knave but not both
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),
    # C can either be a knight or a knave but not both
    Or(CKnight, CKnave), Not(And(CKnight, CKnave))
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    KnowledgeBase,
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnave, AKnight)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    KnowledgeBase,
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    KnowledgeBase,
    # A is a knave
    Implication(AKnave, Or(Not(And(AKnave, BKnave)), Not(And(AKnight, BKnight)))),
    # A is a knight
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # B is a knight
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
    # B is a knave
    Implication(BKnave, Or(Not(And(AKnave, BKnight)), Not(And(AKnight, BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    KnowledgeBase,
    # 1st statement
    # A is knight
    Implication(AKnight, Or(AKnight, AKnave)),
    # A is Knave
    Implication(AKnave, Not(Or(AKnight, AKnave))),

    # 2nd statement
    # B is a knight
    Implication(BKnight, Or(Implication(AKnight, BKnave), Implication(AKnave, BKnave)))
    # B is a knave
    Implication(BKnight, Or(Implication(AKnight, Not(BKnave)), Implication(AKnave, Not(BKnave))))
    # 3rd statement
    # B is a Knight
    Implication(BKnight, CKnave),
    # B is a Knave
    Implication(BKnave, Not(CKnave))
    
    

    # TODO
)


def main():
    # simple list
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    # a list of a dictionary
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
