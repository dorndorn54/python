import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    """
    expects a command line argument which will be the name of the directory
    to search through to compute PageRanks
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # initalising the dict
    dict_probability = {}

    if len(corpus[page]) != 0:
        # pulling the keys from the value of page
        dict_value_list = list(corpus[page])
        # calculating the neccesary values needed
        prob_value = damping_factor / len(corpus[page])
        residual_value = (1 - damping_factor) / len(corpus)
        sum_value = prob_value + residual_value
        for i in dict_value_list:
            dict_probability[i] = sum_value
        # add the page user is on probability
        dict_update = {"corpus[page]": residual_value}
        dict_probability.update(dict_update)
    if len(corpus[page]) == 0:
        # calculate the necessary values
        sum_value = 1 / len(corpus)
        # store all the keys in the corpus in a list
        corpus_list = list(corpus.keys())
        # generate a dictionary key is the corpus.keys
        # and the value is the prob
        for i in corpus_list:
            dict_probability[i] = sum_value
    # finally return the dictionary
    return dict_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    corpus is the dict
    damping factor is the value
    n is the number of samples that should be generated
    """
    prob_distribution = {page_name: 0 for page_name in corpus}
    for k in prob_distribution:
        prob_distribution[k] = 0
    curr_page = random.choice(list(prob_distribution))
    prob_distribution[curr_page] += 1

    for i in range(0, n-1):
        trans_model = transition_model(corpus, curr_page, damping_factor)

        rand_val = random.random()
        total_prob = 0

        for page_name, probability in trans_model.items():
            total_prob += probability
            if rand_val <= probability:
                curr_page = page_name
                break

        prob_distribution[curr_page] += 1
        
    # loop through every value and divide by the sample size
    prob_distribution = {key: value/n for key, value in prob_distribution.items()}

    # to round everything off so the probability sum is 1
    print("The total sum of the probability is " +str(sum(prob_distribution.values())))
    # return the dictionary
    return prob_distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # copy the corpus and reassigns the values
    page_rank = corpus.copy()
    for i in page_rank:
        page_rank[i] = 1/len(corpus)

    # repeatedly perform the calculation till change is less than 0.001

if __name__ == "__main__":
    main()
