'''
ASCII was an American-developed standard, so it only defined unaccented characters.
There was an ‘e’, but no ‘é’ or ‘Í’. This meant that languages which required accented
characters couldn’t be faithfully represented in ASCII.

Unicode started out using 16-bit characters instead of 8-bit characters.
16 bits means you have 2^16 = 65,536 distinct values available, making it possible
to represent many different characters from many different alphabets;
an initial goal was to have Unicode contain the alphabets for every single human language.

'''

#To get a webpage
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
from random import choice

#initialization of variables
URL = 'http://pinyin.info/unicode/diacritics.html'
request_to_page = requests.get(URL)
dict_list = defaultdict(list)
def_dict = {}

#start (scarping)
if request_to_page.status_code == 200:
    #soup contains the HTML of the page
    soup = BeautifulSoup(request_to_page.text, 'html.parser')

    #find method will get the table element
    table = soup.find('table')

    # find_all finds all the tr & td element
    for line in table.find_all('tr'):
        field = line.find_all('td')

        if len(field) == 4:
            #field[0]-> unique number
            #field[1]-> symbols
            #field[2]-> accents
            #field[3]-> description
            symbol = field[1].text
            descr = field[3].text

            #regex to get a text in 'capital O' from 'capital O with BREVE'
            regex_text = re.search(r'((lowercase|capital)\s+\S\b)', descr)

            if regex_text:
                '''
                index contains 
                ...
                capital G
                capital G
                capital G
                capital H
                capital H
                capital H
                ...
                '''
                index = regex_text.group(0)

                #to the particular index append symbols in form of list like
                #'lowercase T': ['t', 'ť', 'ţ', 'ṱ', 'ț', 'ẗ', 'ṭ', 'ṯ', 'ʈ', 'ŧ']
                dict_list[index].append(symbol)

                #Doing other way round
                def_dict[symbol] = index

#scraping ends

#​ function for obfuscating the string
def obfuscate(s):
    output_text = ''
    for i in s:
        if i in def_dict:
            #def_dict['S']= capital S and dict_list['capital S']=['S', 'Ś',...]
            output_text = output_text + choice(dict_list[def_dict[i]])
        else:
            output_text = output_text +  i
    return output_text

input_text='For,​ ​after​ ​all,​ ​how​ ​do​ ​we​ ​know​ ​that​ ​two​ ​and​ ​two​ ​make​ ​four? ' \
           'Or​ ​that​ ​the​ ​force​ ​of​ ​gravity​ ​works?​ ​Or​ ​that​ ​the​ ​past​ ​is​ ​unchangeable?' \
           'If​ ​both​ ​the​ ​past​ ​and​ ​the​ ​external​ ​world​ ​exist​ ​only​ ​in​ ​the​ ​mind,' \
           'and​ ​if​ ​the​ ​mind​ ​itself​ ​is​ ​controllable​ ​–​ ​what​ ​then?'

print ("Diactriticized​ String(from code): "+obfuscate(input_text))
print('\n')
manual_input=input("Plain String: ")
print ("Diactriticized​ String: "+obfuscate(manual_input))
