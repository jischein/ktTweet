import requests
import os
from bs4 import BeautifulSoup
import re
import time
import math
import markovify
import utils
from PyDictionary import PyDictionary
dictionary = PyDictionary()

filename = "ktt.txt"
count=0
def grab_threads():
### Grabs x most recent KTT threads ###
    threadLinks = []
    source_page = requests.get('http://www.kanyetothe.com/forum/')
    soupy = BeautifulSoup(source_page.text, 'html.parser')
    posts = soupy.find_all('span', attrs={'class': 'cb_article_title'})
    for post in posts:

        text = post.find_all('a', href=True)
        for elem in text:
            link = str(elem.get('href'))
            if (link[54] == '.'):
                link = link[:54]
            else:
                link = link[:55]
            threadLinks.append(link)
    return list(set(threadLinks))

def len_thread(link):
    source_page = requests.get(link)
    soupy = BeautifulSoup(source_page.text, 'html.parser')
    numPage = soupy.find_all(
        'a',
        attrs={'class': 'navPages'}
    )
    if numPage == []:
        return 1
    else:
        finalNum = (numPage[len(numPage)-1].find(text=True))
        return finalNum

def grab_text(links,count):
    final =[]
    for link in links:
        dec = 0
        print(link)
        print('!!!!!!!!!!!!!!!!!!!!')
        k = int(len_thread(link))
        if (k>1000):
            k = 1000
            dec = 40
        else:
            dec = 10
        while (k > 0):

            startNum = ((k-1) * 18)
            url = (link +'.' + str(startNum))
            source_page = requests.get(link +'.' + str(startNum))
            soupy2 = BeautifulSoup(source_page.text, 'html.parser')
            quotes=[
                quote for quote in soupy2.find_all(
                    'div',
                    attrs={'class': 'post_body'})]


            for quote in quotes:
                text = quote.find_all(text=True)
                if (len(text) > 3):
                    textBod = str(text[3]).lower()
                    textBod = textBod.replace('google_ad_section_end', '')
                    textBod = re.sub(':.+:' '\s+', '', textBod)
                    textBod = re.sub(r'^https?:\/\/.*[\r\n]*', '', textBod)
                    textBod = re.sub('\*.+', '', textBod)
                    ###filter out links and google_ad_section_end
                    if (textBod != ' google_ad_section_end ' and (textBod != '')):
                        final.append(textBod)
                        print(textBod,k)



            k-=dec
    final = list(set(final))
    return final
def write_to(text):
    with open(filename, 'wb') as f:
        for line in text:
            f.write(line.encode('utf-8'))
            f.write('\n'.encode('utf-8'))  # separate quotes

def gen_tweet():
    with open(filename, encoding='utf-8') as f:
        text = f.read()


    text_model = markovify.Text(text)

    sentence = text_model.make_short_sentence(120)  # generate short tweet

    # synonymset = dictionary.synonym('happy')
    # synonym = choice(synonymset)

    return sentence.encode('utf-8')


start_time = time.time()
# threads = grab_threads()
# for thread in threads:
#     print (thread)
# quotes = grab_text(threads,count)
# print('***********DONE:-)**********')
# write_to(quotes)
# print('TIME OF RUN*****' + str(time.time()-start_time) + '*****')
for i in range(0,100):
    x = gen_tweet()
    print(x)



