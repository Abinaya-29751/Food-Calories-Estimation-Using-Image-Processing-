import cv2
import numpy as np

# Density - gram / cm^3
density_dict = {1: 0.609, 2: 0.94, 3: 0.641, 4: 0.641, 5: 0.513, 6: 0.482, 7: 0.481}

# Kcal
calorie_dict = {1: 52, 2: 89, 3: 41, 4: 16, 5: 40, 6: 47, 7: 18}

# Skin of photo to real multiplier
skin_multiplier = 5 * 2.3

def getCalorie(label, volume):  # Volume in cm^3
    calorie = calorie_dict[int(label)]
    density = density_dict[int(label)]
    mass = volume * density * 1.0
    calorie_tot = (calorie / 100.0) * mass
    return mass, calorie_tot, calorie  # Calorie per 100 grams

def getVolume(label, area, skin_area, pix_to_cm_multiplier, fruit_contour):
    area_fruit = (area / skin_area) * skin_multiplier  # Area in cm^2
    label = int(label)
    volume = 100
    if label in [1, 5, 7, 6]:  # Sphere: apple, tomato, orange, kiwi, onion
        radius = np.sqrt(area_fruit / np.pi)
        volume = (4 / 3) * np.pi * radius * radius * radius

    if label in [2, 4] or (label == 3 and area_fruit > 30):  # Cylinder: banana, cucumber, carrot
        fruit_rect = cv2.minAreaRect(fruit_contour)
        height = max(fruit_rect[1]) * pix_to_cm_multiplier
        radius = area_fruit / (2.0 * height)
        volume = np.pi * radius * radius * height

    if label == 4 and area_fruit < 30:  # Carrot
        volume = area_fruit * 0.5  # Assuming width = 0.5 cm

    return volume

def getAreaOfFood(img_path):
    img = cv2.imread(img_path)

    # Convert the image to grayscale for better processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get a binary mask
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Find contours in the binary mask
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the largest contour corresponds to the fruit
    largest_contour = max(contours, key=cv2.contourArea)

    # Calculate area and other parameters
    fruit_area = cv2.contourArea(largest_contour)
    final_fruit_area = fruit_area * 1.5  # Just for demonstration, replace with actual logic
    area_of_dish = 200  # Just for demonstration, replace with actual logic
    skin_area = 150  # Just for demonstration, replace with actual logic
    pix_to_cm_multiplier = 0.1  # Just for demonstration, replace with actual logic

    return final_fruit_area, final_fruit_area, area_of_dish, skin_area, largest_contour, pix_to_cm_multiplier

def calories(result, img_path):
    fruit_areas, areaod, skin_areas, fruit_contours, pix_cm = getAreaOfFood(img_path)

    # Print intermediate values for debugging
    print("Fruit Areas:", fruit_areas)
    print("Skin Areas:", skin_areas)
    print("Pix to CM Multiplier:", pix_cm)

    volume = getVolume(result, fruit_areas, skin_areas, pix_cm, fruit_contours)
    mass, cal, cal_100 = getCalorie(result, volume)

    # Print the calculated values for debugging
    print("Volume:", volume)
    print("Mass:", mass)
    print("Calories:", cal)

    return cal

if __name__ == '__main__':
    img_path = r'C:\Users\HP\Downloads\apple.jpg'
    img = cv2.imread(img_path)

    # Display the image using OpenCV (assuming it's in BGR format)
    cv2.imshow('Input Image', img)
    cv2.waitKey(5000)  # Display for 5 seconds
    cv2.destroyAllWindows()

    # Perform your calculations and get the result
    result = calories(1, img_path)  # Use an actual label instead of '1' if needed

    # Print the result or use it as needed
    print(f"Fruit calories: {result}")
