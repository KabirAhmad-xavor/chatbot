# import sqlite3
# import json

# from userinfo import userdata  # Your original userdata here (unchanged)

# user_profile={}
# def convert_to_json(data):
#     if isinstance(data, (list, dict)):
#         return json.dumps(data)
#     return data

# # Connect to the database
# conn = sqlite3.connect('userdata.db')
# cursor = conn.cursor()

# # # Create table if it doesn't exist
# # cursor.execute('''
# # CREATE TABLE IF NOT EXISTS user_profile (
# #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #     name TEXT,
# #     age INTEGER,
# #     gender TEXT,
# #     ethnicity TEXT,
# #     area TEXT,
# #     location TEXT,
# #     professional_background TEXT,
# #     hobbies TEXT,
# #     likes TEXT,
# #     dislikes TEXT,
# #     cognitive_physical_abilities TEXT,
# #     goals_and_needs TEXT,
# #     daily_routine TEXT,
# #     technology_comfort_level TEXT,
# #     challenges_and_pain_points TEXT,
# #     desired_features TEXT
# # )
# # ''')

# # # Insert data into the table
# # cursor.execute('''
# # INSERT INTO user_profile (
# #     name, age, gender, ethnicity, area, location, professional_background,
# #     hobbies, likes, dislikes, cognitive_physical_abilities, goals_and_needs,
# #     daily_routine, technology_comfort_level, challenges_and_pain_points, desired_features
# # ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# # ''', (
# #     userdata['demographics']['name'],
# #     userdata['demographics']['age'],
# #     userdata['demographics']['gender'],
# #     userdata['demographics']['ethnicity'],
# #     userdata['area'],
# #     userdata['city'],
# #     userdata['professional_background'],
# #     convert_to_json(userdata['hobbies']),
# #     convert_to_json(userdata['likes']),
# #     convert_to_json(userdata['dislikes']),
# #     convert_to_json(userdata['cognitive_physical_abilities']),
# #     convert_to_json(userdata['goals_and_needs']),
# #     convert_to_json(userdata['daily_routine']),
# #     userdata['technology_comfort_level'],
# #     convert_to_json(userdata['challenges_and_pain_points']),
# #     convert_to_json(userdata['desired_features'])
# # ))

# # conn.commit()

# # Retrieve data for user with id = 1
# cursor.execute('SELECT * FROM user_profile ')
# row = cursor.fetchone()

# # Define the column names in the same order as in the database table
# columns = [
#     "id", "name", "age", "gender", "ethnicity", "area", "location", "professional_background",
#     "hobbies", "likes", "dislikes", "cognitive_physical_abilities", "goals_and_needs",
#     "daily_routine", "technology_comfort_level", "challenges_and_pain_points", "desired_features"
# ]

# if row:
#     # Map each column name to its corresponding value from the row
#     user_profile = dict(zip(columns, row))
#     print("User data:", user_profile)
# else:
#     print("No user found with id = 1")

# conn.close()

# userdata=user_profile
# # print(userdata)




import sqlite3
import json

# User-provided data
userdata = {
    "demographics": {
        "name": "Emiely",
        "age": 23,
        "gender": "Female",
        "ethnicity": "Spanish",
    },
    "area": "DHA",
    "city": "Lahore",
    "professional_background": "Retired Professor of Art History",
    "hobbies": ["Yoga", "Music", "Painting"],
    "likes": [
        "I like to remain physically active as much as possible, especially during the mornings.",
        "I love to attend art exhibitions and am a painter myself.",
        "I enjoy a routine in my life."
    ],
    "dislikes": [
        "I do not like loud and rap music.",
        "I am afraid of the dark, so prefer to sleep with a small light on.",
        "I do not like cats."
    ],
    "cognitive_physical_abilities": [
        "Mild cognitive impairment with occasional confusion regarding the sequence of tasks",
        "Physically active but occasionally forgets to stay hydrated"
    ],
    "goals_and_needs": [
        "Stay healthy and engaged in physical activities",
        "Remember important family events and medication schedules",
        "Maintain independence"
    ],
    "daily_routine": [
        "Morning stretching and yoga in the apartment",
        "Breakfast at 9 AM",
        "Afternoon cooking class",
        "Evening relaxation with television and music"
    ],
    "technology_comfort_level": "High; enjoys using technology to access information online and interact with family and friends",
    "challenges_and_pain_points": [
        "Forgets to drink water throughout the day; sometimes misses medication doses",
        "Experiences anxiety about my health and forgetfulness",
        "Feels lonely at times, and requires company"
    ],
    "desired_features": [
        "Hydration reminders, daily routine tracking, and alerts for missed medications",
        "Sound detection for any distress signals or calls for help"
    ]
}

# Convert lists/dicts to JSON for database storage
def convert_to_json(data):
    return json.dumps(data) if isinstance(data, (list, dict)) else data

# Get database connection
def get_db_connection():
    return sqlite3.connect("user_data.db")  # New database

# Create the user_data table
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        ethnicity TEXT,
        area TEXT,
        city TEXT,
        professional_background TEXT,
        hobbies TEXT,
        likes TEXT,
        dislikes TEXT,
        cognitive_physical_abilities TEXT,
        goals_and_needs TEXT,
        daily_routine TEXT,
        technology_comfort_level TEXT,
        challenges_and_pain_points TEXT,
        desired_features TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Insert user into database
def insert_user(userdata):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO user_data (
        name, age, gender, ethnicity, area, city, professional_background,
        hobbies, likes, dislikes, cognitive_physical_abilities, goals_and_needs,
        daily_routine, technology_comfort_level, challenges_and_pain_points, desired_features
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        userdata['demographics']['name'],
        userdata['demographics']['age'],
        userdata['demographics']['gender'],
        userdata['demographics']['ethnicity'],
        userdata['area'],
        userdata['city'],
        userdata['professional_background'],
        convert_to_json(userdata['hobbies']),
        convert_to_json(userdata['likes']),
        convert_to_json(userdata['dislikes']),
        convert_to_json(userdata['cognitive_physical_abilities']),
        convert_to_json(userdata['goals_and_needs']),
        convert_to_json(userdata['daily_routine']),
        userdata['technology_comfort_level'],
        convert_to_json(userdata['challenges_and_pain_points']),
        convert_to_json(userdata['desired_features'])
    ))

    conn.commit()
    conn.close()
    print("User data inserted successfully.")

# Retrieve all users
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()
    
    columns = [
        "id", "name", "age", "gender", "ethnicity", "area", "city", "professional_background",
        "hobbies", "likes", "dislikes", "cognitive_physical_abilities", "goals_and_needs",
        "daily_routine", "technology_comfort_level", "challenges_and_pain_points", "desired_features"
    ]

    users = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return users

# Retrieve a specific user by ID
def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    
    columns = [
        "id", "name", "age", "gender", "ethnicity", "area", "city", "professional_background",
        "hobbies", "likes", "dislikes", "cognitive_physical_abilities", "goals_and_needs",
        "daily_routine", "technology_comfort_level", "challenges_and_pain_points", "desired_features"
    ]
    
    user = dict(zip(columns, row)) if row else None

    conn.close()
    return user

# Update user information
def update_user(user_id, updated_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE user_data SET
        name = ?, age = ?, gender = ?, ethnicity = ?, area = ?, city = ?, 
        professional_background = ?, hobbies = ?, likes = ?, dislikes = ?, 
        cognitive_physical_abilities = ?, goals_and_needs = ?, daily_routine = ?, 
        technology_comfort_level = ?, challenges_and_pain_points = ?, desired_features = ?
    WHERE id = ?
    ''', (
        updated_data['name'],
        updated_data['age'],
        updated_data['gender'],
        updated_data['ethnicity'],
        updated_data['area'],
        updated_data['city'],
        updated_data['professional_background'],
        convert_to_json(updated_data['hobbies']),
        convert_to_json(updated_data['likes']),
        convert_to_json(updated_data['dislikes']),
        convert_to_json(updated_data['cognitive_physical_abilities']),
        convert_to_json(updated_data['goals_and_needs']),
        convert_to_json(updated_data['daily_routine']),
        updated_data['technology_comfort_level'],
        convert_to_json(updated_data['challenges_and_pain_points']),
        convert_to_json(updated_data['desired_features']),
        user_id
    ))

    conn.commit()
    conn.close()
    print("User data updated successfully.")


def safe_json_loads(value):
    """Safely parse a JSON string into a Python object, return original if parsing fails."""
    try:
        return json.loads(value) if isinstance(value, str) and value.startswith("[") else value
    except json.JSONDecodeError:
        return value

def convert_userdata(userdata):
    # Ensure userdata is a dictionary, in case it's passed as a string
    if isinstance(userdata, str):
        userdata = json.loads(userdata)
    
    # List of keys that should be converted from stringified JSON lists to actual lists
    list_keys = [
        "hobbies", "likes", "dislikes", "cognitive_physical_abilities",
        "goals_and_needs", "daily_routine", "challenges_and_pain_points", "desired_features"
    ]
    
    # Convert only necessary keys
    for key in list_keys:
        userdata[key] = safe_json_loads(userdata[key])

    return f"""My name is {userdata['name']}, and I am a {userdata['age']}-year-old {userdata['gender'].lower()} currently living in {userdata['city']}. 
I am a {userdata['professional_background']} with a deep appreciation for creativity and routine. 
I enjoy hobbies such as {', '.join(userdata['hobbies'])} and love attending art exhibitions. 
I remain physically active, especially in the mornings, and find comfort in structured daily routines. 
However, I dislike {', '.join([dislike.split('.')[0] for dislike in userdata['dislikes']])}. 

I experience {userdata['cognitive_physical_abilities'][0].lower()}. 
Sometimes, I {userdata['cognitive_physical_abilities'][1].lower()}. 
My goals include {', '.join(userdata['goals_and_needs'])}. 
My daily routine consists of {', '.join(userdata['daily_routine'])}. 

I am {userdata['technology_comfort_level'].lower()}. 
However, I struggle with {', '.join([challenge.split(';')[0].lower() for challenge in userdata['challenges_and_pain_points']])}. 
At times, I feel lonely and require companionship. 

To support my well-being, I desire tools such as {', '.join(userdata['desired_features'])}. 
These features would help me maintain a structured lifestyle, ensuring both my health and safety while allowing me to continue enjoying my passions and independence."""


# Delete user by ID
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM user_data WHERE id = ?", (user_id,))
    
    conn.commit()
    conn.close()
    print(f"User with ID {user_id} deleted successfully.")

# Main execution
def get_data():
    #create_table()  # Ensure table exists
    #insert_user(userdata)
    # Insert user data (only insert if empty)
    #if not get_all_users():
        #insert_user(userdata)

    # View all users
    data= json.dumps(get_user_by_id(2), indent=4)
    #print(data)
    converted_string=convert_userdata(data)
    #print(converted_string)
    return converted_string
    #print (x)
    # View a specific user (uncomment and change ID as needed)
    # print(json.dumps(get_user_by_id(1), indent=4))

    # Delete a user (uncomment if needed)
    # delete_user(1)


