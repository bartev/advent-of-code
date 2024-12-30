from pathlib import Path
from time import sleep

from tqdm import tqdm

steps = 10
for step in tqdm(range(steps)):
    sleep(0.05)

vscript_dir = Path(__name__).parent.absolute()
print(script_dir)

script_dir = Path(__file__).parent.absolute()
print(script_dir)
