from tkinter import *
from wonderwords import RandomSentence
import time



def thread1():
    def generate_random_para():        
        formated_para = ""
        
        for i in range(16):
            if len(formated_para)==0:
                formated_para += RandomSentence().sentence()
            else:
                formated_para += " "+RandomSentence().sentence()
        else:
            return formated_para


    def time_taken(events=None):
        end = time.time()
        counter = 0
        correct_char_written = ""
        char_entered_user = entry_widget.get("1.0","end-1c").strip()
        for i in char_entered_user:
            if i==paragraph[counter]:
                correct_char_written += i
            else:
                pass
            
            counter += 1
        
        try:
            total_time = end-start
            wpm = round((len(correct_char_written)*60)/(5*round(total_time,2)),2)
            accuracy = round((len(correct_char_written)/len(char_entered_user))*100,2)
            print("WPM",wpm)
            print("Accuracy",accuracy,"%")
            wpm_acuracy.config(text=f"WPM: {wpm}\t\tAccuracy: {accuracy} %")
            entry_widget.after(500,time_taken)
        except:
            ...
    
    
    root = Tk()

    root.configure(bg="#161616")
    root.resizable(False,False)
    paragraph = generate_random_para()
    # paragraph = "My Name is Akhilesh Verma"

    root.geometry("1150x450")

    text_widget = Text(root, wrap=WORD, font="Consolas 14 bold", bg="#161616", fg="#c0c0c0")
    text_widget.insert(INSERT, paragraph)
    text_widget.config(state=DISABLED)  # Make the text widget read-only
    text_widget.place(x=1, y=1, relwidth=1,relheight=0.4)
    
    start = time.time()
    
    entry_widget = Text(root,wrap=WORD,font="Roboto 14 bold",fg="#151515")
    entry_widget.place(x=1,y=150,relheight=0.32,relwidth=1)
    # entry_widget.bind("<Return>",time_taken)
    
    
    wpm_acuracy = Label(root,text="Nothing",font="Aerial 13 bold",fg="#F8F8F8",bg="#161616")
    wpm_acuracy.place(x=1,y=350)
    
    time_taken()
    
    root.mainloop()
    



thread1()