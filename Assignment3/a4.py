import re
import json
import time
from tkinter import *

def listToString(s):
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
    # return string
    return str1

# this function will return the id list for the query
def findSameDoc(query):
    id_list = []
    common_id = []
    with open ('/Users/hanson/Desktop/report/submit2.json', 'r') as f:
        src = json.load(f)
        if len(query) < 2:
            for i in src[listToString(query)]:
                common_id.append(i[0])
        else:
            for word in query:
                for i in src[listToString(word)]:
                    if i[0] not in id_list:
                        id_list.append(i[0])
                    else:
                        common_id.append(i[0])
    return common_id


# check if first two words in query is adjcentWord
def isAdjcentword(common_id, query_set):
    with open ('/Users/hanson/Desktop/report/word_position.json', 'r') as f:
        src = json.load(f)
    post1 = src[str(common_id)][query_set[0]]
    post2 = src[str(common_id)][query_set[1]]
    diff = []
    for i in post1:
        for j in post2:
            diff.append(j-i-len(query_set[0]))
    if 1 or 0 in diff:
        return True
    else:
        return False

def get_link(url_id):
    url_links = []
    with open ('/Users/hanson/Desktop/report/doc_id.json', 'r') as f:
        src = json.load(f)
    for i in url_id:
        url_links.append(src[str(i)])
    return url_links

def search_index(word):
    # print("enter word")
    # word = input()
    # word.lower()
    query_set = []
    query_set = word.split()

    length = len(query_set)
    links = []
    url_id = []
    if length < 2:
        common_id = []
        common_id = findSameDoc(query_set)
        url_id = common_id
    else:
        i = 0
        haveAdjcent = False
        while (i+1) < length:
            firstTwoWords = []
            firstTwoWords.append(query_set[i])
            firstTwoWords.append(query_set[i+1])
            print(firstTwoWords)
            common_id = []
            common_id = findSameDoc(firstTwoWords)
            for singleId in common_id:
                haveAdjcent = isAdjcentword(singleId,firstTwoWords)
                
                if haveAdjcent == True:
                    url_id.append(singleId)
            if haveAdjcent == False:
                url_id = common_id
            i+=1
#    links = get_link(url_id)
    with open ('/Users/hanson/Desktop/report/doc_id.json', 'r') as f:
        src = json.load(f)

    for i in url_id:
        links.append(src[str(i)])
    return links


def displayInfo(x):
    return search_index(x)


# def search():
#     word = u.get()
#     url_links = displayInfo(word)
#     label = Label(root, text= url_links)
#     label.pack()

    
# root = Tk()
# root.title("NiuBi Search")
# frame = Frame(root)
# frame.pack(padx=8, pady=8, ipadx=4)
# lab1 = Label(frame, text="query:")
# lab1.grid(row=0, column=0, padx=5, pady=5, sticky=W)

# myLabel = Label(frame)

# #绑定对象到Entry
# u = StringVar()
# ent1 = Entry(frame, textvariable=u)
# ent1.grid(row=0, column=1, sticky='ew', columnspan=2)


# button = Button(frame, text="Search", command=search,default='active')# default='active'
# button.grid(row=1, column=0)

# # DeleteButton = Button(frame, text="Delete Text", command=myDelete)
# # DeleteButton.grid(row=1, column=2)

# # lab3 = Label(frame, text="")
# # lab3.grid(row=2, column=0, sticky=W)


# #以下代码居中显示窗口

# root.update_idletasks()
# x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
# y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
# root.geometry("+%d+%d" % (x, y))
# root.mainloop()

def myClick():
    global myLabel
    myLabel = Label(root)
    myLabel.destroy()

    # calcute the search time
    start_time = time.time()
    url_links = displayInfo(e.get())
    print("--- %s seconds ---" % (time.time() - start_time))
    # url_links = "Hello " + e.get()

    myLabel = Label(root, text = url_links)

    e.delete(0, 'end')
    myLabel.grid(row=3, column=0, pady=10)

# GUI for the search enginee 
root = Tk()
root.title('NewBee Search')
root.geometry("400x400")

myLabel = Label(root)

e = Entry(root, width=15, font=('Helvetica', 30))
e.grid(row=0, column=0, padx=10, pady=10)


myButton = Button(root, text='Saerch', command=myClick)
myButton.grid(row=1, column=0, pady=10)



root.mainloop()






