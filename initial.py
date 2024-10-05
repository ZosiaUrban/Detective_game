import mysql.connector
import random
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

# remeber change to match yours when editing the code
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="126",
            database="flight_game"
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

# function to start the game you guys can edit if you would like to add or change something
def start():
        if des == "":
            fetch_infolugga()
        else:
            print("Exiting game.")




start()
