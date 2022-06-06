from socket import *
from threading import *
from tkinter import *
from tkinter import simpledialog
from tkinter import scrolledtext

# Connecting To Server
client = socket(AF_INET, SOCK_STREAM)
client.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

client.connect(('127.0.0.1', 7500))

nicknameWin = Tk()
nicknameWin.withdraw()

nickname = simpledialog.askstring("Nickname", "Nickname:",
                                  parent=nicknameWin)

win = Tk()
bgClr = "lightgray"
font = ("Arial", 12)
win.configure(bg=bgClr)
win.title(nickname)

msg_label = Label(win, text="Chat App\nWelcome " + nickname, bg=bgClr)
msg_label.config(font=font)
msg_label.pack(padx=20, pady=5)

txtMessages = scrolledtext.ScrolledText(win, width=50)
txtMessages.pack(padx=20, pady=5)


msg_label = Label(win, text="Message:", bg=bgClr)
msg_label.config(font=font)
msg_label.pack(padx=20, pady=5)

txtYourMessage = Entry(win, width=50)
txtYourMessage.pack(padx=20, pady=10)


def sendMsg():
    clientMessage = txtYourMessage.get()
    client.send((nickname + ": " + clientMessage).encode("ascii"))
    txtYourMessage.delete(0, END)


send_bt = Button(win, text="send", command=sendMsg)
send_bt.config(font=font)
send_bt.pack(padx=20, pady=5)


def stop():
    win.destroy()
    client.close()
    exit(0)


win.protocol("WM_DELETE_WINDOW", stop)


def recvMessage():
    while True:
        serverMessage = client.recv(1024).decode("ascii")
        if serverMessage == "NICK":
            client.send(nickname.encode("ascii"))
        else:
            print(serverMessage)
            txtMessages.insert(END, "\n" + serverMessage)


recvThread = Thread(target=recvMessage)
recvThread.daemon = True
recvThread.start()

win.mainloop()
