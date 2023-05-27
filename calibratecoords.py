import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
background_image = Image.open("./map/BombsiteB.png")
image_width, image_height = background_image.size
fig = plt.figure(figsize=(image_width / 100, image_height / 100))
ax = plt.axes(frameon=True)
ax.get_xaxis().set_visible(True)
ax.get_yaxis().set_visible(True)

ax.imshow(background_image)

plt.show()
