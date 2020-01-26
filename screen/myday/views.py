from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import pos_tag
from django.views.decorators.csrf import csrf_exempt
import datetime


import spacy

#from django.http import HTTPRe

data = {}
def hid(text):
    nlp = spacy.load('en_core_web_sm')

    # ----- REFs -----
    sid = SentimentIntensityAnalyzer()
    # Call the prebuilt Sentiment ML algo
    stopWords = set(stopwords.words('english') + ["hate","dislike","like","love","hated","disliked","liked",'loved','today'])
    tokenizer = RegexpTokenizer(r'\w+')


    data['active'] = []
    data['recreational'] = []
    data['work'] = []
    data['nodes'] = []
    data['final'] = []
    # FUNCTIONS THAT RUN BEFORE TO CLEAN CODE
    def preproc(text):
            final = []
            text = tokenizer.tokenize(text.lower());

            for n in text:
                if n not in stopWords:
                    final.append(n);
            return final

    # QUERY CODE
    def nnouns(text):
        final = []
        for tup in text:
            if (tup.pos_ == "NOUN" or tup.pos_ == "PROPN"):
                final.append(tup.text)
        return final

    def classifyverbs(text):
        final = []
        for tup in text:
            if (tup.pos_ == "VERB"):
                final.append(tup.text)
        return final

    # find how simmilar they are to Sports / Work / Rec

    def simindexv (text):
        indexa = 0
        indexr = 0
        indexw = 0
        ttext = nlp(text)
        active = ['swim', 'drown', 'swimming', 'float', #index for swim
                  'jog','jogged', 'ramble', 'nudge', 'trot', 'lope', #index for jog
                 'walk','walking','walked','pass','run', #index for jog
                 'ski', #index for ski
                 'run','ran', 'go'] #index for ski

        rec = ['consume', 'eat', 'munch', #index for eat
                 'observe','watch','watch', 'see', 'view','viewed', #index for see
                 'blab','lecture','speak','talk','talked','sing' #index for talk
                 'play','played', #index for play
                 'dance', 'sleep'] #index for dance

        wor = ['code', 'learn', 'study', #index for eat
                 'memorize','instruct','work', 'cram', 'do','did', #index for see
                 'remember','consider']

        for word in active:
            z = nlp(word)
            indexa = max(indexa, z.similarity(ttext))

        for word in rec:
            z = nlp(word)
            indexr = max(indexr, z.similarity(ttext))

        for word in wor:
            z = nlp(word)
            indexw = max(indexr, z.similarity(ttext))



        if (indexa > indexr and indexa > indexw):
            return ("active")
        elif (indexr > indexa and indexr > indexw):
            return ('recreational')
        else:
            return('work')



        return("ass")


    def child2 (group, verb):
        data[group].append({
            "verb": verb
        })

    def child3 (group, verb, noun):
        data[group].append({
            verb: 1,
            noun: 1
        })
    # QUERY CODE
    def intentfram (sent):
        #Code to find intensisty
        score = sid.polarity_scores(sent);
        #Score is a dict with entries for [pos] = positivity and [neg] = negitivity
        mat = 100* score['pos'] -100 * score['neg']
        return mat




    def start(text):
        count = 0;
        total = 0;
        phara = sent_tokenize(text)
        for rawsent in phara:
            count += 1;

            data["nodes"].append({
                count: intentfram(rawsent)
            });
            total += intentfram(rawsent);
            sent = nlp(' '.join(preproc(rawsent)))


            verb = classifyverbs(sent);
            noun = nnouns(sent);



            if (len(verb) == 0):
                print("SENT DOESNT MAKE SENSE")

            else:
                verb = verb[0]

                vresult = simindexv(verb)

                if (len(noun) == 0):
                    child2(vresult, verb);
                else:
                    child3(vresult, verb,noun[0])







        if(count != 0):
            data["final"].append({
            "average": total/count
        });
        
        return (True)



    if(start(text)):
        return (True)
#saving("active","ass")

    
    
# Create your views here.
def allday(request):
    #request.POST.get("title","ok")
    #all_days = MyJournal.objects.all()
    #return render(request, 'day.html', {'allthedays': all_days})
    a = MyJournal(content = data, date_created = datetime.date.today())
    context= {
    'info': a.content,
    'date': a.date_created,
    }
    return render(request, 'days.html', context)

@csrf_exempt
def passinfo(request):
    print(request.method)
    if request.method == "POST":
        
        print("POST")
        unfixedsent = str(request.body);
        z = len(unfixedsent)
        unfixedsent = unfixedsent[2:(z-1)]
        
        line = unfixedsent.replace("\\n",' ')
        print(line);
        
        if (hid("I run to work.")):
            print(data)
            return HttpResponse(request, {'data': data})
        else:
            print("NOTHING")
            
        
    elif request.method == "GET":
        print("GET")
        if (hid("I run to work.")):
            print(data)
            json_data = serializers.serialize("json", data)
            return HttpResponse(json_data, content_type='')
        
    else:
        print("WHAT")
    
def oneday(request):
    #all_days = MyJournal.objects.all()
    
    context= {
    'info': data,
    'date':datetime.date.today(),
    }
    return render(request, 'day.html', context)
    #return render(request, 'days.html',{'allthedays': all_days[day_id-1]})

