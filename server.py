# Noam Sabban 329897391
# Hadas Dahan 205636970

import sys
import random
import socket
import threading

"""
###################### classes ######################
"""

# making the chaser answer prob to 0.75
def correct():
    return random.randrange(100) < 75


class chaser:
    stepsIn = 0

    def __init__(self, stepsIn):
        self.stepsIn = 0


class player:
    stepsIn = 0
    money = 0
    help = 0
    ask_1 = ''
    ask_2 = ''
    clientconn = ''

    def __init__(self, money, stepsIn, stepsFromChaser, ask_1, ask_2, clientconn):
        self.money = money
        self.stepsIn = stepsIn
        self.stepsFromChaser = stepsFromChaser
        self.help = help
        self.ask_1 = ask_1
        self.ask_2 = ask_2
        self.clientconn = clientconn

# class for question
# making the questions and asking it according to the phase
class Question:

    def __init__(self, number, prompt, answer, options):
        self.number = number
        self.prompt = prompt
        self.answer = answer
        self.options = options


    def ask1(self, asked):
        asked.append(self.number)
        player.ask_1 += self.prompt + '?\n'
        for n, options in enumerate(self.options):
            player.ask_1 += '%d) %s\n' % (n + 1, options)

        clientconn.send(bytes(player.ask_1, "utf-8"))
        clientresponse = int(clientconn.recv(256).decode())

        if clientresponse == self.answer:
            player.ask_1 = 'Correct !\n'
            player.money += 5000
        else:
            player.ask_1 = 'Wrong !\n'

    def ask2(self, asked, ask_2=""):
        asked.append(self.number)
        player.ask_2 += self.prompt + "?\n"

        for n, options in enumerate(self.options):
            player.ask_2 += "%d) %s\n" % (n + 1, options)

        if (player.help == 0):
            player.ask_2 += "5) HELP"

        clientconn.send(bytes(player.ask_2, "utf-8"))
        clientresponse = int(clientconn.recv(256).decode())

        if clientresponse == 5 and player.help == 0:
            self.help()

        if clientresponse == self.answer:
            player.ask_2 = "Correct !\n"
            player.stepsIn += 1

        elif clientresponse != self.answer and clientresponse != 5:
            player.ask_2 = "Wrong !\n"

        if correct():
            chaser.stepsIn += 1
        
        # sending the info after every question
        player.ask_2 += "\nYou have " + str(player.money) + " dollar"
        player.ask_2 += "\nYou are on step " + str(player.stepsIn)
        player.ask_2 += "\nChaser is on step " + str(chaser.stepsIn) + "\n"
        if player.help == 0:
            player.ask_2 += "You have 1 help left\n"
        else:
            player.ask_2 += "You don't have any help left\n"
        player.ask_2 += "\n"

    def help(self):
        player.help += 1
        help_1 = self.prompt + "?\n"
        count = 0
        a = 0
        for n, options in enumerate(self.options):
            if count == 2:
                break
            if n + 1 == self.answer:
                help_1 += "%d) %s\n" % (n + 1, options)
                count += 1
            k = random.randint(0, 1)

            if k == 1 and n + 1 != self.answer and a == 0 and n != 3:
                help_1 += "%d) %s\n" % (n + 1, options)
                count += 1
                a += 1
        if count == 1 and n == 3 and n + 1 != self.answer:
            help_1 += "%d) %s\n" % (n + 1, options)
        elif count == 1 and n == 3:
            help_1 += "%d) %s\n" % (n - 1, options)
        
        # sending the aquestion with 2 options
        clientconn.send(bytes(help_1, "utf-8"))
        clientResHelp = int(clientconn.recv(256).decode())

        if clientResHelp == self.answer:
            player.ask_2 = "Correct !\n"
            player.stepsIn += 1
        else:
            player.ask_2 = "Wrong !\n"


"""
###################### New Thread - new game ######################
"""


def newGame(clientconn):
    player(0, 0, 0, '', '', clientconn)
    chaser(0)
    asked = []
    # making all the questions
    questions = [
        Question(1, "How many legs on a horse", 4, ["one", "two", "three", "four"]),
        Question(2, "How many wheels on a bicycle", 2, ["one", "two", "three", "four"]),
        Question(3, "What day is Shabbat", 1, ["Saturday", "Monday", "Tuesday", "Friday"]),
        Question(4, "What's the capital of Israel", 3,
                 ["Paris", "Tel Aviv", "Jerusalem", "Washington"]),
        Question(5, "What's the world's largest island", 2,
                 ["Australia", "Greenland", "Hawaii", "France"]),
        Question(6, "Who is the actual President of the USA", 3,
                 ["Donald Trump", "Walt Disney", "Joe Biden", "Tom Cruise"]),
        Question(7, "When was the Great Fire of London", 3, ["1994", "1892", "1666", "1766"]),
        Question(8, "What is the tiny piece at the end of a shoelace called", 2,
                 ["Lacend", "Aglet", "shoe", "Python"]),
        Question(9, "What war lasted from June 5 to June 10, 1967", 3,
                 ["Operation Protective Edge", "Yom Kippur War", "Six-day war", "South Lebanon conflict"]),
        Question(10, "How many movies there is in the toy story franchise", 4,
                 ["1", "2", "3", "4"]),
        Question(11, "How many Star Wars movies there is", 1,
                 ["9", "20", "3", "6"]),
        Question(12, "In which European city would you find Orly airport", 2,
                 ["London", "Paris", "Berlin", "Amsterdam"]),
        Question(13, "What's the distance between earth and the sun", 1,
                 ["149,600,000 km", "227,940,000 km", "120,000,000 km", "205,000,000 km"]),
        Question(14, "What's the average lifespan of a bee", 3,
                 ["12-22 days", "37-43 days", "122-152 days", "150-185 days"]),
        Question(15, "what's the height of the tallest building in the world", 4,
                 ["755 m", "632 m", "923 m", "828 m"]),
        Question(16, "Which singer’s real name is Stefani Joanne Angelina Germanotta?", 2,
                 ["Hannah Montana", "Lady gaga", "Cardi B", "Lana Del Rey"]),
        Question(17, "Who is the author of Lord of the Rings", 2,
                 ["George R. R. Martin", "J.R.R Tolkien", "Hadas Dahan", "Ian McKellen"]),
        Question(18, "Which of Shakespeare’s plays is the longest", 1,
                 ["Hamlet", "Romeo and Juliet", "The Comedy of Errors", "Macbeth"]),
        Question(19, "What is the tallest breed of dog in the world", 3,
                 ["Akita", "Bulldog", "The Great Dane", "German Shepherd"]),
        Question(20, "Who was the first female Prime Minister of Great Britain", 4,
                 ["Golda Meir", "Angela Merkel", "Theresa May", "Margaret Thatcher"]),
        Question(21, "Which of the following is not a wish the Genie cannot grant in Aladdin", 1,
                 ["To  become a prince", "To kill someone", "bring anyone back from the dead",
                  "make anyone fall in love"]),
        Question(22, "Who chooses Moana to return the heart", 2,
                 ["Her grandmother", "The Ocean", "Maui", "Te Fiti"]),
        Question(23, "What is the slogan for the Monsters Incorporated", 3,
                 ["We scare because we want.", "We scare because we can.", "We scare because we care.",
                  "We scare because we cant."]),
        Question(24, "What isnt a name of Merida’s brothers in Disney’s Brave", 2,
                 ["Harris", "Mickey", "Hubert", "Hamish"])
    ]

    firstPhase(asked, questions)


def intialize(asked, questions):
    asked.clear()  # reset the question list
    random.shuffle(questions)  # Shuffle randomly the question list
    player.help = 0  # Reset help
    player.money = 0
    player.stepsIn = 0
    chaser.stepsIn = 0
    player.ask_1 = ''
    player.ask_2 = ''


# First part , 3 questions
def firstPhase(asked, questions):
    n = 0  # checks how many questions were asked
    intialize(asked, questions) # intialize player properties
    for question in questions:
        if question.number in asked:
            continue
        if n >= 3:
            break
        else:
            n += 1
            question.ask1(asked)
    # player answered wrong every question, asking if he wants to play again        
    if player.money == 0:
        loose1 = player.ask_1
        loose1 += "Do you want to play again? Y=yes, N=no\n"
        clientconn.send(bytes(loose1, "utf-8"))
        finalPhase()

    secondPhase(asked, questions)


# Second part, maximum 5 questions
def secondPhase(asked, questions):
    option = player.ask_1
    option += "You have " + str(player.money) + " money\n"
    options = [
        "1. starting from step 3 with current funds",
        "2. get one step closer to chaser and start from step 2 for 2 times the funds",
        "3. get one step further from the chaser and start from step 4 with 1/2 the funds"
    ]

    option += "Your options are \n"
    option += '\n'.join(options)
    option += "\nPlease choose an option"

    clientconn.send(bytes(option, "utf-8"))
    playerChoice = int(clientconn.recv(256).decode())
    
    # updating the money and the steps of player acording to player choice
    if (playerChoice == 1):
        player.stepsIn = 3

    elif (playerChoice == 2):
        player.stepsIn = 2
        player.money *= 2

    elif (playerChoice == 3):
        player.stepsIn = 4
        player.money /= 2

    thirdPhase(asked, questions)


def thirdPhase(asked, questions):
    for question in questions:
        if question.number in asked:
            continue
        question.ask2(asked)
        
        # printing who won and if he want to play 
        
        if (player.stepsIn == 7 and chaser.stepsIn != 7):
            final = "Player won\n"
            final += "Do you want to play again? Y=yes, N=no"

            clientconn.send(bytes(final, "utf-8"))
            break
        
        
        elif (chaser.stepsIn == player.stepsIn):
            final = "Chaser won\n"
            final += "Do you want to play again? Y=yes, N=no"

            clientconn.send(bytes(final, "utf-8"))
            break
    
    # going to final phase to start a new game or close the connection
    finalPhase()


def finalPhase():
    response = clientconn.recv(256).decode()
    # starting a new game 
    if (response == 'Y'):
        newGame(player.clientconn)
    # closing the connection
    elif (response == 'N'):
        clientconn.send(bytes("Player choose not to play\n", "utf-8"))
        


"""
###################### MAIN ######################
"""

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

while True:
    # accept 4 connections from outside
    s.listen(4)
    clientconn, address = s.accept()

    # check number of active clients and deny the forth
    if threading.active_count() <= 3:
        print("Connection from " + str(address[0]) + " has been established.")
        # create a new thread that handles the game for current client
        t = threading.Thread(target=newGame, args=(clientconn,))
        # start thread
        t.start()
    # deny forth client
    else:
        print("Connection from " + str(address[0]) + " refused due to max players currently online.")
        clientconn.close()

