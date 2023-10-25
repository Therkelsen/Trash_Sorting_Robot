from ftplib import FTP
import os # allows me to use os.chdir
import time
import cv2
import msvcrt as m
from roboflow import Roboflow
import tempfile

ftp_ip="192.168.0.1"
ftp_login='anonymous'

abs_path = "C:/Users/Therkelsen/Documents/GitHub/Trash_Sorting_Robot/Data/Images/RGB/"

rf = Roboflow(api_key="e6vqYw2hVrLBzvqxJoQc")
project = rf.workspace().project("taco-trash-annotations-in-context")
model = project.version(16).model

def setup_ftp(ip, login, path):
    os.chdir(path)
    ftp = FTP(ip)
    ftp.login(login,"")
    return ftp
    
def fetch_image(ftp):
    try:
        num_elems = len([name for name in os.listdir(abs_path) if os.path.isfile(os.path.join(abs_path, name))])
        img_path = abs_path + "rgb_" + str(num_elems) +".png"
        with open(img_path, 'wb') as localfile:
            ftp.retrbinary('RETR ' + "/private/rgb_2.png", localfile.write)
        img = cv2.imread(img_path)
        height, width = img.shape[:2]
        crop_img = img[150:height+5, 270:width-20]
        cv2.imwrite(img_path, crop_img)
        
        # getting prediction
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            cv2.imwrite(temp_file.name, crop_img)
            
            
            # plain img result
            print("1. Printing img with bounding lines")
            model.predict(temp_file.name).save("bounding_lines.jpg")
            
            print("2. Printing cropped images")
            predictions_data = model.predict(temp_file.name).json()
            image = cv2.imread(temp_file.name)
            for index, prediction in enumerate(predictions_data['predictions']):
                x, y, width, height = int(prediction['x']), int(prediction['y']), int(prediction['width']), int(prediction['height'])
                
                # Crop the area based on bounding box coordinates
                roi_x = int(prediction['x'] - prediction['width'] / 2)
                roi_y = int(prediction['y'] - prediction['height'] / 2)
                roi_width = int(prediction['width'])
                roi_height = int(prediction['height'])
                
                cropped_area = image[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
                
                # Save the cropped area
                cv2.imwrite(f'cropped_object_{index}.png', cropped_area)
                
                relative_x = x - roi_x
                relative_y = y - roi_y
                cv2.circle(cropped_area, (relative_x, relative_y), 5, (0, 0, 255), -1)  # Radius=5, Color=Green, Thickness=-1 (filled)
                
                # Draw coordinates above the circle
                font = cv2.FONT_HERSHEY_SIMPLEX
                text = f"({relative_x}, {relative_y})"
                text_size = cv2.getTextSize(text, font, 0.5, 1)[0]
                text_x = relative_x - text_size[0] // 2
                text_y = relative_y - 10  # 10 pixels above the circle
                cv2.putText(cropped_area, text, (text_x, text_y), font, 0.5, (0, 0, 255), 1)

                
                # Save the cropped area with the circle
                cv2.imwrite(f'cropped_object_with_circle_{index}.png', cropped_area)
    
        
        print("Saved image: rgb_" + str(num_elems) +".png")
    except:
        print("Could not get file from FTP server, try again")
        os.remove(img_path)

def wait_for_keypress():
    print("Press enter to snap a new picture\nOr c to exit")
    while True:
        char = m.getch()
        if char == b'\r':
            return "enter"
        if char == b'c':
            return "c"

if __name__ == "__main__":
    ftp = setup_ftp(ftp_ip, ftp_login, abs_path)
    while True:
        keypress = wait_for_keypress()
        if keypress == "enter":
            fetch_image(ftp)
        elif keypress == "c":
            quit()