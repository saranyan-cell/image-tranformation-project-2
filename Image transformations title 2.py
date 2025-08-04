import cv2
import numpy as np
image = cv2.imread('sample.jpg')
if image is None:
    print("Image not found!")
    exit()
original = image.copy()

drawing = False
ix, iy = -1, -1
shape = 'rectangle'

def draw_shape(event, x, y, flags, param):
    global ix, iy, drawing, image, shape

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp = image.copy()
            if shape == 'rectangle':
                cv2.rectangle(temp, (ix, iy), (x, y), (0, 255, 0), 2)
            elif shape == 'circle':
                radius = int(((x - ix) ** 2 + (y - iy) ** 2) ** 0.5)
                cv2.circle(temp, (ix, iy), radius, (255, 0, 0), 2)
            elif shape == 'line':
                cv2.line(temp, (ix, iy), (x, y), (0, 0, 255), 2)
            cv2.imshow('Image Editor', temp)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if shape == 'rectangle':
            cv2.rectangle(image, (ix, iy), (x, y), (0, 255, 0), 2)
        elif shape == 'circle':
            radius = int(((x - ix) ** 2 + (y - iy) ** 2) ** 0.5)
            cv2.circle(image, (ix, iy), radius, (255, 0, 0), 2)
        elif shape == 'line':
            cv2.line(image, (ix, iy), (x, y), (0, 0, 255), 2)

cv2.namedWindow('Image Editor')
cv2.setMouseCallback('Image Editor', draw_shape)

print("""
[Instructions]
t - Rotate 90 degrees
r - Resize to half
g - Grayscale filter
b - Blur filter
e - Edge detection
1 - Draw Rectangle
2 - Draw Circle
3 - Draw Line
s - Save image
c - Reset to original
q - Quit
""")

while True:
    cv2.imshow('Image Editor', image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('t'):
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    elif key == ord('r'):
        h, w = image.shape[:2]
        image = cv2.resize(image, (w // 2, h // 2))

    elif key == ord('g'):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    elif key == ord('b'):
        image = cv2.GaussianBlur(image, (7, 7), 0)

    elif key == ord('e'):
        edges = cv2.Canny(image, 100, 200)
        image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif key == ord('1'):
        shape = 'rectangle'
        print("Drawing: Rectangle")

    elif key == ord('2'):
        shape = 'circle'
        print("Drawing: Circle")

    elif key == ord('3'):
        shape = 'line'
        print("Drawing: Line")

    elif key == ord('s'):
        cv2.imwrite('edited_image.jpg', image)
        print("Image saved as 'edited_image.jpg'")

    elif key == ord('c'):
        image = original.copy()
        print("Image reset to original.")

    elif key == ord('q'):
        break

cv2.destroyAllWindows()
