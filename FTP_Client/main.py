from ftplib import FTP
import os # allows me to use os.chdir
import time
import cv2
import msvcrt as m

ftp_ip="192.168.0.1"
ftp_login='anonymous'

abs_path = "C:/Users/Therkelsen/Documents/GitHub/Trash_Sorting_Robot/Data/Images/RGB/"

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
        crop_img = img[140:height, 270:width-20]
        cv2.waitKey(0)
        cv2.imwrite(img_path, crop_img)
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