import mysql.connector
import random

from streamlit import cursor

#start of the game user sets username/story/rules explained if its too ng just tell me

username=input("Hello detective! what would you like to be called?: ")
print(f"Its an honor to have you {username}! please allow me to explained why we requested your service")
print("Your goal is to retrieve passengers lost luggage using your detective skills!")
print("visit various airports around the world by completing different challenges")
print("Each retrival mission is tied to a country’s capital city, and you’ll need to visit the correct airport to score points. The more efficient you are, the higher your score will be!")
print("You will be given a passenger luggage code to be able to track it, in order to successfully you will have to")
print("guess the country based of of 3 hints given by the system if you guess right you will fly there without a Co2 penalty")
print(f"Good luck {username}!")

des=input("if you are ready to start click enter!")

# Variable to track CO2 penalty
co2_penalty = 0


# Database connection function
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="126",
            database="flight_game",
            collation="utf8mb4_general_ci"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# oulls a random passamger info from data base
def fetch_infolugga():
    connection = connect_to_database()

    if connection:
        cursor = connection.cursor(dictionary=True)

        try:

            cursor.execute("SELECT COUNT(*) FROM passenger")
            total_passengers = cursor.fetchone()['COUNT(*)']


            random_offset = random.randint(0, total_passengers - 1)
            query = "SELECT first_name, last_name, age, gender, destination_airport, luggage_code FROM passenger LIMIT %s, 1"
            cursor.execute(query, (random_offset,))

            passenger = cursor.fetchone()

            if passenger:
                print("Random Passenger Details:")
                print(f"Name: {passenger['first_name']} {passenger['last_name']}")
                print(f"Age: {passenger['age']}")
                print(f"Gender: {passenger['gender']}")
                print(f"Destination Airport: {passenger['destination_airport']}")
                print(f"Luggage Code: {passenger['luggage_code']}")
            else:
                print("No passenger found.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Connection to database failed.")



#function to start the game you guys can edit if you would like to add or change something

def start():
    guesses=3
    co2_penalty=0
    if des == "":
        fetch_infolugga()
        while guesses > 0:
            guess_country = input("Where is the luggage? ")
            if guess_country == : #write the code for the correct country
               print("You are correct!")
            else:
               guesses-=1
               co2_penalty+=100
               print(f"You guessed wrong! You have {guesses} guess left")
    else:
        print("Exiting game.")


start()