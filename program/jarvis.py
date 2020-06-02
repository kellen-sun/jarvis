import speech_recognition as sr
import os, sys, webbrowser, random, calendar, urllib.parse, smtplib, json, textwrap
import nltk, bs4, wolframalpha, wikipedia, requests, datetime, urllib.request
import threading, subprocess, re, pickle, playsound, pyowm #, pygame
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
from gtts import gTTS
from conversation import converse
import pandas as pd
import pandas_datareader.data as web
from pandas import Series, DataFrame

#pygame.init()
#pygame.display.set_caption('JARVIS')
app_id = "wolframalpha id"
chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
#dis=pygame.display.set_mode((800, 400))

def note(text):
    file_name = "note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])
    
def speak(text):
    speak_1(text)
    
def listening(question=None):
    if question != None:
        speak(str(question))
    r=sr.Recognizer()
    with sr.Microphone() as source:
        #dis.blit(pygame.font.SysFont("comicsansms", 24).render('JARVIS is ready...', True, (30, 30, 30)), [0, 0])
        print('JARVIS is ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: '+command)
        return command
        #dis.blit(pygame.font.SysFont("comicsansms", 24).render('You said: ' + command, True, (30, 30, 30)), [0, 0])
    except sr.UnknownValueError:
        return ''
    
def speak_1(text):
    '''time=datetime.datetime.now().strftime('%H:%M')
    if int(time[:2])>12:
        time=str(int(time[:2])-12)+time[2:]
    xy=[0, 0]
    dis.fill((232, 33, 39))
    v=textwrap.fill(text, 65)
    for part in v.split('\n'):
        rendered_text = pygame.font.SysFont("comicsansms", 24).render(part, True, (30, 30, 30))
        dis.blit(rendered_text,xy)
        xy[1] += 30
    dis.blit(pygame.font.SysFont("comicsansms", 36).render(time, True, (30, 30, 30)), [720, 360])
    pygame.display.update()'''

    v=textwrap.fill(text, 90)
    for part in v.split('\n'):
        print(part)
    try:
        tts = gTTS(text=text, lang='en')
        tts.save('voice.mp3')
        playsound.playsound('voice.mp3')
        os.remove('voice.mp3')
    except:
        print('The speaker is muted')
    
def tasks(command):
    if ('hey jarvis' in command or 'okay jarvis' in command) and command.split()[1]=='jarvis':
        #dis.fill((232, 33, 39))
        #pygame.display.update()
        if 'open' in command or 'launch' in command:
            if 'google docs' in command:
                webbrowser.get('chrome').open_new_tab('https://docs.google.com/document/u/0/')
                speak('I\'m done!')
            elif 'google slides' in command:
                webbrowser.get('chrome').open_new_tab('https://docs.google.com/presentation/u/0/')
                speak('I\'m done!')
            elif 'youtube' in command:
                webbrowser.get('chrome').open_new_tab('https://www.youtube.com')
                speak('I\'m done!')
            elif 'gmail' in command:
                webbrowser.get('chrome').open_new_tab('https://mail.google.com')
                speak('I\'m done!')
            elif 'google' in command or 'chrome' in command:
                webbrowser.get('chrome').open_new_tab('https://www.google.com')
                speak('I\'m done!')
                    
        elif 'search'==command.split()[2] and 'google'==command.split()[3] and 'for'==command.split()[4]:
            words=command.split()[5:]
            command=''
            for x in range(len(words)):
                command=command+' '+words[x]
            query_string = urllib.parse.urlencode({'':command[0:]})
            try:
                webbrowser.get('chrome').open_new_tab("https://www.google.com/search?q" + query_string)
            except:
                webbrowser.get('chrome').open_new("https://www.google.com/search?q" + query_string)
            speak("i'm done!")
            
        elif 'search'==command.split()[2] and 'wikipedia'==command.split()[3] and 'for'==command.split()[4]:
            try:
                words=command.split()[5:]
                command=''
                for x in range(len(words)):
                    command=command+' '+words[x]
                speak(command[0:])
                speak(wikipedia.summary(command[0:], sentences=3))
            except:
                speak(command[0:]+' not found')  
                      
        elif 'tell'==command.split()[2] and 'me'==command.split()[3] and 'about'==command.split()[4]:
            try:
                words=command.split()[5:]
                command=''
                for x in range(len(words)):
                    command=command+' '+words[x]
                speak(command[0:])
                speak(wikipedia.summary(command[0:], sentences=5))
            except:
                speak(command[0:]+' not found')
                    
        elif 'search'==command.split()[2] and 'youtube'==command.split()[3] and 'for'==command.split()[4]:
            words=command.split()[5:]
            if 'videos' in words:
                words.remove('videos')
            elif 'video' in words:
                words.remove('video')
            command=''
            for x in range(len(words)):
                command=command+' '+words[x]
            query_string = urllib.parse.urlencode({"search_query" : command[0:] })
            try:
                webbrowser.get('chrome').open_new_tab("http://www.youtube.com/results?" + query_string)
            except:
                webbrowser.get('chrome').open_new("http://www.youtube.com/results?" + query_string)
            speak("i'm done!")
                
        elif command.split()[2]=='show' and command.split()[3]=='me' and (command.split()[-1]=='videos' or command.split()[-1]=='video'):
            words=command.split()[4:-1]
            if 'videos' in words:
                words.remove('videos')
            elif 'video' in words:
                words.remove('video')
            command=''
            for x in range(len(words)):
                command=command+' '+words[x]
            query_string = urllib.parse.urlencode({"search_query" : command[0:] })
            try:
                webbrowser.get('chrome').open_new_tab("http://www.youtube.com/results?" + query_string)
            except:
                webbrowser.get('chrome').open_new("http://www.youtube.com/results?" + query_string)
            speak("i'm done!")
                
        elif 'time' in command:
            time=datetime.datetime.now().strftime('%H:%M')
            if int(time[:2])>12:
                time=str(int(time[:2])-12)+time[2:]
            speak('it is '+str(time))
            
        elif 'date' in command:
            my_string=str(datetime.datetime.now())[:10]
            time=datetime.datetime.strptime(my_string, "%Y-%m-%d")
            week=calendar.day_name[time.weekday()]
            month=calendar.month_name[int(my_string[5:7])]
            if str(my_string[-1])=='1':
                day=str(my_string[-1])+'st'
            elif str(my_string[-1])=='2':
                day=str(my_string[-1])+'nd'
            elif str(my_string[-1])=='3':
                day=str(my_string[-1])+'rd'
            else:
                day=str(my_string[-1])+'th'
            speak('Today is '+week+' '+month+' the '+day+' '+my_string[:4])
        
        elif 'search news for' in command:
            try:
                words=command.split()[5:]
                command=' '.join(words)
                query_string = urllib.parse.urlencode({"search_query" : command})
                client=urllib.request.urlopen("https://news.google.com/rss/search?q="+query_string)
                xml_page=client.read()
                client.close()
                soup_page=bs4.BeautifulSoup(xml_page, "xml")
                news_list=soup_page.findAll('item')
                for news in news_list[:2]:
                    article=Article(str(news.link.text))
                    article.download()
                    article.parse()
                    article.nlp()
                    speak(article.summary)
            except Exception as e:
                print(e)
                speak('nothing new')
                
        elif 'news' in command:
            try:
                news_url="https://news.google.com/news/rss"
                client=urllib.request.urlopen(news_url)
                xml_page=client.read()
                client.close()
                soup_page=bs4.BeautifulSoup(xml_page, "xml")
                news_list=soup_page.findAll('item')
                for news in news_list[:2]:
                    article=Article(str(news.link.text))
                    article.download()
                    article.parse()
                    article.nlp()
                    speak(article.summary)
            except Exception as e:
                print(e)
                speak('nothing new')
                
        elif 'send' in command and 'email' in command:
            msg = MIMEMultipart() 
            user=#your email
            speak('who do i send the email to?')
            to=listening()
            msg['From']=user
            msg['To']=to
            speak("what's the subject of the email")
            subject=listening()
            speak('what do you wish to write?')
            body=listening()
            msg.attach(MIMEText(body, 'plain'))
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            s.starttls() 
            password= #your password
            s.login(user, password)
            text = msg.as_string() 
            s.sendmail(user, to, text) 
            s.quit()
        
        elif "make a note" in command or "write this down" in command:
                speak("What would you like me to write down?")
                note_text = listening()
                note(note_text)
                speak("I've made a note of that.")
        
        elif "hey jarvis play the song" in command or "hey jarvis search the song" in command:
            infile = open('music_list','rb')
            music_list=pickle.load(infile)
            infile.close()
            words=command.split()[5:]
            if 'music' in words:
                words.remove('music')
            elif 'song' in words:
                words.remove('song')
            command=' '.join(words)
            query_string = urllib.parse.urlencode({"search_query" : command+' music'})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            try:
                webbrowser.get('chrome').open_new_tab("http://www.youtube.com/watch?v=" + search_results[0])
            except:
                webbrowser.get('chrome').open_new("http://www.youtube.com/watch?v=" + search_results[0])
            outfile = open('music_list','wb')
            music_list.append(command)
            pickle.dump(music_list, outfile)
            outfile.close()
            speak("i'm done!")
            
        elif "hey jarvis play music" in command or "hey jarvis play me a song" in command or "hey jarvis play some music" in command:
            infile = open('music_list','rb')
            music_list=pickle.load(infile)
            infile.close()
            song=random.choice(music_list)
            query_string = urllib.parse.urlencode({"search_query" : song})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            try:
                webbrowser.get('chrome').open_new_tab("http://www.youtube.com/watch?v=" + search_results[0])
            except:
                webbrowser.get('chrome').open_new("http://www.youtube.com/watch?v=" + search_results[0])
            speak("i'm done!")
        
        elif "coin" in command and 'flip' in command:
            coin=['heads', 'tails']
            speak('you flipped ' + random.choice(coin))
        
        elif 'dice' in command and 'roll' in command:
            speak('You rolled ' + str(random.randint(1, 6)))
        
        elif 'weather' in command:
            owm = pyowm.OWM('3820e101d369089c44c3466b18e5690e')
            if 'in' in command:
                words=command.split()
                place=' '.join(words[words.index('in')+1:])
                country=listening('What country? ')[:2].upper()
                observation = owm.weather_at_place(place.title()+','+country)
            else:
                observation = owm.weather_at_place('Kanata,CA')
            try:
                w=observation.get_weather()
                temp=w.get_temperature(unit='celsius')
                status=w.get_status()
                speak("the weather status is "+status+" and the temperature is "+str(temp['temp'])+' degrees.')
                speak("the high is " + str(temp['temp_max'])+' and the low is '+str(temp['temp_min'])+' degrees')
            except:
                speak('place not found')
                
        elif "what is the stock price of" in command:
            my_string=str(datetime.datetime.now())[:10]
            time=datetime.datetime.strptime(my_string, "%Y-%m-%d")
            week=calendar.day_name[time.weekday()]
            ticker=listening('What is the ticker or stock symbol?')
            x = datetime.datetime.now()
            if week=='Saturday':
                date = datetime.datetime(x.year, x.month, x.day-1)
            elif week=='Sunday':
                date = datetime.datetime(x.year, x.month, x.day-2)
            else:
                date = datetime.datetime(x.year, x.month, x.day)
            df = web.DataReader(ticker, 'yahoo', date)
            df.tail()
            close_price=round(df['Close'][0], 2)
            open_price=round(df['Open'][0], 2)
            percent=round((close_price-open_price)/open_price*100, 2)
            speak(ticker+' is at '+str(close_price)+' dollars. It opened at '+
            str(open_price)+' and increased by '+str(percent)+' percent.')
        
        elif ("open" in command) and ("note" in command):
            file_name='note.txt'
            while True:
                try:
                    subprocess.Popen(["notepad.exe", file_name])
                except:
                    break
            speak("There are no more notes.")
            
        elif 'joke' in command:
            speak("How do I learn coding in a single night?")
            speak('Pack a laptop and fo to the north pole at the beginning of winter.')
        
        else:
            try:
                words=command.split()[2:]
                command=' '.join(words)
                client = wolframalpha.Client(app_id)
                res = client.query(command)
                answer = next(res.results).text 
                speak('The answer is ' + answer)
            except:   
                try:
                    words=command.split()[2:]
                    command=''
                    for x in range(len(words)):
                        command=command+' '+words[x]
                    speak('I found this on the web.')
                    speak(wikipedia.summary(command[0:], sentences=3))
                except:
                    errors=['i\'m not programmed to answer that yet.',
                    "i don't know what you mean!",
                    "Excuse me?"]
                    speak(random.choice(errors))

def setup():
    time=datetime.datetime.now().strftime('%H:%M')
    if int(time[:2])>12:
        time=str(int(time[:2])-12)+time[2:]
    #dis.fill((232, 33, 39))
    #dis.blit(pygame.font.SysFont("comicsansms", 36).render(time, True, (30, 30, 30)), [720, 360])
    #pygame.display.update()
    command=listening().lower()
    #dis.blit(pygame.font.SysFont("comicsansms", 36).render(time, True, (30, 30, 30)), [720, 360])
    #pygame.display.update()
    return command
    
def jarvis():
    while True:
        command=listening()
        c=converse(command)
        if c=='bye and have a nice day':
            speak(c)
            #pygame.quit()
            sys.exit()
        elif c:
            speak(c)
        else:
            tasks(command)
        
jarvis()
