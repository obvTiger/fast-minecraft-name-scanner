import requests
import itertools
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def fetch_combinations(combinations, tried_combinations, pbar):
    for combination in combinations:
        if combination not in tried_combinations:
            fetch_combination(combination, pbar)

def fetch_combination(combination, pbar):
    url = f"https://api.wireway.ch/mcnameapi/mojang/{combination}"
    while True:
        response = requests.get(url)
        if response.status_code in [200, 404]:
            break
    if response.status_code == 404:
        with open('found.txt', 'a') as f:
            f.write(combination + '\n')
    with open('tried.txt', 'a') as f:
        f.write(combination + '\n')
    pbar.update(1)

def main():
    num_threads = 30
    length = 3
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789_'
    tried_combinations = set()
    with open('tried.txt', 'r') as f:
        tried_combinations.update(line.strip() for line in f)

    combinations = [''.join(combination) for combination in itertools.product(characters, repeat=length)]

    chunk_size = len(combinations) // num_threads
    chunks = [combinations[i:i+chunk_size] for i in range(0, len(combinations), chunk_size)]

    total_combinations = len(combinations)

    with tqdm(total=total_combinations) as pbar:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for chunk in chunks:
                futures.append(executor.submit(fetch_combinations, chunk, tried_combinations, pbar))

            for future in futures:
                future.result()

if __name__ == "__main__":
    main()
