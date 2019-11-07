from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl, random, webbrowser
from tkinter import *
from PIL import Image, ImageTk

SUBJECTS = {}
RESULT = []

def SoupIt():
    global SUBJECTS
    context = ssl._create_unverified_context()
    response = urlopen("https://www.tutorialspoint.com/tutorialslibrary.htm", context=context)
    htmlinfo = response.read()
    soup = BeautifulSoup(htmlinfo, 'html.parser')
    # print(soup)
    columns = soup.find_all("div", {"class":"mui-col-md-3"})
    # print(columns)
    for column in columns:
        subjs = column.find_all("li")
        for sub in subjs:
            content = sub.a
            if (content == None):
                break
            link = content.get('href')
            title = content.get('title')
            # print(title, link)
            SUBJECTS[title] = link
    # print(SUBJECTS)

def GetRandomSubject():
    global SUBJECTS
    randNum = random.randint(0, len(SUBJECTS) - 1)
    THECHOSENONE = list(SUBJECTS.keys())[randNum]
    # print("Subject of the day:", THECHOSENONE)
    context = ssl._create_unverified_context()
    finalLink = 'https://www.tutorialspoint.com' + SUBJECTS[THECHOSENONE]
    # print("Link:", finalLink)
    # webbrowser(finalLink, new=0, autoraise=True)
    # urlopen("https://www.tutorialspoint.com/" + SUBJECTS[THECHOSENONE], context = context)
    return THECHOSENONE, finalLink

def loadImg():
    load = Image.open("study.png")
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x = 0, y = 0)

def randomizeSubject():
    global RESULT, subjectLabel
    RESULT = GetRandomSubject()
    subjectLabel.config(text=RESULT[0])

def browseLink():
    global RESULT
    # context = ssl._create_unverified_context()
    # print(RESULT[1])
    # urlopen(RESULT[1], context = context)
    webbrowser.open_new(RESULT[1])

def runGUI():
    global RESULT, subjectLabel
    root = Tk()
    root.title("TutorialsOnPoint Randomizer")
    root.option_add('*font', ('verdana', 12, 'bold'))

    # winWidth = root.winfo_reqwidth()
    # winHeight = root.winfo_reqheight()
    # positionRight = int(root.winfo_screenwidth()/2 - winWidth/2)
    # positionDown = int(root.winfo_screenheight()/2 - winHeight/2)
    # root.geometry("700x400+300+300")
    # root.geometry("+{}+{}".format(positionRight, positionDown))
    # loadImg()
    # loadTxt(textResult)

    leftFrame = Frame(root)
    leftFrame.pack(side=LEFT)
    rightFrame = Frame(root)
    rightFrame.pack(side=LEFT)

    load = Image.open("study.png")
    render = ImageTk.PhotoImage(load)
    img = Label(leftFrame, image=render)
    img.pack()

    label1 = Label(rightFrame, text="Random subject for today: ")
    label1.pack(side=TOP)
    subjectLabel = Label(rightFrame, text=RESULT[0], bg="green", fg="white")
    subjectLabel.pack(side=TOP)
    subjectBtn = Button(rightFrame, text="Randomize subject", bg="pink", command=randomizeSubject)
    subjectBtn.pack()
    linkBtn = Button(rightFrame, text="Open in browser", bg="pink", command=browseLink)
    linkBtn.pack()

    root.mainloop()

#MAIN
def main():
    global SUBJECTS, RESULT
    SoupIt()
    RESULT = GetRandomSubject()
    runGUI()

if __name__ == "__main__":
    main()