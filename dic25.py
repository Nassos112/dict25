# dict25 v1.3   [11/2/2025]

from pydoc import text
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from turtle import Vec2D
from PIL import Image, ImageTk
import pandas as pd
import openpyxl, os
import webbrowser
import random
import pygame
pygame.init()
wrong=pygame.mixer.Sound("sounds/wrong.wav")
corr=pygame.mixer.Sound("sounds/corr.wav")
pan=pygame.mixer.Sound("sounds/pansoft.mp3")
pop=pygame.mixer.Sound("sounds/pop1.mp3")
menu=pygame.mixer.Sound("sounds/menu1.mp3")
web=pygame.mixer.Sound("sounds/web.mp3")
click=pygame.mixer.Sound("sounds/click.mp3")
hit=pygame.mixer.Sound("sounds/hit.mp3")
play1=pygame.mixer.Sound("sounds/play1.mp3")
r_from=10
r_upto=20
string_on=False
mode=sounds=True
res_window=None

if sounds:pygame.mixer.Sound.play(pan)

vath=0
startfrom=0 # search_a string in active_list
more=loc=reverse=langs_selector=False   

def load_data():
    global file_name
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")]) 
    file_name = os.path.basename(file_path)
    root.focus_force()
    if file_path:
        df = pd.read_excel(file_path)
        # Fill NaN values with empty strings
        df = df.fillna("")
        greek_words = df.iloc[:, 0].tolist()
        english_words = df.iloc[:, 1].tolist()
        italian_words = df.iloc[:, 2].tolist()
        spanish_words = df.iloc[:, 3].tolist()
        french_words = df.iloc[:, 4].tolist()
        return greek_words, english_words, italian_words, spanish_words, french_words    
    return [], [], [], [], []

def update_entries(index):
    if sounds:pygame.mixer.Sound.play(click)
    if index < len(greek_words):  
        file_entry.delete(0, tk.END)
        len_entry.delete(0, tk.END)
        french_entry.delete(0, tk.END)
        spanish_entry.delete(0, tk.END) 
        italian_entry.delete(0, tk.END)
        english_entry.delete(0, tk.END)
        greek_entry.delete(0, tk.END)

        greek_entry.insert(0, greek_words[index])
        english_entry.insert(0, english_words[index]) 
        italian_entry.insert(0, italian_words[index])
        spanish_entry.insert(0, spanish_words[index])
        french_entry.insert(0, french_words[index])
       
       
        cur_index.config(text=index+1)
        file_entry.insert(0, file_name)    
        len_entry.insert(0, len(greek_words))

def alter_dict():
    if sounds:pygame.mixer.Sound.play(click)
    load_data()
    update_entries(current_index)

def next_word():
    global current_index
    if sounds:pygame.mixer.Sound.play(click)
    current_index += 1
    if current_index >= len(greek_words):
        current_index = 0
    update_entries(current_index)
    cur_index.config(text=current_index+1)

def prev_word():
    global current_index
    if sounds:pygame.mixer.Sound.play(click)
    current_index -= 1
    if current_index < 0:
        current_index = len(greek_words) - 1
    update_entries(current_index)
    cur_index.config(text=current_index+1)

def loc_this():
    global root, loc 
    if sounds:pygame.mixer.Sound.play(click)  
    loc=not loc
    if loc==False:
        loc_button.config(bg="light gray", text="L-off")       
    else:
        loc_button.config(bg="light green", text="L-on")  

def find_string():
    global startfrom, a_word, active_list
    found = False
    for i in range(startfrom, len(active_list)):
        if a_word in active_list[i]:
            update_entries(i)
            startfrom = i + 1  # Update startfrom to the next position
            found = True
            break  # Stop after finding the first match
    if not found:
        startfrom = 0  # Reset startfrom if not found

def find_word(selected_option):
    global loc, string_on,active_list,a_word
    if sounds:pygame.mixer.Sound.play(click)
    selected = f"You selected: {selected_option}"
    if selected_option == "Gr":
        a_word=greek_entry.get()
        active_list=greek_words
    elif selected_option == "En":
        a_word=english_entry.get()
        active_list=english_words
    elif selected_option == "It":
        a_word=italian_entry.get()
        active_list=italian_words
    elif selected_option == "Es":
        a_word=spanish_entry.get()
        active_list=spanish_words
    elif selected_option == "Fr":
        a_word=french_entry.get()
        active_list=french_words

    if string_on:
        a_word=the_string.get()
        find_string()
        return

    if not loc:
        index = next((i for i, name in enumerate(active_list) if name.startswith(a_word)), None)
        if index is not None:
            update_entries(index)
        else:
            print("Word not found!")
    else: # locate all words-- New window root2----------
        root2 = tk.Tk()
        root2.title("Dict25 v.3.1 ")
        root2.geometry("220x370")
        root2.configure(bg="#0D5EAF")    # Blue for Greece
        m_text=tk.Text(root2,width=218,height=20,bg="pale green",fg="maroon", font=("Arial",12))
        m_text.grid(row=0,column=9, rowspan=12)
        for i, word in enumerate(active_list):
            if word.startswith(a_word):
                position = active_list.index(word)+1
                m_text.insert(tk.END, f" {word}  >{i+1}#  \n")

def new_set():    # Clear all entries 
    global greek_words, english_words, italian_words, spanish_words, french_words
    if sounds:pygame.mixer.Sound.play(click)
    greek_entry.delete(0, tk.END)
    english_entry.delete(0, tk.END)
    italian_entry.delete(0, tk.END)
    spanish_entry.delete(0, tk.END)
    french_entry.delete(0, tk.END)
    greek_entry.insert(0,"Νέα λέξη")
    english_entry.insert(0,"New word")
    italian_entry.insert(0,"Nuova parola")
    spanish_entry.insert(0,"Nueva palabra")
    french_entry.insert(0,"Nouveau mot")
    cur_index.config(text=len(greek_words)+1)

def append_new_set():
    if sounds:pygame.mixer.Sound.play(click)
    greek_words.append(greek_entry.get())
    english_words.append(english_entry.get())
    italian_words.append(italian_entry.get())
    spanish_words.append(spanish_entry.get())
    french_words.append(french_entry.get())
    cur_index.config(text=len(greek_words))
    print("New set appended!")

def save_changes(): # Save the changes to the lists
    if sounds:pygame.mixer.Sound.play(click)
    greek_words[current_index] = greek_entry.get()
    english_words[current_index] = english_entry.get()
    italian_words[current_index] = italian_entry.get()
    spanish_words[current_index] = spanish_entry.get()
    french_words[current_index] = french_entry.get()
    print("Changes saved!")

def save_to_excel():
    if sounds:pygame.mixer.Sound.play(click)
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Dictionary"
        headers = ["Greek", "English", "Italian", "Spanish", "French"]
        sheet.append(headers)
        for i in range(len(greek_words)):
            row = [
                greek_words[i],
                english_words[i],
                italian_words[i],
                spanish_words[i],
                french_words[i]
            ]
            sheet.append(row)
        workbook.save(file_path)
        print("Data saved to Excel!")
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Dictionary"
    headers = ["Greek", "English", "Italian", "Spanish", "French"]
    sheet.append(headers)

    for i in range(len(greek_words)):
        row = [
            greek_words[i],
            english_words[i],
            italian_words[i],
            spanish_words[i],
            french_words[i]
        ]
        sheet.append(row)
        f_path="xlsx\\"
        f_mane="dictionary.xlsx"
        my_file=f_path+f_mane
    workbook.save(my_file)    
    print("Data saved to Excel!")

def on_close():
    if sounds:pygame.mixer.Sound.play(hit)
    if messagebox.askyesno("Save Changes", "Do you want to save the changes?"):
        save_to_excel()
    root.destroy()

def more(): #resize the window "root" 
    global root, more   
    more=not more
    if sounds:pygame.mixer.Sound.play(menu)
    if more==False:
        more_button.config(bg="light gray", text="Less")
        root.geometry("485x370")
        root.update()       
    else:
        more_button.config(bg="light green", text="More")
        root.geometry("485x280")
        root.update()

def getatriple(the_rnd):
    global v1, v2
    indices = set()
    while len(indices) < 3:
        num = random.randint(v1, v2)
        if num != the_rnd:
            indices.add(num)
    return tuple(indices)

def reset_all():
    global totwtemp,vath
    if sounds:pygame.mixer.Sound.play(hit)
    w1.config(bg="white",text="")
    w2.config(bg="white",text="")
    w3.config(bg="white",text="")
    w4.config(bg="white",text="")
    st_butt.config(state="normal")
    st_butt.config(state="normal")
    sto_butt.config(state="disabled")
    time_butt.config(state="normal")
    tot_butt.config(state="normal")
    chrs_butt.config(state="normal")
    lang_butt.config(state="normal")
    tot_l.config(text=totw)
    totwtemp=totw 
    vath=0 
          
def set_the_set():
    global correct,chrsnow,lex0
    if not timer_running or totwtemp==0:
        reset_all()       
        return
    w1.config(bg="bisque")
    w2.config(bg="bisque")
    w3.config(bg="bisque")
    w4.config(bg="bisque")
    a0=random.randint(0,len(greek_words)-1)
    a0 = random.randint(v1, v2)
    a1,a2,a3 =getatriple(a0)
    lex0=act1lang[a0]
    lex1=act2lang[a0]
    lex2=act2lang[a1]
    lex3=act2lang[a2]
    lex4=act2lang[a3]
    ans_list=[]
    ans_list.extend([lex1, lex2, lex3, lex4])
    rnd_list=ans_list
    random.shuffle(rnd_list)
    w0.config(text=lex0)
    if chrsnow =="full":
        w1.config(text=ans_list[0])
        w2.config(text=ans_list[1])
        w3.config(text=ans_list[2])
        w4.config(text=ans_list[3])
    else:
        w1.config(text=str(ans_list[0])[0:chrsnow])
        w2.config(text=str(ans_list[1])[0:chrsnow])
        w3.config(text=str(ans_list[2])[0:chrsnow])
        w4.config(text=str(ans_list[3])[0:chrsnow])
    correct = lex1

def update_timer():
    global time_left, timer_rem, timer_running,totwtemp
    if timer_running:
        if time_left > 0:
            time_left -= 1
            timer_rem.config(text=str(time_left))
            play_w.after(1000, update_timer)
        else:
            print("Time's up!")
            timer_running=False
            totwtemp=totw
            reset_all()          

def stop():
    global timer_running
    global totwtemp
    if sounds:pygame.mixer.Sound.play(pop)
    timer_running=False
    reset_all()

def close_res_window():
    global res_window
    if res_window is not None and res_window.winfo_exists():  # Αν το παράθυρο υπάρχει
        res_window.destroy()  # Κλείσιμο παραθύρου
        res_window = None  # Reset της μεταβλητής

def start():
    global play_w, w0,w1,w2,w3,w4,langs_selector,res_window,text2
    global flang,slang, act1lang,act2lang,secperw,timer_running
    global time_left,timer_rem,time_butt,vath,err
    global to1,fr1,v1,v2,res_window
    v1 =int( fr1.get())
    v2 = int(to1.get())
    vath_l.config(text=0)
    play_w.geometry("300x340")
    if sounds:pygame.mixer.Sound.play(pop)
    close_res_window()
    # making the Results window -------------------
    res_window = tk.Toplevel(play_w)  # Use Toplevel instead of Tk
    res_window.title("Results")
    res_window.geometry("350x360+500+100")
    text2 = tk.Text(res_window, bg="snow", fg="cyan",font=("arial",12))
    text2.grid(row=0, column=0)
    # Tags-----------------------------
    text2.tag_configure("correct", foreground="blue")
    text2.tag_configure("incorrect", foreground="red")
    lang_butt.config(state="disabled")
    st_butt.config(state="disabled")
    time_butt.config(state="disabled")
    tot_butt.config(state="disabled")
    chrs_butt.config(state="disabled")
    sto_butt.config(state="normal")

    langs_selector=False
    lang1=(flang.get())
    lang2=(slang.get())
    time_left=secperw*totw
    err=0
    err_l.config(text=err)
    timer_running = True
    update_timer()

    # select lang1
    if lang1=="Gr":
        act1lang=greek_words  
    elif lang1=="Fr":
        act1lang=french_words
    elif lang1=="En":
        act1lang=english_words  
    elif lang1=="Es":
        act1lang=spanish_words
    elif lang1=="It":
        act1lang=italian_words

    # select lang2
    if lang2=="Gr":
        act2lang=greek_words  
    elif lang2=="Fr":
        act2lang=french_words
    elif lang2=="En":
        act2lang=english_words  
    elif lang2=="Es":
        act2lang=spanish_words
    elif lang2=="It":
        act2lang=italian_words         
    if timer_running:
        set_the_set()

def endofgame(): # to be ready tomorow
    pass

def check_my_text(event):
    global correct, vath, vath_l,timer_running,err, err_l,chrsnow,lex0
    global res_w,text2,tot_l,totwtemp
    my_ans = event.widget["text"]
    event.widget.config(bg="grey")

    if chrsnow == "full":
        correct_substr = str(correct)
    else:
        correct_substr = str(correct)[:int(chrsnow)]
    
    if my_ans == correct_substr and timer_running:
        totwtemp-=1
        if totwtemp==0:
            endofgame()
            pass
        tot_l.config(text=totwtemp)   
        if sounds:pygame.mixer.Sound.play(corr)
        text2.insert(tk.END, f" {lex0} = {correct}\n", "correct") 
        vath+=1    
        vath_l.config(text=vath) 
        set_the_set()
       
        
    elif timer_running:
        err+=1
        vath-=1
        vath_l.config(text=vath)
        if sounds:pygame.mixer.Sound.play(wrong)
        text2.insert(tk.END, f" {lex0} <===\n", "incorrect")
    #vath_l.config(text=vath)
    err_l.config(text=err)

def langs(window):# resise
    global play_w, langs_selector   
    if sounds:pygame.mixer.Sound.play(pop)
    if langs_selector==False:
        window.geometry("450x340")
        window.update()       
    else:
        window.geometry("300x340")
        window.update() 
    langs_selector=not langs_selector

def sec_w(): # second/word
    global time_l,secperw
    if sounds:pygame.mixer.Sound.play(pop)
    secperw=time_l.cget("text")
    if secperw<9:
        secperw+=1
    else:
        secperw=3
    time_l.config(text=secperw)
    togo=totw*secperw
    timer_rem.config(text=togo)

def chrs(): #chrs / word
    global chrs_l,chrsnow
    if sounds:pygame.mixer.Sound.play(pop)
    chrsnow=chrs_l.cget("text")
    if chrsnow=="full":
        chrsnow=2
    else:
        chrsnow+=1
    if chrsnow==6:
        chrsnow="full"
    chrs_l.config(text=chrsnow)     

def words(): #total words
    global tot_l,totw
    if sounds:pygame.mixer.Sound.play(pop)
    totw=tot_l.cget("text")
    if totw==30:
        totw=10
    else:
        totw+=5
    tot_l.config(text=totw)
    togo=totw*secperw
    timer_rem.config(text=togo)

def up_langs(): # lang selector
    global flang, slang,lang_l
    if sounds:pygame.mixer.Sound.play(pop)
    lang1=(flang.get())
    lang2=(slang.get())
    newstr=lang1+"-"+lang2
    lang_l.config(text=newstr)

def reset_lim():
    global fr1,to1,v1,v2
    v1=1
    v2=len(greek_words)-1
    fr1.delete(0,tk.END)
    to1.delete(0,tk.END)
    fr1.insert(0,v1)
    to1.insert(0,v2)

def play():    # prepare the play window "play_w"
    global root, w0, w1, w2, w3, w4, flang, slang,play_w, lang_butt
    global secperw,timer_rem, totw,totwtemp,tot_butt,st_butt,lang_l,chrs_butt
    global time_l, chrsnow,chrs_l,time_butt,tot_l,sto_butt,vath_l,err_l,err
    global fr1,to1,v1,v2
    v1=1
    v2=len(greek_words)-1
    if sounds:pygame.mixer.Sound.play(play1)
    secperw=3
    totw=totwtemp=10
    chrsnow="full"
    vath=err=0
    togo=totw*secperw
    play_w = tk.Toplevel(root)
    play_w.title("Dict25 --PlayLand")
    play_w.geometry("300x340")
    play_w.configure(bg="plum1") 
    empt1 = tk.Label(play_w, width="1", text="", bg="plum1")
    empt1.grid(row=0, column=0)
    w0 = tk.Label(play_w, width=24, bg="pale green", text="",anchor="w", font=("arial", 14), bd=2, relief="raised")
    w0.grid(row=1, column=1, columnspan=5)
    empt2 = tk.Label(play_w, width="1", text="", bg="plum1")
    empt2.grid(row=2, column=0)
    w1 = tk.Label(play_w, width=24, bg="bisque", text="",anchor="w", font=("arial", 14), bd=1, relief="solid")
    w1.grid(row=3, column=1, columnspan=5)
    w2 = tk.Label(play_w, width=24, bg="bisque", text="", anchor="w",font=("arial", 14), bd=1, relief="solid")
    w2.grid(row=4, column=1, columnspan=5)
    w3 = tk.Label(play_w, width=24, bg="bisque", text="",anchor="w", font=("arial", 14), bd=1, relief="solid")
    w3.grid(row=5, column=1, columnspan=5)
    w4 = tk.Label(play_w, width=24, bg="bisque", text="",anchor="w", font=("arial", 14), bd=1, relief="solid")
    w4.grid(row=6, column=1, columnspan=5)
   
    empt3 = tk.Label(play_w, width="1", text="", bg="plum1")
    empt3.grid(row=0, column=6, rowspan=6)
    options = ["Gr", "En", "It", "Es", "Fr"]
    i = 2
    flang = tk.StringVar(value=options[0])  # Set default value to "Gr"
    for option in options:
        radio = tk.Radiobutton(play_w, text=option, variable=flang, value=option, width=4,command=up_langs)
        radio.grid(row=i, column=7, sticky="w", padx=5, pady=2) 
        i += 1
    empt4 = tk.Label(play_w, width="1", text="", bg="plum1")
    empt4.grid(row=0, column=8, rowspan=6)
    i = 2
    slang = tk.StringVar(value=options[4])  # Set default value to "Fr"
    for option in options:
        radio = tk.Radiobutton(play_w, text=option, variable=slang, value=option,width=4,command=up_langs)
        radio.grid(row=i, column=9, sticky="w", padx=5, pady=2)  
        i += 1
    
    w1.bind("<Button-1>", check_my_text) 
    w2.bind("<Button-1>", check_my_text)  
    w3.bind("<Button-1>", check_my_text)  
    w4.bind("<Button-1>", check_my_text)  

    empt5 = tk.Label(play_w, width="1", text="", bg="plum1")
    empt5.grid(row=9, column=1, columnspan=6)
    
    lang_butt = tk.Button(play_w, width=6, bg="light blue",text="Langs", command=lambda:langs(play_w))
    lang_butt.grid(row=10, column=1)
    chrs_butt = tk.Button(play_w, width=6,bg="dodger blue", text="Chrs", command=lambda:chrs())
    chrs_butt.grid(row=10, column=2)
    time_butt = tk.Button(play_w, width=6,bg="salmon", text="Timer", command=lambda:sec_w())
    time_butt.grid(row=10, column=3)
    tot_butt = tk.Button(play_w, width=6,bg="coral", text="Words", command=lambda:words())
    tot_butt.grid(row=10, column=4)
    st_butt = tk.Button(play_w, width=6, text="Start", command=start)
    st_butt.grid(row=10, column=5)
    sto_butt = tk.Button(play_w, width=6, text="Stop", command=stop,state="disabled")
    sto_butt.grid(row=11, column=5)
    
    lang_l = tk.Label(play_w, width="6", text="Gr-Fr", bg="light blue",bd=2,relief="sunken")
    lang_l.grid(row=11, column=1)
    chrs_l = tk.Label(play_w, width="6", text=chrsnow, bg="dodger blue",bd=2, relief="sunken")
    chrs_l.grid(row=11, column=2)
    time_l = tk.Label(play_w, width="6", text=secperw, bg="salmon", bd=2,relief="sunken")
    time_l.grid(row=11, column=3)
    tot_l = tk.Label(play_w, width="6", text=totw, bg="coral",bd=2,relief="sunken")
    tot_l.grid(row=11, column=4)

    empt6 = tk.Label(play_w, width="1", text="", bg="plum1",font=("Arial",4))
    empt6.grid(row=12, column=0,columnspan=6)

    timer_l= tk.Label(play_w, width="6", text="Time :",fg="white", bg="blue",bd=2,relief="sunken")
    timer_l.grid(row=13, column=1)
    timer_rem = tk.Label(play_w, width="6", text=togo, bg="cyan",bd=2,relief="ridge")
    timer_rem.grid(row=13, column=2)

    score_l=tk.Label(play_w, width="6", text="Score :",fg="white", bg="blue",bd=2,relief="sunken")
    score_l.grid(row=13, column=3)
    vath_l=tk.Label(play_w, width="6", text=vath, bg="cyan",bd=2,relief="ridge")
    vath_l.grid(row=13, column=4)
    err_l=tk.Label(play_w, width="6", text=err, bg="red",fg="yellow",bd=2,relief="ridge")
    err_l.grid(row=13, column=5)
   
    empt7 = tk.Label(play_w, width="1", text="", bg="plum1",font=("Arial",4))
    empt7.grid(row=14, column=0,columnspan=6)

    range1_l=tk.Label(play_w,width=8,text="From :") 
    range1_l.grid(row=15,column=1,columnspan=1)
    range2_l=tk.Label(play_w,width=5,text="  to :") 
    range2_l.grid(row=15,column=3)

    fr1=tk.Entry(play_w,width=6,font=("Arial",10)) #fr1_entryValue>0 and fr_entryValue<len.greek_words
    fr1.grid(row=15,column=2,sticky="w")
    fr1.insert(0,v1)
    to1=tk.Entry(play_w,width=6,font=("Arial",10)) #to1_entryValue>0 and to1_entryValue<len.greek_words
    to1.grid(row=15,column=4,sticky="w")
    to1.insert(0,v2)
    all_b=tk.Button(play_w,text="All",width=6,bg="lime green",command=reset_lim)
    all_b.grid(row=15,column=5)


    play_w.update()

def goto_web(): 
    # Open web pages
    if sounds:pygame.mixer.Sound.play(web)
    root1 = tk.Tk()
    root1.title("Sites to search")
    root1.geometry("540x350")
    root1.configure(bg="#0D5EAF")    # Blue for Greece
    root1.resizable(False, False)
    # Create url for france
    en_list = [ 
        "https://dictionary.cambridge.org/",
        "https://www.merriam-webster.com/"
    ]
    fr_list = [
        "https://dvlf.uchicago.edu/",
        "https://www.larousse.fr/dictionnaires/francais",
        "https://dictionnaire.lerobert.com/fr/",
        "https://www.dictionnaire-academie.fr/",
        "https://fr.wiktionary.org/wiki/Wiktionnaire:Page_principale"
    ]
    # Create url for Spain
    sp_list = [
        "https://dle.rae.es/",
        "https://www.rae.es/dpd/"
    ]
    # Create url for Italy
    it_list = [
        "https://www.dizionario-italiano.it/",
        "https://www.etimo.it/",
        "https://dizionari.corriere.it/"
    ]

    site_names = [
        "Chicago DVLF ",
        "Larousse ", 
        "Le Robert ", 
        "Academie Francaise", 
        "Wiktionnaire ", 
        "Academie Espagnola", 
        "Panhispanico dudas", 
        "Dizionario Olivetti",
        "Etimo ",
        "Corriere della Sera",
        "Cambridge ",
        "Merriam Webster "
    ]  
    # Create buttons for the sites
    # create empty labels
    empty1_label = tk.Label(root1, text="*", width=30,bg="#0D5EAF", font=("Arial", 4))
    empty1_label.grid(row=0, column=0, columnspan=8, padx=10, pady=5)
    #create emtpy columns
    empty2_label = tk.Label(root1, text="*", width=12,bg="#0D5EAF", font=("Arial", 4))
    empty2_label.grid(row=0, column=0 )
    site_list = fr_list + sp_list + it_list + en_list
    i = 1
    for site, name in zip(site_list, site_names):
        site_button = tk.Button(root1, text=name, width=22, command=lambda site=site: webbrowser.open(site), bg="light blue")
        site_button.grid(row=i, column=1)
        address_label = tk.Label(root1, text=site, width=40, font=("Arial", 10), anchor="w", fg="white", bg="#0D5EAF")  # Blue for Greece
        address_label.grid(row=i, column=2)
        i += 1
    root1.mainloop()

def info_on_web():
    global selected_option
    if sounds:pygame.mixer.Sound.play(pop)
    # Open the web page   
    lang=(selected_option.get())
    if mode:
        if lang=="Gr":
            a_word=greek_entry.get() 
            webbrowser.open(f"https://www.wordreference.com/gren/{a_word}")   
        elif lang=="En":
            a_word=english_entry.get() 
            webbrowser.open(f"https://www.wordreference.com/enit/{a_word}")
        elif lang=="It":
            a_word=italian_entry.get() 
            webbrowser.open(f"https://www.wordreference.com/ites/{a_word}")      
        elif lang=="Es":
            a_word=spanish_entry.get() 
            webbrowser.open(f"https://www.wordreference.com/esfr/{a_word}")
        elif lang=="Fr":
            a_word=french_entry.get() 
            webbrowser.open(f"https://www.wordreference.com/frgr/{a_word}") 
    else:
        if lang=="Gr":
            a_word=greek_entry.get() 
            webbrowser.open(f"http://christikolexiko.academyofathens.gr/index.php/anazitisi")   
        elif lang=="En":
            a_word=english_entry.get() 
            webbrowser.open(f"https://www.wordreference.com/definition/{a_word}")
        elif lang=="It":
            a_word=italian_entry.get() 
            webbrowser.open(f"https://www.treccani.it/enciclopedia/ricerca/{a_word}")      
        elif lang=="Es":
            a_word=spanish_entry.get() 
            webbrowser.open(f"https://www.wordreference.com/definicion/{a_word}")
        elif lang=="Fr":
            a_word=french_entry.get() 
            webbrowser.open(f"https://www.littre.org/definition/{a_word}")        

def remover():
    global greek_words, english_words, italian_words, spanish_words, french_words
    if sounds:pygame.mixer.Sound.play(pop)
    greek_words.pop(current_index)
    english_words.pop(current_index)
    italian_words.pop(current_index)
    spanish_words.pop(current_index)
    french_words.pop(current_index)
    print("Word removed!")
    next_word()

def update_sounds(*args):
    global sounds
    sounds = bool(sound_on.get())

def update_mode(*args):
    global mode
    mode = bool(mode_on.get())

def str_mode():
    global root, string_on,startfrom
    if sounds:pygame.mixer.Sound.play(click)  
    
    if string_on:
        string.config(bg="white", text="Str-off")       
    else:
        string.config(bg="yellow green", text="Str-on")  
    string_on=not string_on
    startfrom=0

def go_now(event):
    global current_index
    user_input = len_entry.get()  # Παίρνουμε την τιμή ως string
    try:
        user_input = int(user_input)  # Μετατροπή σε ακέραιο
        if 0 < user_input < len(greek_words):  # Έλεγχος αν είναι εντός ορίων
            current_index=user_input-1
            update_entries(current_index)  # Στέλνουμε τον αριθμό στη συνάρτηση
    except ValueError:
        print("Λάθος: Η τιμή δεν είναι έγκυρος αριθμός!")

# Initialize main window root ------------------
root = tk.Tk()
root.title("Dict25 v.1.3     by PanSoft Hellas")
root.geometry("485x270")
root.configure(bg="#0D5EAF") # Blue for Greece
root.resizable(False, False)
sounds=True
# Load and display the flash image
flash_image = Image.open("pansoft.png")
flash_image = flash_image.resize((485, 270), Image.LANCZOS)
flash_photo = ImageTk.PhotoImage(flash_image)
flash_label = tk.Label(root, image=flash_photo)
flash_label.grid(row=0, column=0, columnspan=9)
root.update()
# Load data
greek_words, english_words, italian_words, spanish_words, french_words = load_data()
current_index = 0

flash_label.grid_forget()

greek_label = tk.Label(root, text="Gr", width=4,font=("Arial", 14), anchor="e",fg="white", bg="#0D5EAF")  # Blue for Greece
greek_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
greek_entry = tk.Entry(root,width=30, font=("Arial", 14))
greek_entry.grid(row=1, column=1, columnspan=7,padx=10, pady=5)

english_label = tk.Label(root, text="En",width=4, font=("Arial", 14), anchor="e",fg="white", bg="#00247D")
english_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
english_entry = tk.Entry(root,width=30, font=("Arial", 14))
english_entry.grid(row=2, column=1, columnspan=7, padx=10, pady=5)

italian_label = tk.Label(root, text="It",width=4, font=("Arial", 14), anchor="e",fg="white", bg="#009246")
italian_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
italian_entry = tk.Entry(root,width=30, font=("Arial", 14))
italian_entry.grid(row=3, column=1, columnspan=7, padx=10, pady=5)

spanish_label = tk.Label(root, text="Sp",width=4, font=("Arial", 14), anchor="e",fg="white", bg="#AA151B")
spanish_label.grid(row=4, column=0,  padx=10, pady=5, sticky="w")
spanish_entry = tk.Entry(root,width=30, font=("Arial", 14))
spanish_entry.grid(row=4, column=1, columnspan=7, padx=10, pady=5)

french_label = tk.Label(root, text="Fr", width=4, font=("Arial", 14), anchor="e",fg="white", bg="#0055A4")
french_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
french_entry = tk.Entry(root,width=30, font=("Arial", 14))
french_entry.grid(row=5, column=1, columnspan=7, padx=10, pady=5)

#  empty labels ---------------  
empty1_label = tk.Label(root, text="*", width=30,bg="#0D5EAF", font=("Arial", 4))
empty2_label = tk.Label(root, text="*", width=30,bg="#0D5EAF", font=("Arial", 4))
empty3_label = tk.Label(root, text="*", width=30,bg="#0D5EAF", font=("Arial", 4))
empty4_label = tk.Label(root, text="*", width=30,bg="#0D5EAF", font=("Arial", 4))
empty3_label.grid(row=8, column=0, columnspan=8, padx=10, pady=5)
empty1_label.grid(row=0, column=0, columnspan=8, padx=10, pady=5)
empty2_label.grid(row=6, column=0, columnspan=8, padx=10, pady=5)
empty3_label.grid(row=8, column=0, columnspan=8, padx=10, pady=5)
empty4_label.grid(row=10, column=0, columnspan=8, padx=10, pady=5)
# row 7---------
prev_button = tk.Button(root, text="Prev", width=5,command=prev_word, bg="light blue")
prev_button.grid(row=7, column=4)
cur_index = tk.Label(root,width=5, text=0, bg="pale green", font=("Arial", 12))
cur_index.grid(row=7, column=5)

next_button = tk.Button(root, text="Next", width=5,command=next_word, bg="light blue")
next_button.grid(row=7, column=6)
search_button = tk.Button(root, text="Find", width=5,command=lambda: find_word(selected_option.get()), bg="light yellow")
search_button.grid(row=7, column=7)

Info_button = tk.Button(root, text="Web >",width=5, command=info_on_web, bg="light pink")
Info_button.grid(row=7, column=8)
more_button = tk.Button(root, text="More", width=5,command=more, bg="light gray")
more_button.grid(row=7, column=0)
file_entry = tk.Entry(root, width=14, font=("Arial", 10), fg="white", bg="#0D5EAF", justify="center")
file_entry.grid(row=7, column=1, columnspan=2, padx=0, pady=0)
len_entry = tk.Entry(root, width=5, font=("Arial", 10), fg="white", bg="#0D5EAF", justify="center")
len_entry.grid(row=7, column=3, padx=0, pady=0)
len_entry.bind("<Return>", go_now)  # Δέσιμο του πλήκτρου Enter
# row 9---------
open_button = tk.Button(root, text="Open", width=5,command=alter_dict, bg="coral")
open_button.grid(row=9, column=0)
play_button = tk.Button(root, text="Play", width=5,command=play, bg="light sky blue")
play_button.grid(row=9, column=1)
loc_button = tk.Button(root, text="L-off", width=5,command=loc_this, bg="light sky blue")
loc_button.grid(row=9, column=2)
adv_button = tk.Button(root, text="Search", width=5,command=goto_web, bg="light sky blue")
adv_button.grid(row=9, column=3)

new_button = tk.Button(root, text="New",width=5, command=new_set, bg="light coral")
new_button.grid(row=9, column=4)
append_button = tk.Button(root, text="Add", width=5,command=append_new_set, bg="light salmon")
append_button.grid(row=9, column=5)
save_button = tk.Button(root, text="Save", width=5,command=save_changes, bg="light sky blue")
save_button.grid(row=9, column=6)
clear_button = tk.Button(root, text="Clear",width=5, command=remover, bg="red",fg="yellow")
clear_button.grid(row=9, column=7)
write_button = tk.Button(root, text="Write",width=5, command=save_to_excel, bg="light green")
write_button.grid(row=9, column=8)

sound_on = tk.IntVar(value=1)
sound_on.trace_add("write", update_sounds)
sound_onoff_button = tk.Checkbutton(root, text=" Sound",width=7, variable=sound_on)
sound_onoff_button.grid(row=11, column=0, columnspan=2,sticky="w")
if sound_on:pygame.mixer.Sound.play(hit)

mode_on = tk.IntVar(value=1)
mode_on.trace_add("write", update_mode)
mode_onoff_button = tk.Checkbutton(root, text=" Mode",width=7, variable=mode_on)
mode_onoff_button.grid(row=11, column=1, columnspan=2,sticky="w")

string=tk.Button(root,text="Str-off",width=6, command=str_mode, bg="white")
string.grid(row=11,column=3,columnspan=2,sticky="w")
nextstr=tk.Button(root,text=">",width=4, 
                  command=lambda: find_word(selected_option.get()), bg="yellow green")
nextstr.grid(row=11,column=6,sticky="w")

the_string=tk.Entry(root,width=14,font=("Arial",10),bg="pale green")
the_string.grid(row=11,column=4,sticky="e",columnspan=2)

options = ["Gr", "En", "It", "Es", "Fr"]
i = 1
selected_option = tk.StringVar(value=options[0])  # Set default value to "Gr"
for option in options:
    radio = tk.Radiobutton(root, text=option, variable=selected_option, value=option)
    radio.grid(row=i, column=8, columnspan=6)#, padx=10, pady=5)
    i += 1

# Initialize labels with the first word
if greek_words:
    update_entries(current_index)
    
# Start the main loop
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()