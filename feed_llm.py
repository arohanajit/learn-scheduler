import csv
import os
from openai import OpenAI

client = OpenAI(api_key="sk-proj-BnsnZ8AxBfQA3eZJrHCLT3BlbkFJQ2yjUYG7dAENorvNI7AL")
import os

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
    prompt += "\nPlease provide a summary of these events."
    return prompt

def get_summary_from_openai(prompt):
    response = client.completions.create(model="gpt-4o",  # Use the appropriate engine
    prompt=prompt,
    max_tokens=150,  # Adjust as necessary
    n=1,
    stop=None,
    temperature=0.7)
    summary = response.choices[0].text.strip()
    return summary

def main():
    file_path = 'events.csv'
    events = read_events_from_csv(file_path)
    prompt = format_events_for_prompt(events)
    summary = get_summary_from_openai(prompt)
    print("Summary of Events:")
    print(summary)

if __name__ == '__main__':
    main()