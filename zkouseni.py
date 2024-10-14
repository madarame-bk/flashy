import os
import csv
import random
import subprocess
import sys
from datetime import datetime
from datetime import timedelta
import curses
from curses import wrapper

def get_question(flashcard):
    #question = random.choice(list(flashcard.keys()))
    #return question

    now = datetime.now().strftime("%Y-%m-%d-%H:%M")
    relevant_cards={}

    for question, data in flashcard.items():
        if data["next_review_date"] <= now:
            relevant_cards[question] = data

    if relevant_cards:
        return random.choice(list(relevant_cards.keys()))
    else:
        return None
    


nazev=""
s={}
def main(nazev,s):

    #print("Teď zadáš název datasetu ze kterého chceš test. Pro ukončení napiš \"0\"")
    nazev = input("Z jakého datasetu se chceš nechat vyzkoušet? ")

    s={}

    if nazev!=0:
        if os.path.exists(f"datasety/{nazev}.csv"):
            print(f"Dataset {nazev} nalezen!")

            with open(f"datasety/{nazev}.csv","r") as csv_file:
                reader=csv.reader(csv_file)
                for row in reader:
                    key=row[0]
                    s[key]={
                        "odpoved":row[1],
                        "last_review_date":row[2],
                        "times_reviewed":int(row[3]),
                        "factor":float(row[4]),
                        "times_correct":int(row[5]),
                        "times_wrong":int(row[6]),
                        "correct_streak":int(row[7]),
                        "next_review_date":row[8],
                    }
        else:
            print("Daný dataset neexistuje. Chceš ho vytvořit?")
            odpoved = input("y/n: ")
            if odpoved=="y":
                subprocess.run(["python", "zadavani.py"])
                sys.exit()
            else:
                subprocess.run(["python", "zkouseni.py"])
                sys.exit()
    else:
        exit()

    i=""
    print("Začínáme zkoušet! Pro ukončení při odpovědi napiš \"stop\"")
    while i!="0":
        otazka = get_question(s)
        if otazka is None:
            print("A je to! Pro teď jsi zvládl všechny otázky. Pro zopakování se můžeš vrátit později. Nezapomeň si zopakovat ostatní datasety.")
            break
        print(otazka)
        odpoved=input("Víš odpověď? (y/n): ")

        if odpoved=="stop":
            i="0"
            continue

        if odpoved=="y":
            s[otazka]['correct_streak']+=1
            s[otazka]['times_correct']+=1
            interval_days = 2**s[otazka]["correct_streak"]

        if odpoved=="n":
            s[otazka]['correct_streak']=0
            s[otazka]['times_wrong']+=1
        
        next_review_date = datetime.now() + timedelta(days=interval_days)
        s[otazka]['next_review_date']=next_review_date.strftime("%Y-%m-%d-%H:%M")
        #print(f"strftime: {s[otazka]['next_review_date']}")
        print(f"Odpověď: {s[otazka]['odpoved']}")
        s[otazka]['last_review_date']=datetime.now().strftime("%Y-%m-%d-%H:%M")
        s[otazka]['times_reviewed']=int(s[otazka]['times_reviewed'])+1
        s[otazka]['factor']=1

        with open(f"datasety/{nazev}.csv", "w",newline="") as csv_file:
            writer=csv.writer(csv_file)
            for key, values in s.items():
                writer.writerow([key, values["odpoved"], values["last_review_date"], values["times_reviewed"], values["factor"],values["times_correct"], values["times_wrong"], values["correct_streak"], values["next_review_date"]])

    
main(nazev,s)

