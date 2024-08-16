from tkinter import Tk,Text,Label,WORD,INSERT,DISABLED
from threading import Thread
from wonderwords import RandomSentence
from time import sleep


def generate_random_para() -> str:        
    formated_para = []
    for i in range(16):
        if len(formated_para)==0:
            formated_para.append(RandomSentence().sentence())
        else:
            formated_para.append(" ")
            formated_para.append(RandomSentence().sentence())
            
    else:
        return "".join(formated_para)


def time_taken(entry_widget:Text, paragraph:str, show_wpm_accuracy:Label) -> None:
    entry_widget.config(state="disabled")
    correct_char_written = []
    char_entered_user = entry_widget.get("1.0","end-1c").split()
    paragraph = paragraph.split()
    for i, char in enumerate(char_entered_user):
        if i < len(paragraph) and char == paragraph[i]:
            entry_widget.config(fg="#0E7534")
            correct_char_written.append(char)
        else:
            entry_widget.config(fg="#FF0000")
    else:
        second_min = 15/60
        gross_wpm = len(char_entered_user)/second_min
        uncorrect_error_wpm = len(correct_char_written)/second_min
        net_wpm = gross_wpm - uncorrect_error_wpm
        
        del gross_wpm, uncorrect_error_wpm
        accuracy = round(len(correct_char_written)/len(char_entered_user),2)*100
        
        show_wpm_accuracy.config(text=f"WPM: {net_wpm} | Accuracy: {accuracy} %")
        


def start_timer(entry_widget:Text, paragraph:str, root:Tk, show_time:Label,
                show_wpm_accuracy:Label):
    timmee = 16
    while 0<timmee:
        timmee -= 1
        show_time.config(text=f"{timmee}")
        root.update()
        sleep(1)
    else:
        time_taken(entry_widget=entry_widget, show_wpm_accuracy=show_wpm_accuracy, paragraph=paragraph)


def start_io(entry_widget:Text, paragraph:str, root:Tk, show_time:Label,
            show_wpm_accuracy:Label, events=None):
    entry_widget.unbind("<KeyPress>")
    
    a = Thread(target=start_timer,args=(entry_widget, paragraph, root, show_time, show_wpm_accuracy))
    a.start()


def gui() -> None:
    root:Tk = Tk()
    root.configure(bg="#161616")
    root.resizable(False,False)
    paragraph = generate_random_para()
    
    # paragraph = "My Name is Akhilesh Verma"
    root.geometry("1150x450")
    text_widget:Text = Text(root, wrap=WORD, font="Consolas 14 bold", bg="#161616", fg="#c0c0c0")
    text_widget.insert(INSERT, paragraph)
    text_widget.config(state=DISABLED)  # Make the text widget read-only
    text_widget.place(x=1, y=1, relwidth=1,relheight=0.4)
    
    
    entry_widget:Text = Text(root,wrap=WORD,font="Roboto 14 bold",fg="#0E7534")
    entry_widget.place(x=1,y=150,relheight=0.32,relwidth=1)
    
    show_time = Label(root,text="30",fg="#F70B0B",bg="#161616",font="Roboto 20 bold")
    show_time.place(x=1,y=300)
    
    entry_widget.bind("<KeyPress>",lambda event: start_io(entry_widget=entry_widget, paragraph=paragraph,
                                                       root=root, show_time=show_time,
                                                       show_wpm_accuracy=show_wpm_accuracy
                                                       ))    
    
    # entry
    show_wpm_accuracy = Label(root,text="rt",bg="#161616",fg="#C0C0C0",font="Aerial 14 bold")
    show_wpm_accuracy.place(x=0,y=350)
    root.mainloop()



gui()