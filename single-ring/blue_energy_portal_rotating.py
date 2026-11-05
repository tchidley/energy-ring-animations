
from pathlib import Path
from PIL import Image
import cv2
import numpy as np

# VIDEO SETTINGS
INPUT_IMAGE = Path(__file__).with_name("Blue Energy Portal 2.png")
OUTPUT_VIDEO = Path(__file__).with_name("Blue_Energy_Portal_Rotating.mp4")

WIDTH = 1280
HEIGHT = 720
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

# LOAD IMAGE
if not INPUT_IMAGE.exists():
    raise FileNotFoundError("Blue Energy Portal 2.png was not found!")

portal = Image.open(INPUT_IMAGE).convert("RGBA")

# RESIZE IMAGE
portal.thumbnail((620, 620), Image.Resampling.LANCZOS)

# CENTER IMAGE
canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))

x = (WIDTH - portal.width) // 2
y = (HEIGHT - portal.height) // 2

canvas.alpha_composite(portal, (x, y))

# CREATE MP4 VIDEO
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

video = cv2.VideoWriter(
    str(OUTPUT_VIDEO),
    fourcc,
    FPS,
    (WIDTH, HEIGHT)
)

if not video.isOpened():
    raise RuntimeError("Could not create MP4 video.")

# ROTATION ANIMATION
try:
    for i in range(TOTAL_FRAMES):

        angle = -1080 * i / TOTAL_FRAMES

        rotated = canvas.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            expand=False
        )

        # BLACK BACKGROUND
        background = Image.new(
            "RGBA",
            (WIDTH, HEIGHT),
            (0, 0, 0, 255)
        )

        background.alpha_composite(rotated)

        # CONVERT TO VIDEO FRAME
        frame = cv2.cvtColor(
            np.array(background.convert("RGB")),
            cv2.COLOR_RGB2BGR
        )

        video.write(frame)

        if (i + 1) % 30 == 0:
            print(f"Rendering: {i + 1}/{TOTAL_FRAMES}")

finally:
    video.release()

print("VIDEO COMPLETED!")
print(f"Saved to: {OUTPUT_VIDEO}")
