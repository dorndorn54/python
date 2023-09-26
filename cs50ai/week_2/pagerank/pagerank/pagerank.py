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
    # acces the dict using the page value
    dict_value_list = corpus[page]
    # page count excluding the page key
    page_count = len(dict_value_list)

    if page_count != 0:
        # calculating the neccesary values needed
        prob_value = (damping_factor / page_count)
        residual_value = (1 - damping_factor) / (page_count + 1)
        sum_value = prob_value + residual_value
        for i in dict_value_list:
            dict_probability[i] = sum_value
        # add the page user is on probability
        dict_probability.update((corpus[page], residual_value))
    if page_count == 0:
        # calculate the necessary values
        sum_value = 1 / len(corpus)
        # store all the keys in the corpus in a list
        corpus_list = list(corpus.keys())
        # generate a dictionary key is the corpus.keys and the value is the probability
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
    """
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
