
# Jarvis Day 12 : WhatsApp Automation

In this Video We will learn how to import google contacts in sql database and How to automate WhatsApp


## Steps:

#### 1. Create contacts Table 

```bash
# Create a table with the desired columns
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

```

#### 2. Export Google Contacts


#### 3. Import CSV file into database

```bash

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
desired_columns_indices = [0, 30]

# Read data from CSV and insert into SQLite table for the desired columns
with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        selected_data = [row[i] for i in desired_columns_indices]
        cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# Commit changes and close connection
con.commit()
con.close()

```

#### 4. Insert Single contacts (Optional)

```bash
query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890')"
cursor.execute(query)
con.commit()
```

#### 5. Search Contacts from database

```bash
query = 'kunal'
query = query.strip().lower()

cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
results = cursor.fetchall()
print(results[0][0])

```

#### 6. Make Helper Function to remove unwanted words from query

```bash
def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

```
#### 7. Example of Helper Function

```bash
#Example usage
input_string = "make a phone call to pappa"
words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', '']

result = remove_words(input_string, words_to_remove)
print(result)

```

#### 8. Create find contacts number Function in features.py

```bash

# Whatsapp Message Sending
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

``` 

#### 9. Create Whatsapp Function in features.py

```bash

def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

``` 
#### 10. create whatsapp command in command.py

```bash

elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    message = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    message = 'call'
                else:
                    message = 'video call'
                    
                whatsApp(contact_no, query, message, name)

```