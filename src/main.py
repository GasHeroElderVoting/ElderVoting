import csv
import hashlib
import numpy as np
from seeds import polygon_block_hash, candidates_csv

def weighted_sample(population, weights, k):
    """
    Return a k length list of unique elements chosen from the population sequence.
    The weights sequence must be the same length as the population sequence. 
    It defines the relative weights/probabilities for selection of each element.
    """
    indices = np.arange(len(population))
    chosen_indices = np.random.choice(indices, size=k, replace=False, p=weights/np.sum(weights))
    return [population[i] for i in chosen_indices]

def main():
    # Parsing CSV data
    candidate_data = []
    original_names = {}  # Store original codename mapping

    for row in csv.DictReader(candidates_csv.splitlines()):
        codename = row["codename"].strip()
        lowercase_codename = codename.lower()
        
        donation = float(row["donation"].strip())
        candidate_data.append((lowercase_codename, donation))
        original_names[lowercase_codename] = codename

    # Sort based on the lowercase codenames
    candidate_data.sort(key=lambda x: x[0])

    # Extract sorted candidates and weights
    sorted_candidates = [x[0] for x in candidate_data]
    weights = [x[1] for x in candidate_data]

    # Step 3: Generate the random seed using the specified polygon block hash 
    hashed_seed = hashlib.sha256(str(polygon_block_hash).encode()).hexdigest()
    np.random.seed(int(hashed_seed, 16) % (2**32 - 1))  # Numpy expects a 32-bit int for seeding

    # Weighted random sampling from sorted list
    selected_elders = weighted_sample(sorted_candidates, weights, k=min(7,len(weights)))

    # Print selected elders, one per line, with their original codename
    for elder in sorted(selected_elders, key=lambda x: original_names[x]):
        print(original_names[elder])

if __name__ == "__main__":
    main()
