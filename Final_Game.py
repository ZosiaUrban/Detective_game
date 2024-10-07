import random
import mysql.connector

# Start of the game - user sets username/story/rules explained
username = input("Hello detective! What would you like to be called?: ")
print(f"It's an honor to have you, {username}! Please allow me to explain why we requested your service.")
print("Your goal is to retrieve passengers' lost luggage using your detective skills!")
print("Visit various airports around the world by completing different challenges.")
print("Each retrieval mission is tied to a country’s capital city, and you’ll need to visit the correct airport to score points.")
print("The more efficient you are, the higher your score will be!")
print("You will be given a passenger luggage code to track it. To succeed, you'll have to guess the country based on 3 hints.")
print(f"Good luck, {username}!")

des = input("If you are ready to start, press Enter!")

# This Variable is to track CO2 penalty
co2_penalty = 0

# Database connection  guys remeber to replace this with yours!
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="126",
            database="flight_game",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Fetch random details from pas datab
def fetch_infolugga():
    connection = connect_to_database()

    if connection:
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("SELECT COUNT(*) AS total FROM passenger")
            total_passengers = cursor.fetchone()['total']

            if total_passengers == 0:
                print("No passengers found in the database.")
                return None

            random_offset = random.randint(0, total_passengers - 1)
            query = "SELECT first_name, last_name, age, gender, destination_airport, luggage_code FROM passenger LIMIT %s, 1"
            cursor.execute(query, (random_offset,))
            passenger = cursor.fetchone()

            if passenger:
                print("Missing luggage passenger details:")
                print(f"Name: {passenger['first_name']} {passenger['last_name']}")
                print(f"Age: {passenger['age']}")
                print(f"Gender: {passenger['gender']}")
                print(f"Destination Airport: {passenger['destination_airport']}")
                print(f"Luggage Code: {passenger['luggage_code']}")
                return passenger['destination_airport']
            else:
                print("No passenger found.")
                return None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Connection to database failed.")
        return None

# Fetchs countries from country datab and their facts
def fetch_countries():
    connection = connect_to_database()
    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, facts FROM country")
    countries = cursor.fetchall()

    cursor.close()
    connection.close()

    return countries

# uses fetched countries randomly, had to split hints sorry
def select_random_country(countries):
    selected_country = random.choice(countries)
    hints = selected_country['facts'].split('. ')
    return selected_country['name'], hints

def play_country_guessing_game():
    countries = fetch_countries()
    if not countries:
        print("No countries found. Check database connection or data.")
        return

    rounds = 10
    successful_missions = 0
    negative_strikes = 0

    for round_number in range(1, rounds + 1):
        print(f"\n--- Round {round_number} ---")

        destination_airport = fetch_infolugga()
        if not destination_airport:
            print("Failed to fetch passenger information. Skipping round.")
            continue

        country_name, hints = select_random_country(countries)

        print("Hints:")
        for i, hint in enumerate(hints, start=1):
            print(f"{i}. {hint}")

        guesses_left = 3
        global co2_penalty

        while guesses_left > 0:
            user_guess = input(f"Guess the country (Attempts left: {guesses_left}): ").strip()
            if user_guess.lower() == country_name.lower():
                print(f"Correct! You've completed the mission and tracked the luggage to {destination_airport}.")
                successful_missions += 1
                break
            else:
                guesses_left -= 1
                co2_penalty += 50
                print(f"Incorrect! CO2 penalty: {co2_penalty} tons.")

                if guesses_left == 0:
                    print(f"You've failed this mission! The correct answer was {country_name}.")
                    negative_strikes += 1

        if negative_strikes >= 3:
            print("You’ve accumulated too many negative strikes. Mission failed!")
            break

    print("\n--- Game Over ---")
    print(f"Completed Missions: {successful_missions}")
    print(f"Negative Strikes: {negative_strikes}")

    if successful_missions > negative_strikes:
        print("Congratulations! You've won!")
    else:
        print("Sorry! You've lost!")


play_country_guessing_game()
