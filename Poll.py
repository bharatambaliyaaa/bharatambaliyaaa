import csv
import requests
import io
import os
import time
from telegram import Bot

TOKEN = os.environ.get('TOKEN', 'your-telegram-token')
CHANNEL_ID = '@currentadda'
DELAY = 1800  # 30 minutes in seconds
QUESTION_SHEET_URL = 'https://github.com/bharatambaliyaaa/bharatambaliyaaa/blob/09e36b305317723b2459751d6cf203f41455702a/questions.csv'
MAX_EXPLANATION_LENGTH = 4096

def download_questions():
    response = requests.get(QUESTION_SHEET_URL)
    response.raise_for_status()
    return list(csv.reader(io.StringIO(response.text)))

def send_question(question_data):
    question, *options, correct_option, explanation = question_data
    bot = Bot(token=TOKEN)
    poll_options = [str(option) for option in options]
    correct_option_id = int(correct_option) - 1  # Calculate the correct option ID

    if len(explanation) > MAX_EXPLANATION_LENGTH:
        send_question_without_explanation(question, poll_options, correct_option_id)
    else:
        send_combined_question(question, poll_options, correct_option_id, explanation)

def send_combined_question(question, poll_options, correct_option_id, explanation):
    bot = Bot(token=TOKEN)

    poll_data = {
        'chat_id': CHANNEL_ID,
        'question': question,
        'options': poll_options,
        'is_anonymous': True,
        'type': 'quiz',
        'correct_option_id': correct_option_id,
        'explanation': explanation,
    }

    try:
        message = bot.send_poll(**poll_data)
        print(f"Sent question: {question}")
        print(f"Options: {poll_options}")
        print(f"Correct option: {correct_option_id + 1}")
        print(f"Explanation included in the solution.")
        print("")
    except Exception as e:
        print(f"Failed to send question with explanation: {str(e)}")
        send_question_without_explanation(question, poll_options, correct_option_id)

def send_question_without_explanation(question, poll_options, correct_option_id):
    bot = Bot(token=TOKEN)

    poll_data = {
        'chat_id': CHANNEL_ID,
        'question': question,
        'options': poll_options,
        'is_anonymous': True,
        'type': 'quiz',
        'correct_option_id': correct_option_id,
    }

    try:
        message = bot.send_poll(**poll_data)
        print(f"Sent question without explanation: {question}")
        print(f"Options: {poll_options}")
        print(f"Correct option: {correct_option_id + 1}")
        print("Explanation skipped.")
        print("")
    except Exception as e:
        print(f"Failed to send question without explanation: {str(e)}")

def main():
    while True:
        all_questions = download_questions()
        for question in all_questions:
            send_question(question)
            time.sleep(DELAY)

if __name__ == '__main__':
    main()
