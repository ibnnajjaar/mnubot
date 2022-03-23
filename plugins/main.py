from collections import defaultdict
from datetime import date

from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message

from models.period import Period
from models.subject import Subject
from prettytable import PrettyTable, ALL


@Client.on_message(filters.command('start'))
def start_command(bot, message: Message):
    message.reply("Hello")

@Client.on_message(filters.command('subjects'))
def list_subjects(bot, message: Message):
    subjects = Subject().all()
    subject_table = PrettyTable()
    subject_table.hrules=ALL
    subject_table.field_names = ["Subjects"]
    for subject in subjects:
        subject_table.add_row([
            subject.name + "(" + subject.code + ")\n" +
            "by: " + subject.lecturer
        ])
    subject_table.align["Subjects"] = "l"
    message.reply_text("```" + subject_table.get_string() + "```",parse_mode='markdown')

@Client.on_message(filters.command('table'))
def list_timetable(bot, message: Message):
    # Fetch all periods collection
    all_periods = Period().all()
    # Group all periods by day
    sorted_periods = defaultdict(list)
    for period in all_periods:
        sorted_periods[period.weekday].append(period)

    # foreach group in grouped results
    for weekday in sorted_periods:
        periods = sorted_periods[weekday]
        period_table = format_periods(periods, weekday)
        message.reply_text(f"```{period_table.get_string()}```",parse_mode='markdown')

@Client.on_message(filters.command('today'))
def list_today_timetable(bot, message: Message):
    # Get today's name
    today = date.today().strftime('%A')
    # Filter periods by day
    periods = Period().where('weekday', today).get()
    # Display the periods
    period_table = format_periods(periods, today)
    message.reply_text(f"```{period_table.get_string()}```",parse_mode='markdown')

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
        subject = Subject().where('id', period.subject_id).first()

        period_table.add_row([
            period.start_at + "\n" + period.end_at,
            subject.name,
            period.location
        ])

    return period_table