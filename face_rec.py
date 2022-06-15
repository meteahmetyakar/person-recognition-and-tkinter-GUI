import face_recognition as fr
import os
import cv2

import numpy as np
import sqlite3 as sql

import datetime

import shutil

import tkinter as tk

from PIL import Image, ImageTk


def setName(name): #delete numbers on given name variable
    name = name.replace("_"," ")
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    for x in name:
        if x in numbers:
            name = name.replace(x,"")
            
    return name.strip()


def get_encoded_faces():

    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"): #We use it to navigate through all the folders in the file we want.
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"): #taking jpg or png files
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    return encoded


def classify_face(im, faces):

    ## taking datas from faces
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    ## reading image
    img = cv2.imread(im, 1)
    
    ## finding face on image
    face_locations = fr.face_locations(img)
    unknown_face_encodings = fr.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # comparing given faces and image
        matches = fr.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        face_distances = fr.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)

        # if face has find in faces, taking name
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    if len(face_names) == 0:
        return ["No Face"]
    else:            
        return face_names 


def take_photo():
    image = Image.fromarray(img1)
    image.save("test.jpg")
    global isContinue
    isContinue = False
    

def train_person():
    ### Database and image recording processes

    nameText = str(isim.get(1.0,"end-1c"))
    surnameText = str(soyisim.get(1.0,"end-1c"))
    gmailText = str(gmail.get(1.0,"end-1c"))
    
    db = sql.connect('persons')
    cursor = db.cursor()
    
    if len(cursor.execute("SELECT * FROM persons WHERE name = ? AND surname = ?", (nameText,surnameText)).fetchall()) == 0:
        cursor.execute("CREATE TABLE IF NOT EXISTS persons (name, surname, mail)")
        cursor.execute("INSERT INTO kisiler VALUES(?,?,?)", (nameText,surnameText,gmailText))   

    fileName = str(nameText+"_"+surnameText+"_"+str(datetime.datetime.now().today()).replace(" ", "").replace("-", "").replace(":","").replace(".", "")+".jpg")
    
    shutil.copy('test.jpg', 'D:\Mete\Software\projects\my projects\face_rec/faces/'+str(fileName))
    
    db.commit()
    db.close()
    root.destroy()
    
def print_person_data(name, surname):
    ### printing given person datas to labels
    db = sql.connect('persons')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM persons WHERE name = ? AND surname = ?", (name, surname))   
    
    
    person_data = cursor.fetchone()

    tk.Label(root, text="NAME: "+person_data[0], font = 'Helvetica 10 normal').pack()    
    tk.Label(root, text="SURNAME: "+person_data[1], font = 'Helvetica 10 normal').pack()   
    tk.Label(root, text="MAIL: "+person_data[2], font = 'Helvetica 10 normal').pack()

    tk.Button(root, text ="Exit",font= 'Helvetica 15 bold', command = exit_program).pack(side = "bottom")

    root.mainloop()
    
    
def exit_program():
    root.destroy()
    
    


faces = get_encoded_faces() #getting faces from file

isContinue = True

### GUI initializing start for take a photo window
root = tk.Tk()
root.geometry("700x640")
tk.Label(root, text = "Please introduce face.", font=("times new roman", 30,"bold")).pack()

f1=tk.LabelFrame(root).pack()

L1 = tk.Label(f1, bg="red")
L1.pack()
cap = cv2.VideoCapture(0)

b = tk.Button(root, text="Take a photo", font=("times new roman",20,"bold"), command = take_photo)
b.pack()
### GUI initializing end

while isContinue: #continue until taking a photo
    img = cap.read()[1]
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img1))
    L1["image"] = img
    
    root.update()
   
cap.release()
root.destroy()

if not len(faces) == 0: # comparing taken photo and photos in file
    name = setName(classify_face("test.jpg", faces)[0])
else:
    name = "Unknown"

if name == "Unknown": #if person unknown, it registering
    root = tk.Tk()

    tk.Label(root, text = "Person Not Recognized Please Register", font = 'Helvetica 15 bold').pack()   

    img = Image.open("test.jpg")
    resized = img.resize((350,320), Image.ANTIALIAS)
    
    new_pic = ImageTk.PhotoImage(resized)
    
    my_label = tk.Label(root,image=new_pic)
    my_label.pack(pady=20, side="left")
    
    
    
    tk.Label(root,text="Name").pack(side = "top")
    isim = tk.Text(root, width = 15, height = 1)
    isim.pack(side="top")
    
    tk.Label(root,text="Surname").pack(side = "top")
    soyisim = tk.Text(root, width = 15, height = 1)
    soyisim.pack(side="top")
    
    tk.Label(root,text="Gmail").pack(side = "top")
    gmail = tk.Text(root, width = 15, height = 1)
    gmail.pack(side="top")
    
    b = tk.Button(root, text="Recognise", font= 'Helvetica 15 bold', command = train_person)
    b.pack()
    
    root.mainloop()
    
elif name == "No Face": #if no face found in the photograph taken
    root = tk.Tk()
    tk.Label(root, text="No Face Found in the Photograph Taken", font= 'Helvetica 25 bold').pack()
    
    root.mainloop()
    
else: #if person is known printing to window
    root = tk.Tk()
    personName = name.split(" ")
    
    img = Image.open("test.jpg")
    resized = img.resize((350,320), Image.ANTIALIAS)
    
    new_pic = ImageTk.PhotoImage(resized)
    
    my_label = tk.Label(root,image=new_pic)
    my_label.pack(pady=20, side="left")

    print_person_data(personName[0], personName[1])
    
    
    
    
    
    
    
    
    






