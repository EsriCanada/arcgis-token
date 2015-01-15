import Tkinter as tk
import urllib
import json


def Pressed(event=None):
    text.insert(tk.INSERT, "")
    lblMessage.set("")

    url = 'https://www.arcgis.com/sharing/rest'
    submitUrl = url + '/generateToken'

    data = {'username': username_text.get(), 'password': passwordText.get(), 'expiration': 60, 'client': 'referer',
            'referer': 'https://www.arcgis.com',
            'f': 'json'}

    submitResponse = urllib.urlopen(submitUrl, urllib.urlencode(data))
    submitJson = json.loads(submitResponse.read())

    if 'error' in submitJson:
        lbl_elem.config(fg='red')
        lblMessage.set(str(submitJson['error']['details'][0]))
    else:
        if var.get():
            root.clipboard_clear()
            root.clipboard_append(str(submitJson['token']))
        lbl_elem.config(fg='blue')
        lblMessage.set("Token Granted")
        text.insert(tk.INSERT, str(submitJson['token']))


# Select all the text in textbox
def select_all(event):
    text.tag_add(tk.SEL, "1.0", tk.END)
    text.mark_set(tk.INSERT, "1.0")
    text.see(tk.INSERT)
    return 'break'


root = tk.Tk()
root.wm_title("Token Generator")
root.resizable(width=tk.FALSE, height=tk.FALSE)
root.geometry("200x250")

lblUser = tk.Label(root, text="Username")
lblUser.pack()

username_text = tk.StringVar()
username_elem = tk.Entry(root, textvariable=username_text)
username_elem.focus_set()
username_elem.pack()

lblPass = tk.Label(root, text="Password")
lblPass.pack()

passwordText = tk.StringVar()
password_elem = tk.Entry(root, show='*', textvariable=passwordText)
password_elem.pack()

var = tk.IntVar()
btn_check = tk.Checkbutton(root, text="Copy token to clipboard?", variable=var)
btn_check.pack()

button = tk.Button(root, text='Get Token', command=Pressed)
button.pack(pady=20, padx=20)
root.bind('<Return>', Pressed)

lblMessage = tk.StringVar()
lbl_elem = tk.Label(root, textvariable=lblMessage)
lbl_elem.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text = tk.Text(root, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=5)
text.pack()
text.bind("<Control-Key-a>", select_all)

scrollbar.config(command=text.yview)

root.mainloop()
