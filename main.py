import json
from ai_response import show_suggestions

red = "\033[31;1m"
yellow = "\033[33;1m"
green = "\033[32;1m"
reset = "\033[0m"

def load_ticket(tickets):
    try:
     with open("tickets.json", "r")as f:
        ticket = json.load(f)
        return ticket
    except FileNotFoundError:
        return []



def save_ticket(tickets):
    with open("tickets.json", "w")as f:
        json.dump(tickets, f, indent=2)




def Create_Tickets():
    ticket = []
    while True:
         T_id = input(f"{yellow}Input Ticket_ID{reset}   ").lower()
         if T_id.strip() == "":
            print(f"{yellow}Empty Id: Input your ticket id{reset}\n")
            continue
         T_description = input(f"\n{yellow}Describe Your Problem{reset}  ").lower()
         

         if T_description.strip() == "":
             print(f"{red}Empty Description: describe your problem{reset}\n")
         else:
             break
        
             

    reading = load_ticket(ticket)
    reading.append({"T_id": T_id, "T_description": T_description})
    save_ticket(reading)
    show_suggestions(reading[-1])
    
Create_Tickets()

