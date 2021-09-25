from __future__ import print_function
import argparse
import gspread
import calendar
import time
from tqdm import tqdm
from random import randrange
from datetime import date, datetime, timedelta
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
RECORD_START_INDEX = 6
TITLE_CELL = "B2"
TEMPLATE_WORKSHEET_NAME = "Template"
DATE_COLUMN = "B"
PUNCH_IN_COLUMN = "E"
PUNCH_IN_TIME_RANGE = (-20, 15)
PUNCH_OUT_COLUMN = "F"
PUNCH_OUT_TIME_RANGE = (2, 20)


def main(args):
    credentials = Credentials.from_service_account_file(args.credential, scopes=SCOPES)

    gclient = gspread.authorize(credentials)

    sheet = gclient.open_by_key(args.sheetid)
    for month in tqdm(range(args.startmonth, args.endmonth + 1)):
        new_worksheet = duplicate_sheet(sheet, args.year, month)
        fill_worksheet(new_worksheet, args.year, month)
        time.sleep(20)


def duplicate_sheet(sheet, year, month):
    worksheet = sheet.worksheet(TEMPLATE_WORKSHEET_NAME)
    new_sheet_name = f"{year}/{month}"
    worksheet.duplicate(new_sheet_name=new_sheet_name)

    new_worksheet = sheet.worksheet(new_sheet_name)

    new_title = (
        worksheet.get(TITLE_CELL)
        .first()
        .replace("?", str(year), 1)
        .replace("?", str(month), 1)
    )
    new_worksheet.update(TITLE_CELL, new_title)
    return new_worksheet


def weekday_from_date(current_date):
    return calendar.day_name[current_date.weekday()][0:3]


def fill_worksheet(worksheet, year, month):
    index = RECORD_START_INDEX
    for day in tqdm(range(1, calendar.monthlen(year, month) + 1)):
        current_date = date(year=year, month=month, day=day)
        if current_date.weekday() != 5 and current_date.weekday() != 6:
            worksheet.update(
                f"{DATE_COLUMN}{index}",
                f"{current_date.year}/{current_date.month}/{current_date.day} ({weekday_from_date(current_date)})",
            )
            time.sleep(1)

            punch_in_time = datetime(year, month, day, 9, 0, 0)
            punch_out_time = datetime(year, month, day, 18, 0, 0)
            punch_in_delta = timedelta(
                minutes=randrange(PUNCH_IN_TIME_RANGE[0], PUNCH_IN_TIME_RANGE[1])
            )
            punch_in_time += punch_in_delta
            punch_out_delta = timedelta(
                minutes=randrange(PUNCH_OUT_TIME_RANGE[0], PUNCH_OUT_TIME_RANGE[1])
            )
            punch_out_time += punch_out_delta

            punch_in_time_str = punch_in_time.strftime("%H:%M")
            punch_out_time_str = punch_out_time.strftime("%H:%M")

            worksheet.update(f"{PUNCH_IN_COLUMN}{index}", punch_in_time_str)
            time.sleep(1)
            worksheet.update(f"{PUNCH_OUT_COLUMN}{index}", punch_out_time_str)
            time.sleep(1)
            index += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update previous punch in records.")
    parser.add_argument("-c", "--credential", type=str)
    parser.add_argument("-i", "--sheetid", type=str)
    parser.add_argument("-y", "--year", type=int)
    parser.add_argument("-s", "--startmonth", type=int)
    parser.add_argument("-e", "--endmonth", type=int)
    args = parser.parse_args()
    main(args)
