import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    # loading a dictionary
    # the key is the name and the value is another dict of information of the person
    # true if they have trait false if they dont have trait
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # value to multiply later to return
    joint_probability = 1
    # the loop to calculate the joint probability
    # cover each case of one gene two gene and no gene
    for person in people:
        # no_gene, one_gene, two_gene
        person_genes = (2 if person in two_genes else 1 if person in one_gene else 0)

        # if there is no parents use standard calculation
        # to calculate the probability they have a particular number of gene
        gene_probability = 1
        mother = people[person]['mother']
        father = people[person]['father']

        if not mother and not father:
            gene_probability *= PROBS["gene"][person_genes]

        # if there is parent then use function calculation
        else:
            # use a function to call it twice for both mother and father
            mother_probability = inherit_prob(mother, one_gene, two_genes)
            father_probability = inherit_prob(father, one_gene, two_genes)

            # calculate for the kid the probability of him getting 0, 1, 2
            # based on the request of the function call
            if person_genes == 2:
                # each parent give one
                gene_probability *= mother_probability * father_probability
            if person_genes == 1:
                # one of the parent give one
                # gets from mother not father and gets from father not mother
                gene_probability *= (mother_probability) * (1 - father_probability) + (father_probability) * (1 - mother_probability)
            if person_genes == 0:
                # neither of the parents give the gene
                gene_probability *= (1 - mother_probability) * (1 - father_probability)

        # consider the have trait part of the calculation
        # last part is to determine if the person is in have_trait
        gene_probability *= PROBS["trait"][person_genes][person in have_trait]
        joint_probability *= gene_probability

    # return the entire joint probability calculation back to the function
    return joint_probability

def inherit_prob(parent, one_gene, two_genes):
    # parent with no_gene
    if parent not in one_gene or two_genes:
        return PROBS["mutation"]      
    # parent with one_gene
    if parent in one_gene:
        return 0.5
    # parent with two_genes
    if parent in two_genes:
        return 1 - PROBS["mutation"]



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # access one person(key) in the probabilities dictionary
    for person in probabilities:
        # calculate the factor value
        gene_factor = 1 / sum(probabilities[person]["gene"].values())
        trait_factor = 1 / sum(probabilities[person]["trait"].values())
        
        # iterate through each person gene and divide each value by the gene factor
        # do the same for the trait factor


if __name__ == "__main__":
    main()
