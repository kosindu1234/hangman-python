import mysql.connector
import random
def hangman_repeat ():
    user_input=""
    user_input=input("Do you want to play again(yes/no)").lower()
    if user_input=="yes":
        main_hangman()
    else:
        pass

def main_hangman ():
    "This function is the main body of the hangman"
    conDict = {'host' : 'localhost',
               'database' : 'hangman',#<-------------------open database connection with dictionery 
               'user' : 'root' ,
               'password' : ''}

    db = mysql.connector.connect (**conDict)
    cursor = db.cursor()
    #welcome to the game
    print("Welcome to the Hangman game!")

    #user's name
    user_name = input("Enter your name : ")
    print("Welcome" , user_name , "Please use lower case letters to proceed the game!")

    #Creating a list of words
    words = ['avenue','microwave''oxygen','scratch','duplex','galaxy','luxury','helicopter','mobile','desktop','youtube','bascketball','zombie','australia','america','rugby','competition','acknowledgement','introduction','agriculture']
    word = random.choice(words)  # random word
    word_letters = set(word)  # letters in the word
    used_letters = set()  # what is user guessed
    
    use_sql= ("SELECT Name,Game_played FROM hangman WHERE Name = \""+user_name+"\"")
    cursor.execute(use_sql)
    value = cursor.fetchall()

    if(len(value)>0):
        played_game = "UPDATE hangman SET Game_played  = %s WHERE Name = %s"
        my_value = value[0][1] + 1
        user_info = (my_value, user_name)
        cursor.execute (played_game,user_info)
        db.commit()
    else:
        new_user = "INSERT INTO hangman (Name,Game_played) VALUES (%s,%s)"
        games_played = (user_name,1)
        cursor.execute(new_user,games_played )
        db.commit()

    lives = len(word)

    #getting user's input
    while len(word_letters) > 0 and lives > 0:
        word_list = [letter if letter in used_letters else '_' for letter in word]
        print('Word: ', ' '.join(word_list))
        print(lives, 'turns remain')
        
        user_letter = input('Letter: ').lower()
        if user_letter=="exit":
            break
        if user_letter in word_letters:
            used_letters.add(user_letter)
            word_letters.remove(user_letter)

        else:
            lives = lives - 1  # takes away a life if wrong

    if lives == 0:
        print(user_name,'You lost!' ' Try again')
        print(f'Word is "{word}"')
        win_or_loss = "Lost"

        user_losses = ("SELECT Name,losses FROM hangman WHERE Name = \""+user_name+"\"")
        cursor.execute(user_losses)
        losses=cursor.fetchall()

        #updating lost values each time player losses
        update_user_losses = "UPDATE hangman SET losses= %s WHERE Name = %s"
        losses_user = losses[0][1] + 1
        my_value_losses = (losses_user , user_name)
        cursor.execute (update_user_losses , my_value_losses)
        db.commit()

    else:
        word_list = [letter if letter in used_letters else '_' for letter in word]
        print('Word: ', ' '.join(word_list))
        print(user_name,'You won !')
        print(f'Word is "{word}"')
        win_or_loss = "Win"
        user_wins = ("SELECT Name,Wins FROM hangman WHERE Name = \""+user_name+"\"")
        cursor.execute(user_wins)
        Wins=cursor.fetchall()

        #updating win values each time player wins
        update_user_wins = "UPDATE hangman SET Wins= %s WHERE Name = %s"
        wins_user = Wins[0][1] + 1
        my_value_wins = (wins_user , user_name)
        cursor.execute (update_user_wins , my_value_wins)
        db.commit()

    hangman_repeat()
main_hangman()
