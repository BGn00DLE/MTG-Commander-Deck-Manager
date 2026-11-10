import tkinter as tk
import json
import os
from tkinter import messagebox


def save_decks():
    with open("decks.json", "w") as file:
        json.dump(decks, file, indent=4)


def load_decks():
    if os.path.exists("decks.json"):
        with open("decks.json", "r") as file:
            return json.load(file)

    return {}


decks = load_decks()
last_card_change: tuple[str, str, int | None] | None = None


def refresh_deck_dropdown():
    menu = deck_dropdown["menu"]
    menu.delete(0, "end")

    for deck_name in decks:
        menu.add_command(
            label=deck_name,
            command=lambda name=deck_name: selected_deck.set(name)
        )


def select_deck_manually():
    deck_name = manual_deck_entry.get().strip()

    if deck_name not in decks:
        messagebox.showwarning(
            "Deck Not Found",
            "Please enter the name of an existing deck."
        )
        return

    selected_deck.set(deck_name)
    messagebox.showinfo(
        "Deck Selected",
        f"Selected deck: {deck_name}"
    )


def create_deck():
    deck_name = deck_name_entry.get().strip()
    commander = commander_entry.get().strip()

    if not deck_name or not commander:
        messagebox.showwarning("Missing Information",
                               "Please enter both a deck name and commander.")
        return

    if deck_name in decks:
        messagebox.showwarning("Duplicate Deck",
                               "A deck with that name already exists.")
        return

    decks[deck_name] = {
        "commander": commander,
        "cards": {}
    }
    save_decks()
    refresh_deck_dropdown()

    messagebox.showinfo(
        "Success",
        f"Deck '{deck_name}' created successfully!"
    )


def add_card():
    global last_card_change

    deck_name = selected_deck.get()
    card_name = card_name_entry.get().strip()
    quantity = quantity_entry.get().strip()

    if deck_name not in decks:
        messagebox.showwarning(
            "No Deck Selected",
            "Please select a deck before adding cards."
        )
        return

    if not card_name:
        messagebox.showwarning(
            "Missing Card Name",
            "Please enter a card name."
        )
        return

    if not quantity.isdigit() or int(quantity) < 1:
        messagebox.showwarning(
            "Invalid Quantity",
            "Please enter a positive whole number."
        )
        return

    previous_quantity = decks[deck_name]["cards"].get(card_name)

    if previous_quantity is not None:
        confirmed = messagebox.askyesno(
            "Replace Card Quantity?",
            f"{card_name} currently has {previous_quantity} copies.\n"
            f"Replace that quantity with {quantity}?"
        )

        if not confirmed:
            return

    last_card_change = (deck_name, card_name, previous_quantity)

    decks[deck_name]["cards"][card_name] = int(quantity)
    save_decks()

    messagebox.showinfo(
        "Success",
        f"Added {quantity}x {card_name} to {deck_name}!"
    )


def undo_last_card_change():
    global last_card_change

    if last_card_change is None:
        messagebox.showinfo(
            "Nothing to Undo",
            "No card changes to undo"
        )
        return

    deck_name, card_name, previous_quantity = last_card_change

    if previous_quantity is None:
        del decks[deck_name]["cards"][card_name]
    else:
        decks[deck_name]["cards"][card_name] = previous_quantity

    save_decks()
    last_card_change = None

    messagebox.showinfo(
        "Undo Successful",
        f"Last change to {card_name} has been undone."
    )


def view_decklist():
    deck_name = selected_deck.get()

    if deck_name not in decks:
        messagebox.showwarning(
            "No Deck Selected",
            "Please select a deck to view"
        )
        return

    deck = decks[deck_name]

    deck_window = tk.Toplevel(root)
    deck_window.title(f"Decklist - {deck_name}")
    deck_window.geometry("400x500")

    tk.Label(
        deck_window,
        text=deck_name,
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    tk.Label(
        deck_window,
        text=f"Commander: {deck['commander']}"
    ).pack(pady=5)

    for card_name, quantity in deck["cards"].items():
        tk.Label(
            deck_window,
            text=f"{quantity}x {card_name}"
        ).pack()


root = tk.Tk()
root.title("MTG Commander Deck Manager")
root.geometry("800x800")

title_label = tk.Label(
    root,
    text="MTG Commander Deck Manager",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=20)

tk.Label(
    root,
    text="Step 1: Create a deck -> Step 2: Select a deck -> Step 3: Add cards -> Step 4: View your decklist",
    font=("Arial", 10)
).pack(pady=5)

deck_name_label = tk.Label(root, text="Deck Name:")
deck_name_label.pack(pady=5)

deck_name_entry = tk.Entry(root, width=40)
deck_name_entry.pack(pady=5)

commander_label = tk.Label(root, text="Commander:")
commander_label.pack(pady=5)

commander_entry = tk.Entry(root, width=40)
commander_entry.pack(pady=5)

create_deck_button = tk.Button(
    root,
    text="Create Deck",
    command=create_deck
)
create_deck_button.pack(pady=15)

tk.Label(
    root,
    text="Create and save a new commander deck for organizing your cards.",
    font=("Arial", 9)
).pack(pady=2)

select_deck_label = tk.Label(root, text="Select a Deck:")
select_deck_label.pack(pady=5)

selected_deck = tk.StringVar(root)
selected_deck.set("Select a deck")

deck_dropdown = tk.OptionMenu(root, selected_deck, *decks.keys())
deck_dropdown.pack(pady=5)

tk.Label(
    root,
    text="Or enter an existing deck name:",
    font=("Arial", 9)
).pack(pady=2)

manual_deck_entry = tk.Entry(root, width=40)
manual_deck_entry.pack(pady=5)

manual_select_button = tk.Button(
    root,
    text="Select Typed Deck",
    command=select_deck_manually
)
manual_select_button.pack(pady=5)

card_name_label = tk.Label(root, text="Card Name:")
card_name_label.pack(pady=5)

card_name_entry = tk.Entry(root, width=40)
card_name_entry.pack(pady=5)

quantity_label = tk.Label(root, text="Quantity:")
quantity_label.pack(pady=5)

quantity_entry = tk.Entry(root, width=10)
quantity_entry.pack(pady=5)

tk.Label(
    root,
    text="Note: Adding an existing card again replaces its saved quantity.",
    font=("Arial", 9)
).pack(pady=2)

add_card_button = tk.Button(
    root,
    text="Add Card",
    command=add_card
)
add_card_button.pack(pady=15)

undo_button = tk.Button(
    root,
    text="Undo Last Card Change",
    command=undo_last_card_change
)
undo_button.pack(pady=5)

tk.Label(
    root,
    text="Add cards to your selected deck and save them for future sessions.",
    font=("Arial", 9)
).pack(pady=2)

view_deck_button = tk.Button(
    root,
    text="View Decklist",
    command=view_decklist
)
view_deck_button.pack(pady=10)

tk.Label(
    root,
    text="View your saved Commander deck and all its cards at any time.",
    font=("Arial", 9)
).pack(pady=2)

root.mainloop()