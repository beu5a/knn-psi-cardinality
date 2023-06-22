import csv
from collections import defaultdict
from itertools import combinations
import sys

def create_user_profiles(csv_file):
    user_profiles = defaultdict(set)

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            userid, movieid, rating, _ = row
            rating = float(rating)
            if rating > 3.5:
                user_profiles[userid].add(movieid)

    return user_profiles

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    return intersection / union

if __name__ == '__main__':
    csv_file = '../ml-latest-small/ratings.csv'  # Replace with the actual path to your CSV file
    k = int(sys.argv[1])
    total_nodes = int(sys.argv[2])

    user_profiles = create_user_profiles(csv_file)

    # Define the output file name
    output_file = "jaccard_results.txt"

    # Compute the pairwise Jaccard similarity
    with open(output_file, 'w') as file:
        for i in range(1, total_nodes + 1):
            for j in range(i + 1, total_nodes + 1):
                set1 = user_profiles[str(i)]
                set2 = user_profiles[str(j)]
                similarity = jaccard_similarity(set1, set2)
                file.write(f"{i},{j}: {similarity}\n")

    print("Oracle Construction Complete!")
