import csv
import time
from telegram import Bot
import os


TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
DELAY = 10  # Increased delay between each question (in seconds)
QUESTION_SHEET = 'questions.csv'
MAX_EXPLANATION_LENGTH = 4096

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

def read_questions(sheet):
    with open(sheet, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        return [row for row in reader]

def main():
    all_questions = read_questions(QUESTION_SHEET)
    for question in all_questions:
        send_question(question)
        time.sleep(DELAY)

if __name__ == '__main__':
    main()
