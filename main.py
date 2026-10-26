import json



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
         T_id = input("Input Ticket_ID   ").lower()
         if T_id.strip() == "":
            print("Empty Id: Input your ticket id\n")
            continue
         T_description = input("\nDescribe Your Problem  ").lower()
         if T_description.strip() == "":
             print("Empty Description: describe your problem\n")
         else:
             break

    
    reading = load_ticket(ticket)
    reading.append({"T_id": T_id, "T_description": T_description})
    save_ticket(reading)

Create_Tickets()

