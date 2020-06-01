import nltk, sys, random


def converse(command):
    if command=='':
        print('Your last command couldn\'t be heard')
    elif 'exit' in command or 'bye' in command or 'shut down' in command:
        return 'bye and have a nice day'
    elif command=='hello jarvis' or command=='hey jarvis':
        hello=['hi i am ready', 
        'my name is jarvis your personal voice assistant', 
        'what can i help you with']
        return random.choice(hello)
    elif 'how are you' in command:
        return 'i\'m doing great what about you'
    elif 'thanks' in command or 'thank you' in command:
        return "you're welcome"
    elif 'good morning' in command or 'good evening' in command or 'godd night' in command:
        daytime=int(datetime.datetime.now().strftime('%H'))
        if daytime<12:
            return 'good morning'
        elif daytime<16:
            return 'good afternoon'
        elif daytime<19:
            return 'good evening'
        else:
            return 'good night'
    elif 'okay boomer' in command:
        return 'ok zoomer'
    elif 'okay zoomer' in command:
        return 'no you'

