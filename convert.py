import pandas as pd

# Load your Excel file
file_path = "english_banjara_words.xlsx"   # put your file name here
df = pd.read_excel(file_path)

# Function to categorize words
def categorize_word(word):
    word = str(word).strip().lower()

    greetings = {"hi", "hello", "hey", "greetings", "goodbye", "bye"}
    animals = {"dog", "cat", "cow", "goat", "lion", "tiger", "elephant", "horse"}
    fruits = {"apple", "banana", "mango", "orange", "grape", "pineapple", "watermelon"}
    body_parts = {"head", "hand", "leg", "eye", "ear", "nose", "mouth", "foot", "finger"}
    materials = {"wood", "iron", "gold", "silver", "stone", "water", "fire", "air"}
    things = {"house", "car", "book", "pen", "table", "chair", "road"}

    if word in greetings:
        return "Greeting"
    elif word in animals:
        return "Animal"
    elif word in fruits:
        return "Fruit"
    elif word in body_parts:
        return "Body Part"
    elif word in materials:
        return "Material"
    elif word in things:
        return "Thing"
    else:
        return "Neutral"

# Apply categorization on "English" column
df["Category"] = df["English"].apply(categorize_word)

# Save the updated Excel
output_path = "categorized_banjara_words.xlsx"
df.to_excel(output_path, index=False)

print(f"✅ Categorized Excel saved as {output_path}")
