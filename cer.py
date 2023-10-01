from tkinter.filedialog import askopenfilename, askdirectory
from PIL import ImageTk, Image, ImageFont, ImageDraw
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from CTkColorPicker import *
from email import encoders
from pathlib import Path
import urllib.request
import customtkinter
import pandas as pd
import webbrowser
import functools
import threading
import smtplib
import tkinter
import json
import time
import io
import re

def drag_start(event):
    global crosshair1_coords, crosshair2_coords, crosshair1x, crosshair1y, crosshair2x, crosshair2y
    tags = canvas.gettags(tkinter.CURRENT)
    if ('crosshair1' in tags):
        print('Crosshair1 clicked at:', event.x, event.y)
        if ((crosshair2_coords['x']-10)<event.x):
            crosshair1_coords['x'] = (crosshair2_coords['x']-10)
        elif (event.x<(image_coords[0]-5)):
            crosshair1_coords['x'] = (image_coords[0]-5)
        else:
            crosshair1_coords['x'] = event.x
        if ((crosshair2_coords['y']-10)<event.y):
            crosshair1_coords['y'] = (crosshair2_coords['y']-10)
        elif (event.y<(image_coords[1]-2)):
            crosshair1_coords['y'] = (image_coords[1]-2)
        else:
            crosshair1_coords['y'] = event.y
    elif ('crosshair2' in tags):
        print('Crosshair2 clicked at:', event.x, event.y)
        if ((event.x<crosshair1_coords['x']+10)):
            crosshair2_coords['x'] = (crosshair1_coords['x']+10)
        elif ((image_coords[2]-5)<event.x):
            crosshair2_coords['x'] = (image_coords[2]-5)
        else:
            crosshair2_coords['x'] = event.x
        if ((crosshair1_coords['y']+10)<event.y):
            crosshair2_coords['y'] = (crosshair1_coords['y']+10)
        elif (event.y<(image_coords[3]-2)):
            crosshair2_coords['y'] = (image_coords[3]-2)
        else:
            crosshair2_coords['y'] = event.y


def drag_motion(event):
    global crosshair1_coords, crosshair2_coords, crosshair1x, crosshair1y, crosshair2x, crosshair2y, image_coords
    tags = canvas.gettags(tkinter.CURRENT)
    # Calculate the difference in mouse position since the last motion event
    if ('crosshair1' in tags):
        print('crosshair1 dragged')
        if ((crosshair2_coords['x']-10)<event.x):
            crosshair1_coords['x'] = (crosshair2_coords['x']-10)
        elif (event.x<(image_coords[0]-5)):
            crosshair1_coords['x'] = (image_coords[0]-5)
        else:
            crosshair1_coords['x'] = event.x
        if ((crosshair2_coords['y']-10)<event.y):
            crosshair1_coords['y'] = (crosshair2_coords['y']-10)
        elif (event.y<(image_coords[1]-2)):
            crosshair1_coords['y'] = (image_coords[1]-2)
        else:
            crosshair1_coords['y'] = event.y
        canvas.coords(crosshair1x,0,crosshair1_coords['y'],int(canvas.winfo_width()),crosshair1_coords['y'])
        canvas.coords(crosshair1y,crosshair1_coords['x'], 0, crosshair1_coords['x'], int(canvas.winfo_height()))
        canvas.coords(tkinter.CURRENT, crosshair1_coords['x']-5, crosshair1_coords['y']-5, crosshair1_coords['x']+5, crosshair1_coords['y']+5)

    elif ('crosshair2' in tags):
        print('crosshair2 dragged')
        if (event.x<(crosshair1_coords['x']+10)):
            crosshair2_coords['x'] = (crosshair1_coords['x']+10)
        elif ((image_coords[2]-5)<event.x):
            crosshair2_coords['x'] = (image_coords[2]-5)
        else:
            crosshair2_coords['x'] = event.x
        if (event.y<(crosshair1_coords['y']+10)):
            crosshair2_coords['y'] = (crosshair1_coords['y']+10)
        elif ((image_coords[3]-2)<event.y):
            crosshair2_coords['y'] = (image_coords[3]-2)
        else:
            crosshair2_coords['y'] = event.y
        canvas.coords(crosshair2x,0,crosshair2_coords['y'],int(canvas.winfo_width()),crosshair2_coords['y'])
        canvas.coords(crosshair2y,crosshair2_coords['x'], 0, crosshair2_coords['x'], int(canvas.winfo_height()))
        canvas.coords(tkinter.CURRENT, crosshair2_coords['x']-5, crosshair2_coords['y']-5, crosshair2_coords['x']+5, crosshair2_coords['y']+5)
    
def drag_end(event):
    global crosshair1_coords, crosshair2_coords, image_coords, written
    if written:
        write_on_image(image_coords, crosshair1_coords, crosshair2_coords)


def select_certificate_img():
    global written, filepath, certificate, image_coords, resize_factor, canvasimage, crosshair2_coords, crosshair1_coords
    global crosshair1, crosshair2, crosshair1x, crosshair1y, crosshair2x, crosshair2y
    written = False
    filepath = askopenfilename(filetypes = [
        ('Joint Photographic Experts Group (JPG) files', '.jpg'),
        ('Joint Photographic Experts Group (JPEG) files', '.jpeg'),
        ('Web Picture (WebP) files', '.webp'),
        ('Tag Image File Format (TIF) files', '.tif'),
        ('Tag Image File Format(TIFF) files', '.tiff'),
        ('Bitmap(BMP) files', '.bmp'),
        ('Portable Network Graphics (PNG) files', '.png'),
        ('Scalable Vector Graphics (SVG) files', '.svg')]
    )
    if filepath:
        certificate = Image.open(filepath)
    resize_factor = min(canvas.winfo_width()/certificate.width,canvas.winfo_height()/certificate.height)
    resized_image = certificate.resize((int(certificate.width*resize_factor), int(certificate.height*resize_factor)), Image.Resampling.LANCZOS)
    eimage = ImageTk.PhotoImage(resized_image)
    canvas.image = eimage
    canvasimage = canvas.create_image(canvas.winfo_width()/2,canvas.winfo_height()/2, image = eimage, anchor = "center")
    mainnav.configure(fg_color = "transparent")
    image_coords = canvas.coords(canvasimage)
    image_coords.append(image_coords[0] - int(certificate.width*resize_factor)/2+5)
    image_coords.append(image_coords[1] - int(certificate.height*resize_factor)/2+2)
    image_coords.pop(0)
    image_coords.pop(0)
    image_coords.append(image_coords[0]+ int(certificate.width*resize_factor))
    image_coords.append(image_coords[1]+ int(certificate.height*resize_factor))
    crosshair1_coords['x'] = int(image_coords[0])-5
    crosshair1_coords['y'] = int(((image_coords[1]+image_coords[3])/2)-((image_coords[3]-image_coords[1])/10))-2
    crosshair2_coords['x'] = int(image_coords[2])-5
    crosshair2_coords['y'] = int(((image_coords[1]+image_coords[3])/2)+((image_coords[3]-image_coords[1])/10))-2
    canvas.coords(crosshair1x,0,crosshair1_coords['y'],int(canvas.winfo_width()),crosshair1_coords['y'])
    canvas.coords(crosshair1y,crosshair1_coords['x'], 0, crosshair1_coords['x'], int(canvas.winfo_height()))
    canvas.coords(crosshair1, crosshair1_coords['x']-5, crosshair1_coords['y']-5, crosshair1_coords['x']+5, crosshair1_coords['y']+5)
    canvas.coords(crosshair2x,0,crosshair2_coords['y'],int(canvas.winfo_width()),crosshair2_coords['y'])
    canvas.coords(crosshair2y,crosshair2_coords['x'], 0, crosshair2_coords['x'], int(canvas.winfo_height()))
    canvas.coords(crosshair2, crosshair2_coords['x']-5, crosshair2_coords['y']-5, crosshair2_coords['x']+5, crosshair2_coords['y']+5)
    canvas.tag_raise(canvasimage)
    canvas.tag_raise(crosshair1x)
    canvas.tag_raise(crosshair2x)
    canvas.tag_raise(crosshair1y)
    canvas.tag_raise(crosshair2y)
    canvas.tag_raise(crosshair1)
    canvas.tag_raise(crosshair2)
    print("Image coordinates:", image_coords, "Crosshair1:", canvas.coords(crosshair1), "Crosshair2:", canvas.coords(crosshair2))




def imgResize(event):
    global written, certificate, crosshair1, crosshair2, crosshair1x, crosshair1y, crosshair2x, crosshair2y, image_coords, resize_factor, canvasimage, crosshair1_coords, crosshair2_coords
    if canvasimage:
        canvas.delete(canvasimage)
    old_factor = resize_factor
    old_image_coords = image_coords
    resize_factor = min(canvas.winfo_width()/certificate.width,canvas.winfo_height()/certificate.height)
    #print(old_factor, resize_factor)
    if written:
        global sub_image
        image_resize = sub_image.resize((int(sub_image.width*resize_factor), int(sub_image.height*resize_factor)), Image.Resampling.LANCZOS)
    else:
        image_resize = certificate.resize((int(certificate.width*resize_factor), int(certificate.height*resize_factor)), Image.Resampling.LANCZOS)

    eimage = ImageTk.PhotoImage(image_resize)
    canvas.image = eimage
    canvasimage = canvas.create_image(canvas.winfo_width()/2,canvas.winfo_height()/2, image = eimage, anchor = "center")
    image_coords = canvas.coords(canvasimage)
    if written:
        image_coords.append(image_coords[0] - int(sub_image.width*resize_factor)/2+5)
        image_coords.append(image_coords[1] - int(sub_image.height*resize_factor)/2+2)
        image_coords.pop(0)
        image_coords.pop(0)
        image_coords.append(image_coords[0]+ int(sub_image.width*resize_factor))
        image_coords.append(image_coords[1]+ int(sub_image.height*resize_factor))
    else:
        image_coords.append(image_coords[0] - int(certificate.width*resize_factor)/2+5)
        image_coords.append(image_coords[1] - int(certificate.height*resize_factor)/2+2)
        image_coords.pop(0)
        image_coords.pop(0)
        image_coords.append(image_coords[0]+ int(certificate.width*resize_factor))
        image_coords.append(image_coords[1]+ int(certificate.height*resize_factor))
    old_center = {'x':int((old_image_coords[0] + old_image_coords[2])/2), 'y':int((old_image_coords[1] + old_image_coords[3])/2)}
    new_center = {'x':int((image_coords[0] + image_coords[2])/2), 'y':int((image_coords[1] + image_coords[3])/2)}
    crosshair1_coords['x'] = new_center['x'] + ((crosshair1_coords['x']+5-old_center['x'])/old_factor)*resize_factor-5
    crosshair1_coords['y'] = new_center['y'] + ((crosshair1_coords['y']+2-old_center['y'])/old_factor)*resize_factor-2
    crosshair2_coords['x'] = new_center['x'] + ((crosshair2_coords['x']+5-old_center['x'])/old_factor)*resize_factor-5
    crosshair2_coords['y'] = new_center['y'] + ((crosshair2_coords['y']+2-old_center['y'])/old_factor)*resize_factor-2
    canvas.coords(crosshair1x,0,crosshair1_coords['y'],int(canvas.winfo_width()),crosshair1_coords['y'])
    canvas.coords(crosshair1y,crosshair1_coords['x'], 0, crosshair1_coords['x'], int(canvas.winfo_height()))
    canvas.coords(crosshair1, crosshair1_coords['x']-5, crosshair1_coords['y']-5, crosshair1_coords['x']+5, crosshair1_coords['y']+5)
    canvas.coords(crosshair2x,0,crosshair2_coords['y'],int(canvas.winfo_width()),crosshair2_coords['y'])
    canvas.coords(crosshair2y,crosshair2_coords['x'], 0, crosshair2_coords['x'], int(canvas.winfo_height()))
    canvas.coords(crosshair2, crosshair2_coords['x']-5, crosshair2_coords['y']-5, crosshair2_coords['x']+5, crosshair2_coords['y']+5)
    canvas.tag_raise(canvasimage)
    canvas.tag_raise(crosshair1x)
    canvas.tag_raise(crosshair2x)
    canvas.tag_raise(crosshair1y)
    canvas.tag_raise(crosshair2y)
    canvas.tag_raise(crosshair1)
    canvas.tag_raise(crosshair2)
    print("resize event")

    print("Image coordinates:", image_coords, "Crosshair1:", canvas.coords(crosshair1), "Crosshair2:", canvas.coords(crosshair2))

def on_configure(event):
    if hasattr(canvas, "resize_id"):
        canvas.after_cancel(canvas.resize_id)

    canvas.resize_id = canvas.after(1, imgResize, event)

def set_mailList():
    global NameFrame, csv_path, longestname
    csv_path = askopenfilename(filetypes = (
        ('Comma Separated Values files', '.csv'),
        ('Older Excel files', '.xls'),
        ('Excel files', '.xlsx'))
    )
    if csv_path:
        if csv_path.endswith('.csv'):
            NameFrame = pd.read_csv(csv_path)
        elif csv_path.endswith('.xlsx') or csv_path.endswith('.xls'):
            NameFrame = pd.read_excel(csv_path)
        else:
            tkinter.messagebox.showerror('File Format Error', 'Unsupported file format. Please use csv, xlsx or xls')
        NameFrame.columns = NameFrame.columns.str.lower()
        NameFrame = NameFrame.filter(items=['name', 'email'])
        longestname = max(NameFrame['name'], key = len)


def get_font_from_url(font_url_select):
    global font_url, font, longestname, image_coords, crosshair1_coords, crosshair2_coords, font_file, resize_factor, certificate, canvasimage
    font_url = font_url_select
    try:
        font_url_file = urllib.request.urlopen(font_url).read()
    except:
        tkinter.messagebox.showerror('URL Error', 'Error: Invalid URL')
    else:
        font_file = io.BytesIO(font_url_file)
        try:
            font = ImageFont.truetype(font_file, 15)
        except:
            tkinter.messagebox.showerror('Font Error', 'Error: Font not present at URL')
        else:
            write_on_image(image_coords, crosshair1_coords, crosshair2_coords)

def write_on_image(image_coords, crosshair1_coords, crosshair2_coords):
    global font_file, font, certificate, sub_image, canvas, written, canvasimage, font_color
    global crosshair1, crosshair2, crosshair1x, crosshair2x, crosshair1y, crosshair2y
    reresize_factor = max(certificate.width/(image_coords[2]-image_coords[0]),certificate.height/(image_coords[3]-image_coords[1]))
    textbox_coords = [int(reresize_factor*(crosshair1_coords['x']+5-image_coords[0])),
                        int(reresize_factor*(crosshair1_coords['y']+2-image_coords[1])),
                        int(reresize_factor*(crosshair2_coords['x']+5-image_coords[0])),
                        int(reresize_factor*(crosshair2_coords['y']+2-image_coords[1]))]
    print("Textbox coordinates:",textbox_coords,"Image size:", certificate.width, certificate.height)
    print(font_file)
    written = True
    max_font_size = get_max_font_size(textbox_coords)
    print(max_font_size)
    font_file.seek(0)
    font = ImageFont.truetype(font_file,max_font_size)
    sub_image = certificate.copy()
    draw = ImageDraw.Draw(sub_image)
    x = (textbox_coords[2] + textbox_coords[0]) // 2
    y = textbox_coords[3]
    # for center alignment use y = (textbox_coords[3] + textbox_coords[1]) // 2   and anchor="mm"
    # #maybe change to textbox_coords[3] to align with bottom line insidead of box center and anchor="ms"
    draw.text((x, y), longestname, fill = font_color, font = font, anchor = "ms")
    #imagepath = os.path.join(dirname, 'output.jpeg')
    #sub_image.save(imagepath)
    resize_factor = min(canvas.winfo_width()/sub_image.width,canvas.winfo_height()/sub_image.height)
    image_resize = sub_image.resize((int(sub_image.width*resize_factor), int(sub_image.height*resize_factor)), Image.Resampling.LANCZOS)
    eimage = ImageTk.PhotoImage(image_resize)
    canvas.image = eimage
    if canvasimage:
        canvas.delete(canvasimage)
    canvasimage = canvas.create_image(canvas.winfo_width()/2,canvas.winfo_height()/2, image = eimage, anchor = "center")
    canvas.tag_raise(canvasimage)
    canvas.tag_raise(crosshair1x)
    canvas.tag_raise(crosshair2x)
    canvas.tag_raise(crosshair1y)
    canvas.tag_raise(crosshair2y)
    canvas.tag_raise(crosshair1)
    canvas.tag_raise(crosshair2)


def listToTuple(function):
    def wrapper(*args):
        args = [tuple(x) if type(x) == list else x for x in args]
        result = function(*args)
        result = tuple(result) if type(result) == list else result
        return result
    return wrapper

@listToTuple
@functools.lru_cache(maxsize = 10)
def get_max_font_size(textbox_coords):
    global font_file
    min_font_size = 100
    max_font_size = 1000
    print(textbox_coords)
    while min_font_size < max_font_size:
        try:
            font_file.seek(0)
            font = ImageFont.truetype(font_file, max_font_size)
        except:
            tkinter.messagebox.showerror('URL Error', 'Error: Invalid URL2')
            break
        else:
            text_size = font.getbbox(longestname)
            if (text_size[2] - text_size[0] >=  textbox_coords[2] - textbox_coords[0] or
                text_size[3] - text_size[1] >=  textbox_coords[3] - textbox_coords[1]):
                break
            else:
                min_font_size = max_font_size
                max_font_size = max_font_size*4
    
    while min_font_size < max_font_size:
        try:
            font_file.seek(0)
            font = ImageFont.truetype(font_file, min_font_size)
        except:
            tkinter.messagebox.showerror('URL Error', 'Error: Invalid URL2')
            break
        else:
            text_size = font.getbbox(longestname)
            if (text_size[2] - text_size[0] <=  textbox_coords[2] - textbox_coords[0] and
                text_size[3] - text_size[1] <=  textbox_coords[3] - textbox_coords[1]):
                break
            else:
                max_font_size = min_font_size
                min_font_size = min_font_size // 4
    
    while min_font_size < max_font_size:
        font_size = (min_font_size + max_font_size) // 2  # Calculate midpoint
        try:
            font_file.seek(0)
            font = ImageFont.truetype(font_file, font_size)
        except:
            tkinter.messagebox.showerror('URL Error', 'Error: Invalid URL3')
            break
        else:
            text_size = font.getbbox(longestname)
            
            # Check if the text fits within the textbox_coords
            if (text_size[2] - text_size[0] <=  textbox_coords[2] - textbox_coords[0] and
                text_size[3] - text_size[1] <=  textbox_coords[3] - textbox_coords[1]):
                min_font_size = font_size + 1
            else:
                max_font_size = font_size - 1
    return min_font_size

def help():
    helpwindow = customtkinter.CTkToplevel(master = app)
    helpwindow.minsize(750, 550)
    helpwindow.title("Help")
    helpwindow.grid_columnconfigure((0), weight = 1)
    helpwindow.grid_rowconfigure((0), weight = 1)
    HelpScroll = customtkinter.CTkFrame(master = helpwindow, fg_color = "grey30")
    HelpScroll.pack(padx = (5,5), pady = (5,5), side="top", expand=1, fill="both")
    HelpText = tkinter.Text(master = HelpScroll, font = ("",18))
    HelpText.pack(side="top", expand=1, fill="both")
    HelpText.tag_configure("link", foreground="lightblue", underline=True)
    HelpText.tag_bind("link", "<Button-1>", open_link)
    HelpText.insert("1.0", "1) Click on the Import template button and then select the Certificate template that you want to use. The template should be in an commonly used image format.\n \n")
    HelpText.insert("3.0", "2) Click on the Import spreadsheet button and then select the a csv or an excel file that contains atleast two rows, names and email the the list of names and mail that you want to send to.\n \n")
    HelpText.insert("5.0", "3) Import a google font. Go to fonts.google.com and then choose your font. once you have the link open the link in a browser. There will be a list of links for different fonts. Choose the link that is applicable and then ppasted it in the textbox. then click on open.\n \n")
    HelpText.insert("7.0", "4) Adjust the crosshairs so that you form a textbox in the empty space where the name should go. Once you stop dragging and leave the cursor the text will update to show you the longest name with the proper font size to fit there.\n \n")
    HelpText.insert("9.0", "5) Select the Text tab and drag the color on the color wheel to adjust the font color.\n\n")
    HelpText.insert("11.0", "6) Click on send Certificate.\n \n")
    HelpText.insert("13.0", "7) Follow this procedure for the time being to send email through SMTP using this app.\n \n")
    HelpText.insert("15.0", "Setup Gmail to send emails using this app.", "link")
    HelpText.insert("17.0", "\n \n")

    HelpText.insert("end", "The rest of the procedure is explained as you go through them.")
    HelpText.configure(state="disabled")
    Donebutton = customtkinter.CTkButton(master = helpwindow, width = 60, height = 25, text="Cancel", command=lambda: mailing.destroy())
    Donebutton.pack(side = 'right', padx = (5,5), pady = (5,5), anchor='s')


def open_link(event):
    webbrowser.open("https://www.youtube-nocookie.com/embed/g_j6ILT-X0k?start=25&end=166&autoplay=1")

def ask_color():
    global font_color, image_coords, crosshair1_coords, crosshair2_coords, written
    pick_color = AskColor() # open the color picker
    color = pick_color.get() # get the color string
    print(color)
    font_color = color
    if written:
        write_on_image(image_coords, crosshair1_coords, crosshair2_coords)

def color_select(color):
    global font_color, image_coords, crosshair1_coords, crosshair2_coords, written, function_lock
    if not function_lock.locked():
        with function_lock:
            print(color)
            font_color = color
            if written:
                write_on_image(image_coords, crosshair1_coords, crosshair2_coords)

def send_email():
    global mailing, getmail, Back, Next, Cancel
    try:
        for widget in getmail.winfo_children():
            widget.destroy()
        Back.destroy()
    except:
        mailing = customtkinter.CTkToplevel(master = app)
        mailing.title("Mail")
        mailing.minsize(400, 250)
        getmail = customtkinter.CTkFrame(master = mailing, fg_color = "grey30", width=400, height = 250)
        getmail.pack(side = 'top', padx = (10,10), pady = (10,10), fill = "both", expand = 1)

        Next = customtkinter.CTkButton(master = mailing, width = 60, height = 25, text="Next", command=lambda: confirmation(senderemail.get(), senderpassword.get()))
        Next.pack(side = 'right', padx = (5,10), pady = (5,5), anchor='s')
        Cancel = customtkinter.CTkButton(master = mailing, width = 60, height = 25, text="Cancel", command=lambda: mailing.destroy())
        Cancel.pack(side = 'right', padx = (5,5), pady = (5,5), anchor='s')
    else:
        Next.configure(command=lambda: confirmation(senderemail.get(), senderpassword.get()))

    finally:
        emaillabel = customtkinter.CTkLabel(master = getmail, text = "Email")
        emaillabel.pack(side = 'top', padx = (5,5), pady = (5,0), anchor="w")
        senderemail = customtkinter.CTkEntry(master = getmail, placeholder_text = "Email")
        senderemail.pack(side = 'top', padx = (5,5), pady = (0,5), fill="x", anchor="e")
        passwordlabel = customtkinter.CTkLabel(master = getmail, text = "Password")
        passwordlabel.pack(side = 'top', padx = (5,5), pady = (5,0), anchor="w")
        senderpassword = customtkinter.CTkEntry(master = getmail, placeholder_text = "Password")
        senderpassword.pack(side = 'top', padx = (5,5), pady = (0,5), fill="x", anchor="e")
        try:
            user_credentials_filepath = Path(__file__).parent / "preload" / 'user_credentials.json'
            with open(user_credentials_filepath, 'r') as user_credential_file:
                user_credentials = json.load(user_credential_file)
                sender_email = user_credentials["email"]
                sender_password = user_credentials["password"]
                senderemail.insert(0, sender_email)
                senderpassword.insert(0, sender_password)
        except:
            print("except loop")

        mailavailability = customtkinter.CTkLabel(master = getmail, text = "*Currently only gmail is supported", text_color="grey")
        mailavailability.pack(side = 'top', padx = (5,5), pady = (5,0), anchor="w")

def confirmation(senderemail, senderpassword):
    global mailing, getmail, Next, Cancel, Back
    emailpattern = r'^[\w\.-]+@[\w\.-]+\.\w+'
    if re.match(emailpattern, senderemail):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        try:
            server.login(senderemail,senderpassword)
        except smtplib.SMTPAuthenticationError:
            tkinter.messagebox.showerror('Login Error', 'Check if email or password is entered incorrectly.')
        else:
            server.quit()
            user_credentials_filepath = Path(__file__).parent / "preload" / 'user_credentials.json'
            user_credentials = {
                "email": senderemail,
                "password": senderpassword
            }

            # Write user credentials to the JSON file
            with open(user_credentials_filepath, 'w') as file:
                json.dump(user_credentials, file)
            for widget in getmail.winfo_children():
                widget.destroy()
            emaillabel = customtkinter.CTkLabel(master = getmail, text = f"Your Email is\n{senderemail}")
            emaillabel.pack(side = 'top', padx = (5,5), pady = (5,0))
            passwordlabel = customtkinter.CTkLabel(master = getmail, text = f"Your Password is\n{senderpassword}")
            passwordlabel.pack(side = 'top', padx = (5,5), pady = (5,0))
            Next.configure(command=savelocation)
            try:
                Back.configure(command=send_email)
            except:
                Back = customtkinter.CTkButton(master = mailing, width = 60, height = 25, text="Back", command=send_email)
                Back.pack(side = 'left', padx = (5,10), pady = (5,5), anchor='s')
    else:
        tkinter.messagebox.showerror('Invalid Email', 'Check if email is entered incorrectly.')
        
def select_directory():
    global file_directory_var
    directory = askdirectory()
    if directory:
        file_directory_var.set(directory)
        Next.configure(state = "normal")


def edit_path(state):
    global file_directory_var, Next
    if state == "Yes":
        select_directory_button.configure(state='normal')
        if file_directory_var==customtkinter.StringVar():
            Next.configure(state = "normal")
        else:
            Next.configure(state = "disabled")
    else:
        select_directory_button.configure(state='disabled')
        Next.configure(state = "normal")



def savelocation():
    global mailing, getmail, Next, Cancel, Back, select_directory_button, file_directory_var
    for widget in getmail.winfo_children():
        widget.destroy()
    user_credentials_filepath = Path(__file__).parent / "preload" / 'user_credentials.json'
    with open(user_credentials_filepath, 'r') as user_credential_file:
        user_credentials = json.load(user_credential_file)
        Back.configure(command=lambda: confirmation(user_credentials["email"],user_credentials["password"]))
    Next.configure(command=lambda: sending(save_file.get()))
    save_file = customtkinter.StringVar(value="No")
    save_file_checkbox = customtkinter.CTkCheckBox(master = getmail, text="do you want to create a copy of the certificates locally as well?",
                                                   variable = save_file, onvalue = "Yes", offvalue = "No", command = lambda:edit_path(save_file.get()))
    save_file_checkbox.pack(side = 'top', padx = (5,5), pady = (5,0))  
    file_directory_var = customtkinter.StringVar()
    file_directory_entry = customtkinter.CTkEntry(master=getmail, state='disabled', textvariable=file_directory_var)
    file_directory_entry.pack(side='top', padx=(5, 5), pady=(0, 5))

    select_directory_button = customtkinter.CTkButton(
        master=getmail, text="Select Directory", command=select_directory, state = 'disabled')
    select_directory_button.pack(side='top', padx=(5, 5), pady=(0, 5))
            

def sending(save_file):
    global mailing, getmail, Next, Cancel, Back, crosshair1_coords, crosshair2_coords, font_color, file_directory_var
    for widget in getmail.winfo_children():
        widget.destroy()
    Back.destroy()
    Next.destroy()
    Cancel.destroy()
    Canvas = tkinter.Canvas(master = getmail)
    Canvas.pack(padx = (5,5), pady = (10,5), side = 'top', fill = "both", expand = 1)
    Canvasimage=None
    reresize_factor = max(certificate.width/(image_coords[2]-image_coords[0]),certificate.height/(image_coords[3]-image_coords[1]))
    textbox_coords = [int(reresize_factor*(crosshair1_coords['x']+5-image_coords[0])),
                        int(reresize_factor*(crosshair1_coords['y']+2-image_coords[1])),
                        int(reresize_factor*(crosshair2_coords['x']+5-image_coords[0])),
                        int(reresize_factor*(crosshair2_coords['y']+2-image_coords[1]))]
    print("Textbox coordinates:",textbox_coords,"Image size:", certificate.width, certificate.height)
    max_font_size = get_max_font_size(textbox_coords)
    font_file.seek(0)
    font = ImageFont.truetype(font_file,max_font_size)
    progressbar = customtkinter.CTkProgressBar(master = getmail, orientation="horizontal", determinate_speed=len(NameFrame)/0.02, border_color = "gray1")
    progressbar.pack(padx = (10,10), pady = (10,5), side = 'bottom', fill = "x")
    progressbar.set(0)
    print(progressbar.get())
    user_credentials_filepath = Path(__file__).parent / "preload" / 'user_credentials.json'
    with open(user_credentials_filepath, 'r') as user_credential_file:
        user_credentials = json.load(user_credential_file)
        sender_email = user_credentials["email"]
        sender_password = user_credentials["password"]

    for index, row in NameFrame.iterrows():
        getmail.update_idletasks() 
        name = row['name']
        email = row['email']
        sub_image = certificate.copy()
        sub_image = sub_image.convert("RGB")#JPEG does not allow RGBA so convert to RGB
        draw = ImageDraw.Draw(sub_image)
        x = (textbox_coords[2] + textbox_coords[0]) // 2
        y = textbox_coords[3]
        draw.text((x, y), name, fill = font_color, font = font, anchor = "ms")


        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = 'Certificate'

        # Add text to your email
        body = "Please find your participation certificate attached."
        msg.attach(MIMEText(body, 'plain'))
        if save_file=="Yes":
            sub_image.save(Path(file_directory_var.get()) / "preload" / f"{email}.jpg", 'JPEG')
            with open(Path(file_directory_var.get()) / "preload" / f"{email}.jpg", 'rb') as stream:
                NamedCert = stream.read()
                image = MIMEImage(NamedCert)
            image.add_header('Content-Disposition', 'attachment', filename='Certificate.jpg')
            msg.attach(image)
        else:
            stream = io.BytesIO()
            sub_image.save(stream, format="JPEG")
            stream.seek(0)
            NamedCert = stream.read()
            attachment = MIMEImage(NamedCert)
            attachment.add_header('Content-Disposition', 'attachment', filename='your_image.jpg')
            msg.attach(attachment)

        resize_factor = min(Canvas.winfo_width()/sub_image.width,Canvas.winfo_height()/sub_image.height)
        image_resize = sub_image.resize((int(sub_image.width*resize_factor), int(sub_image.height*resize_factor)), Image.Resampling.LANCZOS)
        eimage = ImageTk.PhotoImage(image_resize)
        Canvas.image = eimage
        if Canvasimage:
            Canvas.delete(Canvasimage)
        Canvasimage = Canvas.create_image(Canvas.winfo_width()/2,Canvas.winfo_height()/2, image = eimage, anchor = "center")
        print(progressbar.cget("determinate_speed"))
        progressbar.step()
        print(progressbar.get())
        try:
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            text = msg.as_string()
            smtp_server.sendmail(sender_email, email, text)
            smtp_server.quit()
            print('Email sent successfully!')
        except Exception as e:
            print('Error sending email:', str(e))

    Done = customtkinter.CTkButton(master = mailing, width = 60, height = 25, text="Done", command=lambda: mailing.destroy())
    Done.pack(side = 'right', padx = (5,5), pady = (5,5), anchor='s')



if __name__  ==  "__main__":
    #predefined datas
    dirname = Path(__file__).parent
    #print(dirname)
    filepath = dirname /  "preload" / 'codechefXvitcc.png'
    #print(filepath)
    certificate = Image.open(filepath)
    csv_path = dirname / "preload" / 'email.csv'
    NameFrame = pd.read_csv(csv_path)
    NameFrame.columns = NameFrame.columns.str.lower()
    NameFrame = NameFrame.filter(items=['name', 'email'])
    font_url = dirname / "preload" / 'Roboto.woff'
    #print(font_url)
    font_url_file = urllib.request.urlopen("file://"+str(font_url)).read()
    font_file = io.BytesIO(font_url_file)
    font = ImageFont.truetype(font_file, 15)
    image_coords = [0,0,100,100]
    resize_factor = 1
    canvasimage = None
    longestname = max(NameFrame['name'], key = len)
    written  = False
    font_color = (0, 0, 0)  # RGB color tuple


    app = customtkinter.CTk()
    app_image = dirname /  "preload" / 'CertSmith icon type 2 iter 4.png'
    photo = tkinter.PhotoImage(file = app_image)
    app.wm_iconphoto(False, photo)
    app.title("CertSmith")
    app.minsize(600,400)
    app.geometry("600x400")

    mainframe = customtkinter.CTkFrame(master = app, fg_color="transparent")
    mainframe.pack(padx = (10,5), pady = (10,10), side = 'left', fill = "both", expand = 1)
    mainframe.grid_columnconfigure((0), weight = 1)
    mainframe.grid_rowconfigure((0), weight = 10)
    #mainframe.grid_rowconfigure((1), weight = 1)

    #Visualiszation section (canvas)
    mainnav = customtkinter.CTkFrame(master = mainframe, fg_color = "gray30")
#    mainnav.grid(row = 0, column = 0, padx = (0,10), pady = (0,10), sticky = "nsew")
    mainnav.grid(row = 0, column = 0, padx = (0,0), pady = (0,0), sticky = "nsew")
    canvas = tkinter.Canvas(master = mainnav)
    mainnav.grid_columnconfigure((0), weight = 1)
    mainnav.grid_rowconfigure((0), weight = 1)
    canvas.grid(row = 0, column = 0, sticky = "nsew")

    crosshair1 = canvas.create_oval(0, 0, 10, 10, outline = "black", fill = "white", tags = "crosshair1")
    crosshair2 = canvas.create_oval(100, 100, 110, 110, outline = "black", fill = "white", tags = "crosshair2")
    crosshair1_coords = {'x':0, 'y':0}
    crosshair2_coords = {'x':100, 'y':100}

    crosshair1x = canvas.create_line(0,crosshair1_coords['y']+5,int(canvas.winfo_width()),crosshair1_coords['y']+5, dash = (5, 2, 3, 2), fill = "black", width = 1, tags = "crosshair1x")
    crosshair1y = canvas.create_line(crosshair1_coords['x']+5, 0, crosshair1_coords['x']+5, int(canvas.winfo_height()), dash = (5, 2, 3, 2), fill = "black", width = 1, tags = "crosshair1y")
    crosshair2x = canvas.create_line(0,crosshair2_coords['y']+5,int(canvas.winfo_width()),crosshair2_coords['y']+5, dash = (5, 2, 3, 2), fill = "black", width = 1, tags = "crosshair2x")
    crosshair2y = canvas.create_line(crosshair2_coords['x']+5, 0, crosshair2_coords['x']+5, int(canvas.winfo_height()), dash = (5, 2, 3, 2), fill = "black", width = 1, tags = "crosshair2y")
    canvas.tag_bind(crosshair1, "<Button-1>", drag_start)
    canvas.tag_bind(crosshair2, "<Button-1>", drag_start)
    canvas.tag_bind(crosshair1, "<B1-Motion>", drag_motion)
    canvas.tag_bind(crosshair2, "<B1-Motion>", drag_motion)
    canvas.tag_bind(crosshair1, "<ButtonRelease-1>", drag_end)
    canvas.tag_bind(crosshair2, "<ButtonRelease-1>", drag_end)

    # #bottom section (font size adjustment)
    # bottombar = customtkinter.CTkFrame(master = mainframe, fg_color = "gray30")
    # bottombar.grid(row = 1, column = 0, padx = (0,10), pady = (10,0), sticky = "nsew")
    # FontSizeLabel = customtkinter.CTkLabel(master = bottombar, text = "Font Size:", fg_color = "transparent")
    # FontSizeLabel.pack(side = 'left', padx = (10,5))
    # FontSizeSlider = customtkinter.CTkSlider(master = bottombar, fg_color = "#000000")
    # FontSizeSlider.pack(side = 'left', padx = (5,10), fill = "x", expand = 1)
    
    #tabview (importing all necessary templates, font, and name&email list)
    editbar = customtkinter.CTkFrame(master = app, width = 175)
    editbar.pack(padx = (5,10), pady = (10,10), side = 'left', fill = "y", expand = 0)
    tabview = customtkinter.CTkTabview(master = editbar, fg_color = "gray30", width = 175)
    tabview.pack(padx = (0,0), pady = (0,0), side = 'top', fill = "y", expand = 1)
    Document = tabview.add("Document")
    Text = tabview.add("Text")
    imgSelectBtn = customtkinter.CTkButton(master = Document, text = "Import Template", command = select_certificate_img)
    imgSelectBtn.pack(side = 'top', padx = (5,5), pady = (5,5))
    csvSelectBtn = customtkinter.CTkButton(master = Document, text = "Import Spreadsheet", command = set_mailList)
    csvSelectBtn.pack(side = 'top', padx = (5,5), pady = (5,5))
    FontSelectEntry = customtkinter.CTkEntry(master = Document, placeholder_text = "Import Google Font")
    FontSelectEntry.pack(side = 'top', padx = (5,5), pady = (5,0))
    FontSelectBtn = customtkinter.CTkButton(master = Document, text = "open", command = lambda:get_font_from_url(FontSelectEntry.get()))
    FontSelectBtn.pack(side = 'top', padx = (5,5), pady = (5,0))

    function_lock = threading.Lock()
    canvas.bind("<Configure>", on_configure)
    colorpicker = CTkColorPicker(master = Text, width=215, orientation="horizontal", command=lambda e:color_select(e))
    colorpicker.pack(padx=(0,0), pady=(5,5), side="top")

    QuestionBtn = customtkinter.CTkButton(master = editbar, text = "Help", width = 40, height = 20, font = ("",-10), command = help)
    QuestionBtn.pack(padx = (5,0), pady = (5,0), side='bottom', anchor='e')
    SendCertificates = customtkinter.CTkButton(master = editbar, text = "Send Certificates", command = send_email)
    SendCertificates.pack(side = 'bottom', padx = (5,5), pady = (5,0))
    app.mainloop()
