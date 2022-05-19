from tkinter import *
import time
from tkinter.messagebox import *
import requests


total_chars = 0
words_index = 0
incorrect = 0
correct = 0


def move_tag(event):
    index = len(user_entry.get("1.0", END))
    if event.char == " ":
        show_another_word()
    else:
        word_label.tag_remove('hg', '1.0', f'1.{index-1}')


def calculate_incorrect(user_entry, word):
    global total_chars
    total_chars += len(user_entry)
    global incorrect
    global correct
    if user_entry != word:
        incorrect += 1
        print(f"This Word {word.strip()} you typed {user_entry.strip()} Are they the same? {word == user_entry}")
        print(user_entry)
        print(word)
    else:
        correct += len(user_entry)


def show_another_word():
    # insert a new text in word label
    calculate_incorrect(user_entry=user_entry.get("1.0", END).strip(), word=word_label.get("1.0", END).strip())
    global words_index
    words_index += 1
    word_label.config(state="normal")
    word_label.delete("1.0", END)
    word_label.insert("1.0", words_list[words_index])
    word_label.tag_add("hg", "1.0", "5.0")
    word_label.tag_config("hg", background="#FFC0D3")
    word_label.config(state="disabled")

    user_entry.focus()
    user_entry.delete("1.0", END)
    user_entry.mark_set("insert", "1.0")
    user_entry.tag_add("start", "1.0", "5.0")
    user_entry.tag_config("start", background="#FDEFF4")


def count_down(count):
    clock_label.config(text=count)
    if count > 0:
        window.after(1000, count_down, count-1)
    else:
        wpm = round((total_chars / 5) / 1)
        print(f"This is icorrect Words .. {incorrect}")
        words_per_minute_value.config(text=wpm)
        accuracy = round((correct / total_chars) * 100)
        accuracy_value.config(text=accuracy)
        net_wpm = round(((total_chars / 5) - incorrect)/1)
        net_wpm_value.config(text=net_wpm)
        user_entry.delete("1.0", END)
        user_entry.config(state="disabled")
        showinfo(
            title="Done", message="Done"
        )
        restart_button.grid(column=1, row=7)



def restart():
    global total_chars
    global words_index
    global incorrect
    global correct
    global words_index
    global words_list
    total_chars = 0
    words_index = 0
    incorrect = 0
    correct = 0
    words_index = 0
    clock_label.config(text="0")
    words_per_minute_value.config(text="")
    accuracy_value.config(text="0")
    start_button.config(state="normal")
    response = requests.get("https://random-word-api.herokuapp.com//word?number=500")
    words_list = response.json()
    word_label.config(state="normal")
    word_label.delete("1.0", END)
    word_label.insert("1.0", words_list[words_index])
    word_label.tag_add("hg", "1.0", "5.0")
    word_label.tag_config("hg", background="#FFC0D3")
    word_label.config(state="disabled")

    user_entry.focus()
    user_entry.delete("1.0", END)
    user_entry.mark_set("insert", "1.0")
    user_entry.tag_add("start", "1.0", "5.0")
    user_entry.tag_config("start", background="#FDEFF4")
    user_entry.config(state="disabled")



def start_timer():
    start_button.config(state="disabled")
    user_entry.config(state="normal")
    count_down(1*60)


def return_pressed(event):
    show_another_word()


window = Tk()
window.geometry('800x600')

window.config(padx=100, pady=50, bg="#524A4E")
time_label = Label(window, text="Time", bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
time_label.grid(column=0, row=0)

clock_label = Label(window, text="0", bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
clock_label.grid(column=0, row=1)

words_per_minute = Label(window, text="Words Per Minute", bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
words_per_minute.grid(column=1, row=0, padx=20)

words_per_minute_value = Label(window, text="...", bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
words_per_minute_value.grid(column=1, row=1)

accuracy_label = Label(window, text="Accuracy %", bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
accuracy_label.grid(column=2, row=0)

accuracy_value = Label(window, text=".. %", bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
accuracy_value.grid(column=2, row=1)

net_wpm_label = Label(window, text="Net WPM",bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
net_wpm_label.grid(column=3, row=0)

net_wpm_value = Label(window, text="...",bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
net_wpm_value.grid(column=3, row=1)


response = requests.get("https://random-word-api.herokuapp.com//word?number=500")
words_list = response.json()

label1 = Label(window, text="What You will Type .. ", bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
label1.grid(column= 1, row=2, pady=10, padx=10)
word_label = Text(window, height=1, width=20, font=("Courier", 15))
word_label.insert("1.0", words_list[0])
word_label.mark_set("insert", END)
word_label.tag_add("hg", "1.0", "5.0")
word_label.tag_config("hg", background="#FFC0D3")
word_label.config(state="disabled")
word_label.grid(column=1, row=3, columnspan=2)

label2 = Label(window, text="Type Here .. ", bg= "#524A4E",fg="#FF5C8D", font=("Courier", 15))
label2.grid(column= 1, row=4, pady=10, padx=10)

user_entry = Text(window, height=1, width=20, font=("Courier", 15))
user_entry.focus()
user_entry.mark_set("insert", END)
user_entry.tag_add("start", "1.0", "5.0")
user_entry.tag_config("start", background="#FDEFF4")
user_entry.grid(column=1, row=5, columnspan=2)
user_entry.config(state="disabled")

user_entry.bind("<Key>", func=move_tag)
user_entry.bind("<Return>", func=return_pressed)
start_button = Button(text="Start Typing", bg="#FF5C8D", fg="#FDEFF4" ,command=start_timer, pady=10)
start_button.grid(column=1, row=6)


restart_button = Button(text="Restart Timer", bg="#FF5C8D", fg="#FDEFF4" ,command=restart, pady=10)
# restart_button.grid(column=1, row=6)
window.mainloop()