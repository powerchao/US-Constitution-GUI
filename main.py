import re
import pandas as pd
import tkinter as tki

with open("constitution.txt", mode="r") as constitution:
    contents = constitution.read()

amendmentRegex = re.compile(r'''(   #Opening ( begins definition of group 1 and guarantees it will contain the entire capture
    \n
    (\w+\sAmendment)                #Group 2 contains the ordered number and word 'Amendment'
    \n+
    ((Section)?                     #Checking if amendment has sections and beginning definition of group 3
        (   
            \s* 
            Section\s\d+            #Capture 'Section n' and associated section text
            \s*
            .*            
        )+                          #Try capturing another section as many times as possible. First success is guaranteed by conditions checked above
        |                           #If amendment has no sections, capture next line
        .*
    )                               #End capturing of group 3, which now contains all body text of amendment
    )''', re.VERBOSE)

amendment_results = amendmentRegex.findall(contents)

amendment_dict = {
    "amendment": [item[1] for item in amendment_results],
    "content": [item[2] for item in amendment_results],
}

amendment_pd = pd.DataFrame(amendment_dict)

amend_opts = amendment_pd.amendment.to_list()

app_win = tki.Tk()
app_win.minsize(height=300, width=500)
app_win.title("Constitutional Amendments")

text_field = tki.Label(height=50, width=60, wraplength=400)

amend_var = tki.StringVar(app_win)
amend_var.set(amend_opts[0])

def menu_select(value):
    target_text = amendment_pd[amendment_pd['amendment'] == value]
    text_field.config(text=target_text.content.item())

amendment_select = tki.OptionMenu(app_win, amend_var, *amend_opts, command=menu_select)
amendment_select.pack()

text_field.pack()

app_win.mainloop()

