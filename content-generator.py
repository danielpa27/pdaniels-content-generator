import tkinter as tk
import wikipedia as wiki
import sys
import csv
from multiprocessing import Process
import os
import time
from states import states


def listen():

    file_path = 'state.csv'
    while not os.path.exists(file_path):
        time.sleep(1)

    read_state()
    os.remove(file_path)
    l = Process(target=listen)
    l.start()


def read_state():

    # read input.csv
    with open('state.csv', newline='') as input_file:
        input_reader = csv.reader(input_file)
        # split rows
        rows = list(input_reader)
        # get and split keywords
        state = rows[1][0]
        year = rows[1][1]

        # create output.csv
        write_state(state, year, generate(state, year))
        del input_file


def write_state(pk, sk, txt):
    """Exports generated text and keywords to output.csv

    Args:
        pk (string): primary keyword
        sk (string): secondary keyword
        txt (string): generated text
    """

    with open('state_content.csv', 'w', newline='') as output:
        output_writer = csv.writer(output)
        # header row
        output_writer.writerow(['input_keywords', 'output_content'])
        # content
        output_writer.writerow([pk, sk, txt])


def check_if_state(pk):

    if pk in states:
        with open('get_pop.csv', 'w', newline='') as output:
            output_writer = csv.writer(output)
            # header row
            output_writer.writerow(['input_state', 'input_year'])
            # content
            output_writer.writerow([pk, '2019'])
        return True


def get_pop():

    file_path = 'read_pop.csv'
    while not os.path.exists(file_path):
        time.sleep(1)

    with open('read_pop.csv', newline='') as input_file:
        input_reader = csv.reader(input_file)
        # split rows
        rows = list(input_reader)
        # get and split keywords
        pop = rows[1][0]
        year = rows[1][1]

        # create output.csv

        del input_file


def generate(pk, sk):
    """Uses python wikipedia library to return the first paragraph on the page
    matching the pk that also contains the sk.

    Args:
        pk (string): primary keyword
        sk (string): secondary keyword

    Returns:
        string: generated text
    """

    # get wiki page and split into list of paragraphs
    page = wiki.WikipediaPage(pk)
    paragraphs = page.content.split("\n")

    if sk == '':
        return paragraphs[0]

    # avoid matching words containing sk
    sk = " " + sk + " "

    # search paragraph list for pk and sk and display paragraph if found
    i = 0
    while i < len(paragraphs):
        if pk in paragraphs[i] and sk in paragraphs[i]:
            return paragraphs[i]
        i += 1

    # not found
    return paragraphs[0]


def gen_btn():
    """Calls generate and displays returned text. Calls export_csv with 
    inputted keywords and generated text.
    """

    # get keywords
    pk = ent_PK.get()
    sk = ent_SK.get()

    # generate and display text
    txt = generate(pk, sk)
    txt_gen.delete(1.0, tk.END)
    txt_gen.insert(tk.END, txt)

    # write to output.csv
    export_csv(pk, sk, txt)


def export_csv(pk, sk, txt, pop=""):
    """Exports generated text and keywords to output.csv

    Args:
        pk (string): primary keyword
        sk (string): secondary keyword
        txt (string): generated text
    """

    with open('output.csv', 'w', newline='') as output:
        output_writer = csv.writer(output)
        # header row
        output_writer.writerow(['input_keywords', 'output_content'])
        # content
        output_writer.writerow([pk + ";" + sk, txt, pop])


def cmd_input():
    """Reads input.csv and calls generate in a export_csv call
    to write the generated content to output.csv
    """

    # read input.csv
    with open(sys.argv[1], newline='') as input_file:
        input_reader = csv.reader(input_file)
        # split rows
        rows = list(input_reader)
        # get and split keywords
        keywords = rows[1][0].split(";")
        pk = keywords[0]
        sk = keywords[1]

        if check_if_state(pk):
            return
        # create output.csv
        export_csv(pk, sk, generate(pk, sk))


if __name__ == '__main__':

    l = Process(target=listen)
    l.start()
    # check for input.csv
    if len(sys.argv) > 1:
        cmd_input()

    else:
        # create window
        window = tk.Tk()
        window.title("Content Generator")

        # configure window layout
        window.rowconfigure(0, minsize=100, weight=1)
        window.rowconfigure(1, minsize=600, weight=1)
        window.columnconfigure(0, minsize=700, weight=1)

        # create input frame and text widgets
        txt_gen = tk.Text(window, bg="#f0f8ff")
        fr_input = tk.Frame(window, bg="#80a3dd")

        # label, entry, button widgets
        lbl_PK = tk.Label(fr_input, text="Primary Keyword: ", bg="#80a3dd")
        lbl_SK = tk.Label(fr_input, text="Secondary Keyword: ", bg="#80a3dd")
        ent_PK = tk.Entry(fr_input, width=30)
        ent_SK = tk.Entry(fr_input, width=30)
        btn_submit = tk.Button(
            fr_input,
            text="Generate!",
            command=gen_btn)

        # input frame grid
        lbl_PK.grid(row=0, column=0, sticky="w", pady=15, padx=5)
        ent_PK.grid(row=0, column=1, sticky="w")
        lbl_SK.grid(row=0, column=2, sticky="w", pady=15, padx=5)
        ent_SK.grid(row=0, column=3, sticky="w")
        btn_submit.grid(row=0, column=4, sticky="ew", padx=15)

        # window grid
        fr_input.grid(row=0, column=0, sticky="nsew")
        txt_gen.grid(row=1, column=0, sticky="nsew")

        window.mainloop()
