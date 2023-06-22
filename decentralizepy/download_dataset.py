import argparse
import torchvision
import requests
import os
import zipfile

def download_movie_lens(dest_path):
    """
    Downloads the movielens latest small dataset.
    This data set consists of:
        * 100836 ratings from 610 users on 9742 movies.
        * Each user has rated at least 20 movies.

    https://files.grouplens.org/datasets/movielens/ml-latest-small-README.html
    """
    url = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    req = requests.get(url, stream=True)

    print("Downloading MovieLens Latest Small data...")
    with open(os.path.join(dest_path, "ml-latest-small.zip"), "wb") as fd:
        for chunk in req.iter_content(chunk_size=None):
            fd.write(chunk)
    with zipfile.ZipFile(os.path.join(dest_path, "ml-latest-small.zip"), "r") as z:
        z.extractall(dest_path)
    print("Downloaded MovieLens Latest Small dataset at", dest_path)
    
def download_datasets(dataset):
    if dataset == "cifar10":
        torchvision.datasets.CIFAR10(root="./eval/data/", train=True, download=True)
        torchvision.datasets.CIFAR10(root="./eval/data/", train=False, download=True)
        print("Downloaded MovieLens Latest Small dataset at", "./eval/data/")

    elif dataset == "movielens":
        root = "./eval/data/"
        zip_file = os.path.join(root, "ml-latest-small.zip")
        if not os.path.isfile(zip_file):
            download_movie_lens(root)
    else:
        print("Invalid dataset choice")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset Downloader")
    choices=["cifar10", "movielens"]
    parser.add_argument("dataset", choices=choices, 
                        help="Specify the dataset to download{}".format(choices))

    args = parser.parse_args()
    download_datasets(args.dataset)