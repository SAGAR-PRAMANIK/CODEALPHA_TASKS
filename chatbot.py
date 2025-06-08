import nltk
import random
import datetime
import pyjokes
import requests

# Download punkt if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Define patterns and responses
intents = {
    "greeting": {
        "patterns": ["hi", "hello", "hey", "how are you", "what's up"],
        "responses": ["Hello!", "Hi there!", "Hey!", "Hi, how are you?"]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you later"],
        "responses": ["Goodbye!", "See you later!", "Bye!"]
    },
    "joke": {
        "patterns": ["tell me a joke", "make me laugh", "joke"],
        "responses": [pyjokes.get_joke()]
    }
}

def get_intent(user_input):
    user_input = user_input.lower()
    for intent, data in intents.items():
        for pattern in data["patterns"]:
            if pattern in user_input:
                return intent
    return None

def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            print("Bot: Goodbye!")
            break

        # --- All your special command if-blocks go here ---
        if "time" in inp:
            print("Bot:", datetime.datetime.now().strftime("%H:%M:%S"))
            continue

        if "weather" in inp:
            api_key = "YOUR_API_KEY"  # Get a free API key from https://openweathermap.org/
            city = "YOUR_CITY"        # Or extract city from user input
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            try:
                response = requests.get(url)
                data = response.json()
                if data["cod"] == 200:
                    weather = data["weather"][0]["description"]
                    temp = data["main"]["temp"]
                    print(f"Bot: The weather in {city} is {weather} with a temperature of {temp}°C.")
                else:
                    print("Bot: Sorry, I couldn't get the weather information.")
            except Exception:
                print("Bot: Sorry, I couldn't connect to the weather service.")
            continue

        if "my name is" in inp:
            name = inp.split("my name is")[-1].strip().capitalize()
            print(f"Bot: Nice to meet you, {name}!")
            continue

        if "calculate" in inp or "what is" in inp:
            try:
                # Extract the math expression
                expr = inp.split("calculate")[-1] if "calculate" in inp else inp.split("what is")[-1]
                expr = expr.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
                result = eval(expr)
                print(f"Bot: The answer is {result}")
            except Exception:
                print("Bot: Sorry, I couldn't calculate that.")
            continue
        # Date
        if "date" in inp:
            print("Bot:", datetime.datetime.now().strftime("%Y-%m-%d"))
            continue

        # Day of the week
        if "day" in inp:
            print("Bot: Today is", datetime.datetime.now().strftime("%A"))
            continue

        # Tell a programming joke (using pyjokes)
        if "programming joke" in inp or "pyjoke" in inp:
            print("Bot:", pyjokes.get_joke(category="programming"))
            continue

        # Flip a coin
        if "flip a coin" in inp or "toss a coin" in inp:
            print("Bot:", random.choice(["Heads", "Tails"]))
            continue

        # Roll a dice
        if "roll a dice" in inp or "roll a die" in inp:
            print("Bot: You rolled a", random.randint(1, 6))
            continue

        # Simple greeting with user's name if known
        if "hello" in inp or "hi" in inp:
            if 'name' in locals():
                print(f"Bot: Hello, {name}!")
            else:
                print("Bot: Hello!")
            continue

        # Help command
        if "help" in inp:
            print("Bot: You can ask me about the time, date, weather, jokes, math, flip a coin, roll a dice, and more!")
            continue

        if "exit" in inp:
            print("Bot: Goodbye!")
            break

        # Wikipedia summary
        if "wikipedia" in inp:
            try:
                import wikipedia
                topic = inp.split("wikipedia")[-1].strip()
                if not topic:
                    print("Bot: Please specify a topic after 'wikipedia'.")
                else:
                    summary = wikipedia.summary(topic, sentences=2)
                    print("Bot:", summary)
            except ImportError:
                print("Bot: Wikipedia module not installed. Run 'pip install wikipedia' to use this feature.")
            except Exception as e:
                print("Bot: Sorry, I couldn't fetch information from Wikipedia.")
            continue

        # Tell a random fact
        if "fact" in inp:
            facts = [
                "Honey never spoils.",
                "Bananas are berries, but strawberries are not.",
                "A group of flamingos is called a flamboyance.",
                "Octopuses have three hearts.",
                "The Eiffel Tower can be 15 cm taller during hot days."
            ]
            print("Bot:", random.choice(facts))
            continue

        # Countdown timer
        if "timer" in inp:
            try:
                import time
                words = inp.split()
                seconds = None
                for i, word in enumerate(words):
                    if word.isdigit():
                        seconds = int(word)
                        break
                if seconds:
                    print(f"Bot: Starting a timer for {seconds} seconds.")
                    time.sleep(seconds)
                    print("Bot: Time's up!")
                else:
                    print("Bot: Please specify the number of seconds for the timer.")
            except Exception:
                print("Bot: Sorry, I couldn't start the timer.")
            continue

        # Reverse your message
        if "reverse" in inp:
            msg = inp.split("reverse")[-1].strip()
            if msg:
                print("Bot:", msg[::-1])
            else:
                print("Bot: Please provide a message to reverse.")
            continue

        # Count words in your message
        if "count words" in inp:
            msg = inp.split("count words")[-1].strip()
            if msg:
                print(f"Bot: Your message has {len(msg.split())} words.")
            else:
                print("Bot: Please provide a message after 'count words'.")
            continue

        # Generate a random password
        if "password" in inp:
            import string
            length = 8
            for word in inp.split():
                if word.isdigit():
                    length = int(word)
                    break
            chars = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(chars) for _ in range(length))
            print(f"Bot: Here is a random password: {password}")
            continue

        # Tell a random motivational quote
        if "motivate" in inp or "motivation" in inp or "quote" in inp:
            quotes = [
                "Believe you can and you're halfway there.",
                "The only way to do great work is to love what you do.",
                "Success is not final, failure is not fatal: It is the courage to continue that counts.",
                "Dream big and dare to fail.",
                "Don't watch the clock; do what it does. Keep going."
            ]
            print("Bot:", random.choice(quotes))
            continue

        # --- Only runs if no special command matched ---
        intent = get_intent(inp)
        if intent:
            print("Bot:", random.choice(intents[intent]["responses"]))
        else:
            print("Bot: Sorry, I didn't understand that.")

if __name__ == "__main__":
    chat()