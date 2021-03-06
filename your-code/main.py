#Libraries

import speech_recognition as sr
from gtts import gTTS 
import os
import playsound
from IPython.display import Image, display

# define rooms and item

#Data Room, former game room
couch = {
    "name": "couch",
    "type": "furniture",
    "image_filename": "Images//sofa.jpg",
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

projector = {
    "name": "projector",
    "type": "furniture",
    "image_filename": "Images//projector.jpg",
}

data_room = {
    "name": "data room",
    "type": "room",
}

#Common Area, former Bedroom 1

common_area={
    'name':'common area',
    'type':'room',
}

table_tennis={
    'name':'table tennis',
    'type':'furniture',
    "image_filename": "Images//table-tennis.jpg",
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

#UX/UI room, former Bedroom 2

ux_ui_room={
    "name": "ux ui room",
    "type": "room",
}

white_board={
    'name':'white board',
    'type':'furniture',
    "image_filename": "Images//whiteboard.jpg",
}

post_it={
    'name':'post it',
    'type':'furniture',
    "image_filename": "Images//post-its.jpg",
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

#web dev room, former Living Room

web_dev_room={
    "name": "web dev room",
    "type": "room",
}

computer={
    'name':'computer',
    'type':'furniture',
    "image_filename": "Images//computer.jpg",
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

all_rooms = [data_room, common_area, ux_ui_room, web_dev_room, outside]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related

object_relations = {
    "data room": [couch, projector, door_a],
    "common area": [table_tennis, door_a, door_b, door_c, door_d],
    "ux ui room": [white_board, post_it, door_b],
    "web dev room": [computer, door_c],
    "outside": [door_b],
    "projector": [key_a],
    'table tennis': [key_b],
    'white board':[key_c],
    'computer': [key_d],
    "door a": [data_room, common_area],
    'door b': [common_area, ux_ui_room],
    'door c': [common_area, web_dev_room],
    'door d': [common_area, outside],
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": data_room,
    "keys_collected": [],
    "target_room": outside
}

def voice():
    """
    takes in a list of keywords, tries to return the one that is said by the user
    """

   
# Initialize recognizer class (for recognizing the speech)

    r = sr.Recognizer()

# Reading Microphone as source
# listening the speech and store in audio_text variable

    with sr.Microphone() as source:
        print('Wait')
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.dynamic_energy_threshold=True
        print("Talk")
        try:
            audio_text = r.listen(source,timeout=10)
            recognized_text = r.recognize_google(audio_text)
            #if recognized_text is None
            if recognized_text == "0" or recognized_text == "1": # check if recognized text makes sense
                return r.recognize_google(audio_text)
            else: # request manual input if not
                print("Sorry, I did not get that")    
                read("Sorry, I did not get that", False)
                return input("If you want to 'explore' type '0', if you want to 'examine' type '1'.").strip()
        except :
            print("Sorry, I did not get that")
            read("Sorry, I did not get that", False)
            #read("Please type what you would you like to do? Type '0' to explore' or '1' to 'examine'?")
            return input("If you want to 'explore' type '0', if you want to 'examine' type '1'.").strip()
        print("Time over, thanks")
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        
        #try:
            # using google speech recognition
         #   return r.recognize_google(audio_text)
        #except:
         #   print("Sorry, I did not get that")
          #  return input("Please type what you would you like to do? Type '0' to explore' or '1' to 'examine'?").strip()

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
    display(Image(filename="Images//ironhack.PNG"))
    print("You were coding until late and you fell asleep. Everyone else has left the building. You wake up on the couch of the data room, and now you need to find a way to get out of Ironhack. Good luck!")
    read("You were coding until late and you fell asleep. Everyone else has left the building. You wake up on the couch of the data room, and now you need to find a way to get out of Ironhack. Good luck!")
    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped Ironhack, you are free to go to your bed. More python will be waiting for you tomorrow!")
        read("Congrats! You escaped Ironhack, you are free to go to your bed. More python will be waiting for you tomorrow!")
        display(Image(filename="Images//bed.jpg"))
        playsound.playsound('sound//stage-clear.wav',True)
    else:
        print("You are now in " + room["name"])
        read("You are now in " + room["name"]) 
        print("If you want to 'explore' say '0', if you want to 'examine' say '1'.")
        #read("If you want to 'explore' say '0', if you want to 'examine' say '1'.",True)
        #intended_action = input("What would you like to do? Type '0' to 'explore' or '1' to 'examine'?").strip()
        intended_action = voice()  
        if intended_action == '0':
            explore_room(room)
            play_room(room)
        elif intended_action == '1':
            #read("What would you like to examine? Please type.",False)
            examine_item(input("What would you like to examine? Please type: ").strip())
        else:
            print("Not sure what you mean.")
            read("Not sure what you mean.")
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
#    affirmative = ["Yes","yes","y","Y","yeah","affirmative"] #variations of affirmative user inputs   
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        playsound.playsound('sound//door-squeak.wav',True)
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                display(Image(filename=item["image_filename"]))
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    playsound.playsound('sound//mario-coin.wav',True)
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
        if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == "yes"):
            play_room(next_room)
        else:
            play_room(current_room)    
    else:
        play_room(current_room)
        
game_state = INIT_GAME_STATE.copy()

start_game()
playsound.playsound('sound//stage-clear.wav',True)