from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image,UnidentifiedImageError
import cv2
image_path=""
message_path=""
def open_img():
    global image_path
    x = openfilename()
    image_path=x
    if x is not None:
        try:
            img = Image.open(x)  
            img = img.resize((250, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            panel = Label(root, image = img)
            panel.image = img
            panel.grid(row = 0,column=3)
            Label(root, text=x).grid(row=0,column=1)
        except UnidentifiedImageError:
            messagebox.showerror("Please Select a Image", "Error")


        
        

def open_mssage():
    global message_path
    file_path = openfilename()
    message_path=file_path
    if file_path is not None:
        f = open(file_path,'r') 
        t=f.read()



        Panel_text = Text(root, height = 5, width = 52)
        Panel_text.grid(row=1, column=3)
        Panel_text.insert(INSERT,chars=t)
        Label(root, text=file_path).grid(row=1,column=1)


def openfilename():
    filename = filedialog.askopenfilename()
    return filename


root=Tk()
root.geometry("1500x1500")
root.resizable(width = True, height = True)
root.title("BPCS Steganography")


Label(root, text='First Name').grid(row=0)
btn = Button(root, text ='open image', command = open_img).grid(
                                        row = 0,column=2)
Label(root,width = 100, height = 4,fg = "blue").grid(column = 4, row = 0)


Label(root, text='Last Name').grid(row=1)
btn = Button(root, text ='open mesage', command = open_mssage).grid(
                                        row = 1,column=2)
Label(root,width = 100, height = 4,fg = "blue").grid(column = 4, row = 1)



label_file_explorer = Label(root,text = "File Explorer using Tkinter",
                                 width = 100, height = 4,fg = "blue").grid(column = 2, row = 4)









button = Button(root, text='Stop', width=25, command=root.destroy).grid(column=1,row=3)

root.mainloop()



