from image import Image
from processing import Processing

images = ["images/8.jpg","images/17.jpg", "images/18.jpg", "images/12.jpg"]

def process_images():
	for img in images:
		img = Image(img, 1)
		processing = Processing(img)
		processing.get_domino_points()	

if __name__ == '__main__':
	process_images()