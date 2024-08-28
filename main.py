from tkinter import Tk,Text,Label,WORD,INSERT,DISABLED,IntVar,Radiobutton,END, OptionMenu, StringVar
from json import load
import sys
import tkinter.messagebox as msgb
from threading import Thread
from wonderwords import RandomWord
from time import sleep


def generate_random_para(n:int) -> str:
    paragraph = RandomWord().random_words(n)
    return " ".join(paragraph)


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
        


def timer(entry_widget:Text, paragraph:str, root:Tk, show_time:Label,
                show_wpm_accuracy:Label, time_sec:IntVar) -> None:
    timmee = time_sec.get()
    while 0<timmee:
        timmee -= 1
        show_time.config(text=f"{timmee}")
        root.update()
        sleep(1)
    else:
        time_taken(entry_widget=entry_widget, show_wpm_accuracy=show_wpm_accuracy, paragraph=paragraph)


def start_time(entry_widget:Text, paragraph:str, root:Tk, show_time:Label,
            show_wpm_accuracy:Label, text_widget:Text, time_sec:IntVar, events=None) -> None:
    
    a = Thread(target=timer,args=(entry_widget, paragraph, root, show_time, show_wpm_accuracy, time_sec))
    
    if time_sec.get() in {15,30,45,60}:
        entry_widget.delete("1.0",END)
        entry_widget.unbind("<KeyPress>")
        
        a.start()
    else:
        entry_widget.delete("1.0",END)
        msgb.showerror(title="Time Not Selected",message="Please Select Time!")


def theme(master:Tk, theme:dict, text_widget:Text, events=None):
    master.configure(bg=theme["bg"])
    text_widget.config(bg=theme["bg"],fg=theme["fg"])
    # entry_widget.config(bg=theme["bg"])
    
    
def gui() -> None:
    root:Tk = Tk()
    root.resizable(False,False)    
    root.geometry("1200x650")
    
    time_sec = IntVar()
    time_sec.set(15)
    checkbutton1:Radiobutton = Radiobutton(root, text="15", variable=time_sec, bg="#212135", fg="#FAEFEF",
                               relief="raised", selectcolor="#000000", width=3, height=2,
                               value=15)

    checkbutton2:Radiobutton = Radiobutton(root, text="30", variable=time_sec, bg="#212135", fg="#FAEFEF",
                               relief="raised", selectcolor="#000000", width=3, height=2,
                               value=30)

    checkbutton3:Radiobutton = Radiobutton(root, text="45", variable=time_sec, bg="#212135", fg="#FAEFEF",
                               relief="raised", selectcolor="#000000", width=3, height=2,
                               value=45)

    checkbutton4:Radiobutton = Radiobutton(root, text="60", variable=time_sec, bg="#212135", fg="#FAEFEF",
                               relief="raised", selectcolor="#000000", width=3, height=2,
                               value=60)

    
    checkbutton1.place(x=400,y=0)
    checkbutton2.place(x=480,y=0)
    checkbutton3.place(x=560,y=0)
    checkbutton4.place(x=640,y=0)
    
    theme_set = StringVar()
    
    with open("themes.json") as file:
        theme_with_hexcolor:dict = load(file)
        list_theme_with_hexcolor:list = list(theme_with_hexcolor)
        list_theme_with_hexcolor.sort()
    
    theme_set.set(list_theme_with_hexcolor[0])
    themes = OptionMenu(root,theme_set,*list_theme_with_hexcolor)
    themes.place(x=1000,y=0)
    
    defaut_theme = theme_with_hexcolor["default"]
    root.configure(bg=defaut_theme["bg"])
    
    paragraph = generate_random_para(170)
    # paragraph = "My Name is Akhilesh Verma"
    
    text_widget:Text = Text(root, wrap=WORD, font="Consolas 14 bold", bg=defaut_theme["bg"],
                            fg=defaut_theme["fg"])
    text_widget.insert(INSERT, paragraph)
    text_widget.config(state=DISABLED)  # Make the text widget read-only
    text_widget.place(x=0, y=30, relwidth=1,relheight=0.44)
    
    
    entry_widget:Text = Text(root,wrap=WORD,font="Roboto 14 bold",fg=defaut_theme["writefg"])
    entry_widget.place(x=1,y=325,relheight=0.3,relwidth=1)
    
    show_time = Label(root,text="",fg="#F70B0B",bg="#323437",font="Roboto 20 bold")
    show_time.place(x=1,y=300)
    
    
    start_time_func = lambda event: start_time(entry_widget=entry_widget, paragraph=paragraph,
                                                       root=root, show_time=show_time,
                                                       show_wpm_accuracy=show_wpm_accuracy,
                                                       text_widget=text_widget, time_sec=time_sec)
    
    entry_widget.bind("<KeyPress>",start_time_func)    
    
    theme_set.trace_add("write",lambda *event:theme(master=root,theme=theme_with_hexcolor[theme_set.get()],
                                                   text_widget=text_widget))
    
    # entry
    show_wpm_accuracy = Label(root,text="",bg="#323437",fg="#C0C0C0",font="Aerial 14 bold")
    show_wpm_accuracy.place(x=0,y=350)
    
    
    root.mainloop()


if __name__=="__main__":
    gui()