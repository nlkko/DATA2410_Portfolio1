import socket
import random
import json
import re

# List of all bots
bots = ["Bot_Anna", "Bot_George", "Bot_Paul"]

# List of verbs that are going to be ignored by the bot. Mainly helping and linking verbs
blacklistedVerbs = ["have", "be", "let", "is", "to", "go", "lets"]

# Loading the json file containing verbs
with open('json/verbs-all.json') as f:
    verbs = json.load(f)

# Loading the json file containing indexes for the verbs json file
# This helps reduce search times by not having to compare as many words
with open('json/verbs-index.json') as f:
    vindex = json.load(f)

# Checks the sentence the method recieved, then it checks if any of the words in that sentence is a verb.
# If the verb is not blacklisten it gets returned.
def returnVerb(msg):
    words = re.sub('\W+',' ', msg).lower().split()      #Splits recieved sentence into an array of words
    for word in words:      # Removes words that are less than 1 in lenght
        if len(word) == 1:
            words.remove(word)

    # Compares each word in the sentence with the verbs list from the json file
    # Then it compares the verbs with the blacklistedVerbs list, and filters them out.
    for word in words:
        letter = word[0]
        for indexArray in vindex:
            if letter == indexArray[0]:
                index = indexArray
                break

        i = index[1]
        while i <= index[2]:
            for verb in verbs[i]:
                if word == verb:
                    blacklisted = False
                    for blVerb in blacklistedVerbs:
                        if verb == blVerb:
                            print("BL: "+ verb +" "+ blVerb)
                            blacklisted = True
                    if not blacklisted:
                        return verbs[i]
            i = i + 1

def returnStatement(client):
    try:
        while True:
            msg = client.recv(1024)
            if msg: # Check if a message has been sent
                msg = msg.decode()
                return msg
    except:
        print("Stopped recieving messages from server")
        client.close()

# Verb tense of returnVerb() - With example: to bike
# verb[0] - infinitive / present simple | 1st person    bike
# verb[1] - present simple | 3rd person                 bikes
# verb[2] - past simple                                 biked
# verb[3] - past participle                             biked
# verb[4] - present participle                          biking

# Anna only wants to do what interests her and always rejects suggestions that do not.
def botAnna(client):
    def satisfy(verb):
        satisfied = False
        for interest in interests:
            if verb == returnVerb(interest):
                satisfied = True
        return satisfied

    def positiveResponse(action, previousAction):
        positiveResponse1 = "I love {}! I always used to {} as a kid".format(action[4], action[0])
        positiveResponse2 = "Yeah! Let's go {}, when are you free?".format(action[4])
        a = satisfy(action)
        b = satisfy(previousAction)
        positiveResponse3 = "Good suggestion, {} is way better than {}".format(action[4], previousAction[4]) if a and not b else "I've been waiting for you to mention {}!".format(action[4])
        positiveResponses = [positiveResponse1, positiveResponse2, positiveResponse3]

        return random.choice(positiveResponses)
    
    def negativeResponse(action, previousAction):
        randomInterest = returnVerb(random.choice(interests))
        negativeResponse1 = "Are you kidding me? I despise {}".format(action[4])
        negativeResponse2 = "I'm not joining in, I don't have time to {}".format(action[0])
        negativeResponse3 = "Instead of {}, could we {}?".format(action[4], randomInterest[0])
        negativeResponses = [negativeResponse1, negativeResponse2, negativeResponse3]

        return random.choice(negativeResponses) 

    interests = ["bike", "read", "hike", "steal", "burgle"]
    response = "I don't have anything to say to that"

    previousAction = None
    action = None
    while True:
        action = returnStatement(client).split(' ~ ')[1]      # Returns only the message part with the delimiter ' ~ '
        verb = returnVerb(action)
        
        # Triggers the correct response depending on what conditions satisfy her
        if verb == None:
            response = "I don't have anything to say to that"
        elif satisfy(verb):
            response = positiveResponse(verb, previousAction)
        else:
            response = negativeResponse(verb, previousAction)
        
        # Stores previous action in case of ab event happening
        previousAction = verb
        client.send(response.encode())

# Finds the correct bot
def botMessage(client, bot):
    if bot == "Bot_Anna":
        botAnna(client)
    elif bot == "Bot_George":
        print("Not programmed yet")
    elif bot == "Bot_Paul":
        print("Not programmed yet")