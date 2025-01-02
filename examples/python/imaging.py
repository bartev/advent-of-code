# The Python Journey - Working with Images and Animations
# https://aoc.just2good.co.uk/python/images


from io import BytesIO
from pathlib import Path

import imageio as iio
import numpy as np
import rich
from matplotlib import image as plt_img
from matplotlib import pyplot as plt
from PIL import Image
from rich.rule import Rule

rich.print(Rule("Begin"))
# script_dir = Path.cwd()
script_directory = Path(__file__).parent if "__file__" in globals() else Path.cwd()

print(f"{script_directory=}")

# Define output_dir as script_directory / "output"
output_dir = script_directory / "output"

# Create the directory if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)
print(output_dir.name)

img_file = script_directory / "baseball.jpeg"
img_file_seattle = script_directory / "427 Seattle_120617_153.jpg"

# Loading and Showing Image File with Pillow
print("Loading image with PIL...")
pil_image = Image.open(img_file)
pil_image_seattle = Image.open(img_file_seattle)


def image_info(pil_img):
    print(f"Type: {type(pil_img)}")
    print(f"Size: {pil_img.size}")
    print(f"Format: {pil_img.format}")
    print(f"Mode: {pil_img.mode}")
    pil_img.show("Pillow Image")  # show the image


image_info(pil_image)
image_info(pil_image_seattle)


# Loading and Showing Image File with Matplotlib (NumPy)

print("\nLoading image with matplotlib...")
py_img = plt_img.imread(img_file)
print(f"Type: {type(py_img)}")
print(f"Dtype: {py_img.dtype}")
print(f"Shape: {py_img.shape}")
plt.axis("off")
plt.imshow(py_img)  # attach the image to the plot
plt.show()  # show the image

# Converting from Pillow to NumPy
print("\nConverting from NumPy ndarray to Pillow...")
from_numpy_to_pillow = Image.fromarray(py_img)
print(f"Type: {type(from_numpy_to_pillow)}")
print(f"Size: {from_numpy_to_pillow.size}")
print(f"Format: {from_numpy_to_pillow.format}")
print(f"Mode: {from_numpy_to_pillow.mode}")
from_numpy_to_pillow.show("From NumPy to Pillow")

# Converting from Matplotlib to BytesIO

print(f"Source type: {type(py_img)}")
frame = BytesIO()
plt.imshow(py_img)  # load the image into Plt
plt.savefig(frame, format="png")  # save the image to (BytesIO) memory
plt.savefig(Path(output_dir, "pyplot_img_file.png"))  # save to disk

# Converting from BytesIO to Pillow

print("\nReading BytesIO in Pillow...")
pil_img = Image.open(frame)  # Pillow open seeks for us
pil_img.show()

# From Pillow to Various Formats, Including BytesIO

print("\nOpening image in Pillow and then saving in various formats to")
print(output_dir)
pil_img = Image.open(img_file)
pil_img.save(output_dir / "pil_img_file.jpg")
pil_img.save(output_dir / "pil_img_file.png")
print("And saving directly to BytesIO...")
frame = BytesIO()
pil_img.save(
    frame, format="PNG"
)  # We can save to a file, or to a file-like object, like BytesIO
print("Success.")
