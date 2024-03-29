from datetime import date
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from actions.create_subjects_prettytable import create_subjects_prettytable
from database.migrations.subscribers import migrate_subscribers_table
from models.period import Period
from models.subject import Subject
from prettytable import PrettyTable, ALL
from models.subscriber import Subscriber

@Client.on_message(filters.command('start'))
def start_command(bot, message: Message):
    Subscriber().register(message.from_user.id)
    message.reply(f"Assalam Alaikum {message.from_user.first_name}!")
    message.reply("To personalize the experience, you may subscribe to your own subjects "
                  "and get notifications accordingly. I hope this bot will be useful to you.\n\n"
                  "If you would like to request for a feature. Enter command /feedback and "
                  "explain what you want in detail.")

@Client.on_message(filters.command('subjects'))
def list_subjects(bot, message: Message):
    subjects = Subject().all()
    subject_table = create_subjects_prettytable(subjects)
    message.reply_text(f"```{subject_table.get_string()}```",parse_mode='markdown')

@Client.on_message(filters.command('table'))
def list_timetable(bot, message: Message):
    # Fetch all periods collection
    unsorted_periods = Period().all()
    sorted_periods = Period().sort_by_weekday(unsorted_periods)
    periods_output = ""
    # foreach group in grouped results
    for weekday in sorted_periods:
        periods = sorted_periods[weekday]
        period_table = format_periods(periods, weekday)
        periods_output += f"```{period_table.get_string()}```"

    message.reply_text(periods_output,parse_mode='markdown')

@Client.on_message(filters.command('today'))
def list_today_timetable(bot, message: Message):
    today = date.today().strftime('%A')
    periods = Period().today()
    period_table = format_periods(periods, today)
    message.reply_text(f"```{period_table.get_string()}```",parse_mode='markdown')

@Client.on_message(filters.command('migrate'))
def migrate_database(bot, message: Message):
    migrate_subscribers_table()

@Client.on_message(filters.text)
def default_message(bot, message):
    message.reply("I am sorry, I dont understand your text! Please check the menu")


def format_periods(periods, weekday):
    period_table = PrettyTable()
    period_table.field_names = ["Time", "Subject", "Location"]
    period_table.hrules = ALL
    period_table.title = weekday
    period_table.align["Time"] = "l"
    period_table.align["Subject"] = "l"
    period_table.align["Location"] = "l"

    for period in periods:
        period_table.add_row([
            period.start_at + "\n" + period.end_at,
            period.subject_name,
            period.location
        ])

    return period_table