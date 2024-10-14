import csv
import os
from datetime import datetime
import curses
from curses import wrapper

print("Budeš zadávat název datasetu otázek. Pro ukončení napiš \"0\"")
nazev = input("Název datasetu: ")

#directory
if nazev!="0":
    os.makedirs("datasety", exist_ok=True)
    if not os.path.exists(f"{nazev}.csv"):
        nazev = nazev
    else:
        print("existuje")
        #...
else:
    exit()

s = {}

print("Zadávání začalo. Pro ukončení a uložení napiš \"stop\". Pro smazání poslední napsané dvojice napiš \"del\".")
i="0"
while i != "stop":


    otazka = input("Zadej otázku: ")
    if otazka == "stop":
        i="stop"
        continue

    if otazka == "del" and len(s) !=0:
        smazano = s.pop()
        print(f"Smazal jsi otázku: \"{smazano.keys()}\" a k ní odpověď \"{smazano.values()}\"")

    else:
        odpoved = input("Zadej odpověď: ")
        #formatuje na rok-mesic-den
        last_review_date=datetime.now().strftime("%Y-%m-%d-%H:%M") #ted
        times_reviewed=0 #jeste nebylo reviewed
        factor = 1.0 #zakladni
        s[otazka] = {
            "odpoved":odpoved,
            "last_review_date":last_review_date,
            "times_reviewed":times_reviewed,
            "factor":factor,
            "times_correct":0,
            "times_wrong":0,
            "correct_streak":0,
            "next_review_date":last_review_date,
        }

if len(s)>0:
    with open(f"datasety/{nazev}.csv","a+",newline="") as csv_file:
        writer=csv.writer(csv_file)
        print(s.items())
        for key, value in s.items():
            writer.writerow([key,value["odpoved"], value["last_review_date"], value["times_reviewed"], value["factor"], value["times_correct"], value["times_wrong"], value["correct_streak"], value["next_review_date"]])




    




