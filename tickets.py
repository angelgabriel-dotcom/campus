import json


def save_ticket(tickets):
    with open("tickets.json", "w")as f:
        json.dump(tickets, f, indent=2)

def load_ticket():
    try:
     with open("tickets.json", "r")as f:
        ticket = json.load(f)
        return ticket
    except FileNotFoundError:
        return []
       



reading = load_ticket()
reading.append({"id": "F200", "description": "laptop"})
save_ticket(reading)

