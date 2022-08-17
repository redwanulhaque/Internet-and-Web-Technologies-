# CSCI 355/655
# Summer 2022
# Assignment 3 - HTML and CSS
# Redwanul Haque


import webbrowser
import os
import requests
from bs4 import BeautifulSoup


TAG_DOCTYPE = '<!DOCTYPE html>'
TAG_HTML = 'html'
TAG_HEAD = 'head'
TAG_BODY = 'body'
TAG_TABLE = 'table'
TAG_TH = 'th'
TAG_TD = 'td'
TAG_TR = 'tr'
TAG_PAR = 'p'
TAG_H1 = 'h1'
TAG_BR = 'br'
TAG_LINK = 'link'
TAG_A = 'a'

def create_element(tag, content, attributes="", end_tag=True):
    element = "<" + tag + " " + attributes + ">"
    if end_tag:
        element += content + "</" + tag + ">"
    return element + "\n"

def create_elements(tag, list_contents):
    elements = ""
    for content in list_contents:
        elements += create_element(tag, content)
    return elements


def create_table(headers, data):
    rows = create_elements(TAG_TH, headers)
    for datum in data:
        name = datum[0]
        href = 'href="https://en.wikipedia.org/wiki/' + name.replace(" ", "_") + '_(state)' + '"'
        a = create_element(TAG_A, name, href, True)
        tda = create_element(TAG_TD, a)
        tds = create_elements(TAG_TD, datum[1:])
        row = create_element(TAG_TR, tda + tds)
        rows += row
    table = create_element(TAG_TABLE, rows)
    return table


def open_file_in_browser(file_name):
    url = 'file:///' + os.getcwd() + '/' + file_name
    webbrowser.open_new_tab(url)


def write_file(file_name, message):
    f = open(file_name, 'w')
    f.write(message)
    f.close()


def get_state_data():
    url = 'https://www.thespreadsheetguru.com/blog/list-united-states-capitals-abbreviations'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    items = soup.find_all('p')
    state_data = ""
    capital_data = ""
    abbr_data = ""
    for item in items:
        if "Alabama" in item:
            state_data = str(item)
        if "NJ" in item:
            abbr_data = str(item)
        if "Juneau" in item:
            capital_data = str(item)
    state_data = state_data[state_data.index("Alabama"):].split("<br/>")
    abbr_data = abbr_data[abbr_data.index("AL"):].split("<br/>")
    capital_data = capital_data[capital_data.index("Montgomery"):].split("<br/>")
    states = [[state_data[i], abbr_data[i], capital_data[i]] for i in range(50)]
    return states


def main():
    states = get_state_data()
    headers = ["State", "Abbreviation", "Capital"]
    table = create_table(headers, states)
    heading = create_element(TAG_H1, "Redwanuls United States")
    link_attributes = 'rel="stylesheet" href="style/myStyle.css"'
    link = create_element(TAG_LINK, "", link_attributes, end_tag=False)
    head = create_element(TAG_HEAD, link)
    body = create_element(TAG_BODY, heading + table)
    message = create_element(TAG_HTML, head + body)
    write_file("states.html", message)
    open_file_in_browser("states.html")


if __name__ == "__main__":
    main()