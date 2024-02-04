from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget, QLabel, QPushButton, QLineEdit, QInputDialog
import json

app = QApplication([])

notes = {}
filteredNotes = {}

isSearching = False

def jsonLoad():
    with open("notes_data.json", "r", encoding="utf-8") as file:
        global notes
        notes = json.load(file)


def jsonUpLoad():
    with open("notes_data.json", "w") as file:
        global notes
        notes = json.dump(notes, file)

def addItemIntoList(itemName):
    listWidget.addItem(str(itemName))
def addItemIntoTags(itemName):
    tagsList.addItem(str(itemName))

def showNote(text):
    MainTextField.setText(text)

def createNoteFunc():
    text, ok = QInputDialog.getText(win, "Add note", "Name of note:")
    if ok and text != "":
        jsonLoad()
        addItemIntoList(text)
        notes[text] = {"text": "", "tag": []}
        jsonUpLoad()

def deleteNoteFunc():
    jsonLoad()
    key = listWidget.selectedItems()[0].text()
    del notes[key]
    listWidget.clear()
    jsonUpLoad()
    refreshList()

def saveNoteFunc():
    jsonLoad()
    key = listWidget.selectedItems()[0].text()
    notes[key] = {"text": MainTextField.toPlainText(), "tag": []}
    jsonUpLoad()

def refreshList():
    jsonLoad()
    for note in notes:
        listWidget.addItem(str(note))

def openNoteFunc():
    jsonLoad()
    key = listWidget.selectedItems()[0].text()
    text = notes[key]["text"]
    win.setWindowTitle("Smart Notes: "+key)
    MainTextField.setText(text)

def searchNotes():
    jsonLoad()
    global isSearching
    if isSearching == False:
        search_tag = searchTag.text()
        tagsList.clear()
        for note in notes: 
            tags = notes[note]["tag"]
            if search_tag in tags:
                tagsList.addItem(note)
        searchUsingTag.setText("Cancel search")
        isSearching = True
    else:
        tagsList.clear()
        searchUsingTag.setText("Search using tag")
        for note in notes:
            tagsList.addItem(note)
        isSearching = False

def addToTagFunc():
    jsonLoad()
    tag = searchTag.text()
    selected_item = tagsList.currentItem()
    if selected_item:
        key = selected_item.text()
        notes[key]["tag"].append(tag)
        jsonUpLoad()

def refreshTagsList():
    jsonLoad()
    for note in notes:
        tagsList.addItem(note)
    
win = QWidget()
win.setWindowTitle("Smart Notes")

main_layout = QHBoxLayout()
secondary_layout = QVBoxLayout()

MainTextField = QTextEdit()
main_layout.addWidget(MainTextField)

ListTitle = QLabel("List of notes")
secondary_layout.addWidget(ListTitle)

listWidget = QListWidget()
secondary_layout.addWidget(listWidget)

createNewNoteButton = QPushButton("Create Note")
createNewNoteButton.clicked.connect(createNoteFunc)
secondary_layout.addWidget(createNewNoteButton)

deleteNoteButton = QPushButton("Delete Note")
deleteNoteButton.clicked.connect(deleteNoteFunc)
secondary_layout.addWidget(deleteNoteButton)

saveNote = QPushButton("Save Note")
saveNote.clicked.connect(saveNoteFunc)
secondary_layout.addWidget(saveNote)

openNote = QPushButton("Open Note")
openNote.clicked.connect(openNoteFunc)
secondary_layout.addWidget(openNote)

tagsListTitle = QLabel("List of searched notes")
secondary_layout.addWidget(tagsListTitle)

tagsList = QListWidget()
secondary_layout.addWidget(tagsList)

searchTag = QLineEdit()
searchTag.setPlaceholderText("Enter tag")
secondary_layout.addWidget(searchTag)

addToTag = QPushButton("Add to tag")
addToTag.clicked.connect(addToTagFunc)
secondary_layout.addWidget(addToTag)

removeFromTag = QPushButton("Remove from tag")
secondary_layout.addWidget(removeFromTag)

searchUsingTag = QPushButton("Search using tag")
searchUsingTag.clicked.connect(searchNotes)
secondary_layout.addWidget(searchUsingTag)

refreshList()
refreshTagsList()

main_layout.addLayout(secondary_layout)
win.setLayout(main_layout)
win.show()

app.exec_()