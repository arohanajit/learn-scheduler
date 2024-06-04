import csv
import os
import openai
from dotenv import load_dotenv
import os

# load_dotenv()
api_key = os.getenv('API_KEY')
openai.api_key = api_key

# Load your OpenAI API key from an environment variable or directly set it here
  # Replace with your OpenAI API key if not using environment variable

def read_events_from_csv(file_path):
    events = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            events.append(row)
    return events

def format_events_for_prompt(events):
    prompt = "Here are the upcoming events:\n"
    for event in events:
        prompt += f"- {event['Start']}: {event['Summary']} (Calendar: {event['Calendar']})\n"
    prompt += "\nI need to learn Python, update my schedule accordingly"
    return prompt

def get_summary_from_openai(prompt):
    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",    
      messages=[
        {"role": "system", "content": "You are a personal assistant who is expert at scheduling. You'll be provided with weekly schedule and you need to specify time period in the schedule where user can dedicate time to learning a technology. Take into account average number of hours to be dedicated based on the technology name provided. Also take into account breaks that need to be take as per events in the schedule. Only specify time schedule to learn. Nothing else."},
        {"role": "user", "content": prompt}
      ]
    )

    summary = response.choices[0].message.content
    return summary

def write_time_slots_to_file(data):
    """
    Write the given data to a text file.

    Parameters:
    data (str): The data to write to the file.
    """
    with open("new.txt", 'w') as file:
        file.write(data)
    print(f"Data has been written to new.txt")

def main():
    file_path = 'events.csv'
    events = read_events_from_csv(file_path)
    prompt = format_events_for_prompt(events)
    summary = get_summary_from_openai(prompt)
    write_time_slots_to_file(summary)
    print("Summary of Events:")
    print(summary)

if __name__ == '__main__':
    main()