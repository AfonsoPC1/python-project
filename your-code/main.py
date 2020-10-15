#Libraries

import speech_recognition as sr
from gtts import gTTS 
import os
import playsound


# define rooms and item

#Game Room
couch = {
    "name": "couch",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

piano = {
    "name": "piano",
    "type": "furniture",
}

game_room = {
    "name": "game room",
    "type": "room",
}

#Bedroom 1

bedroom1={
    'name':'bedroom 1',
    'type':'room',
}

queen_bed={
    'name':'queen bed',
    'type':'furniture',
}

door_b = {
    "name": "door b",
    "type": "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

door_c = {
    "name": "door c",
    "type": "door",
}

#Bedroom 2

bedroom2={
    "name": "bedroom 2",
    "type": "room",
}

double_bed={
    'name':'double bed',
    'type':'furniture',
}

dresser={
    'name':'dresser',
    'type':'furniture',
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

#Living Room

living_room={
    "name": "living room",
    "type": "room",
}

dining_table={
    'name':'dining table',
    'type':'furniture',
}

door_d = {
    "name": "door d",
    "type": "door",
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

#Ouside

outside = {
  "name": "outside"
}

#Global

all_rooms = [game_room, bedroom1, bedroom2, living_room, outside]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a],
    "bedroom 1": [queen_bed, door_a, door_b, door_c],
    "bedroom 2": [double_bed, dresser, door_b],
    "living room": [dining_table, door_c, door_d],
    "outside": [door_b],
    "piano": [key_a],
    'queen bed': [key_b],
    'double bed':[key_c],
    'dresser': [key_d],
    "door a": [game_room, bedroom1],
    'door b': [bedroom1, bedroom2],
    'door c': [bedroom1, living_room],
    'door d': [living_room, outside],
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

def voice(keywords):
    """
    takes in a list of keywords, tries to return the one that is said by the user
    """

    # Initialize recognizer class (for recognizing the speech)

    r = sr.Recognizer()
    
    # Words that sphinx should listen closely for. 0-1 is the sensitivity
    # of the wake word.
    # eg.: keywords = [("examine", 1), ("explore", 1), ]
    # creates list of tuples from the passed keywords
    tuple_keywords = []
    for keyword in keywords:
        key_prm = (keyword, 1)
        tuple_keywords.append(key_prm)            
    
    
    # Reading Microphone as source
    # listening the speech and store in audio_text variable

    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")   
    # listen for 5 seconds and create the ambient noise energy level   
        r.adjust_for_ambient_noise(source, duration=5)  
        r.dynamic_energy_threshold = True  
    # request voice command, record audio
        print("State command") 
        audio_text = r.listen(source,phrase_time_limit=5)
        print("Time over, thanks")
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        print(r.recognize_sphinx(audio_text, "en-us", tuple_keywords))
        try:
            # using google speech recognition
            # print("I think you said:"+r.recognize_sphinx(audio_text, tuple_keywords))
            return r.recognize_sphinx(audio_text, tuple_keywords)
        except:
            print("Sorry, I did not get that")

def read(text, hold = True):
    """
    reads the text provided in english
    """
    speech = gTTS(text = text, lang = "en", slow = False)

    speech.save("text.mp3")
    #os.system("start text.mp3")
    
    if hold == False:
        playsound.playsound('text.mp3',False) #When we don't want it to pause the program until the sound stops playing
    else:
        playsound.playsound('text.mp3',True) #When we want it to pause the program until the sound stops playing
    os.remove('text.mp3') #removes file after playing
    
def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    read("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
        read("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"])
        read("You are now in " + room["name"])    
        read("What would you like to do? Type 'explore' or 'examine'?",False)
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
        #print("What would you like to do? Type 'explore' or 'examine'?")
        #intended_action = voice(['explore','examine'])
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            read("What would you like to examine?",False)
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            read("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))
    read("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))
    
def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    affirmative = ["Yes","yes","y","Y","yeah","affirmative"] #variations of affirmative user inputs   
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            read(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")
        read("The item you requested is not found in the current room.")
    if(next_room):
        read("Do you want to go to the next room? Enter 'yes' or 'no'", False)
        if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() in affirmative):
            play_room(next_room)
    else:
        play_room(current_room)
        
game_state = INIT_GAME_STATE.copy()

start_game()
