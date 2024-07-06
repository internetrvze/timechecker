from os import system
from concurrent.futures import ThreadPoolExecutor


def run(module: str) -> None:
    return system(f'python {module}.py')


with ThreadPoolExecutor() as pool:
    pool.map(run, ['main', 'userbot'])
