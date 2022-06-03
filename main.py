# This program is used to get unique users from the imported CSVs
# within the selected date on a GUI
# Created by: Johan Setiawan

# Import the necessary library(s)
from calendar import Calendar
import tkinter
from tkcalendar import *
from datetime import datetime

import pandas as pd
import glob

main_window = tkinter.Tk()
main_window.geometry("400x600")
main_window.title("Onlead Unique Users Counter")

# The function is to collect the selected start and end dates
def collect_start_end_date():

    start_date = date_convert(cal1.get_date())

    end_date = date_convert(cal2.get_date())

    # Get CSV files list from a folder
    path = '/Users/johansetiawan.onstock/Desktop/Sentry Error'
    csv_files = glob.glob(path + "/*.csv")

    # Read each CSV files as a list
    df_list = (pd.read_csv(file) for file in csv_files)

    # Concatenate all DataFrames from list of DFs to a big df
    big_df = pd.concat(df_list, ignore_index=True)

    # Drop unused columns
    big_df_cleaned = big_df.drop(["value", "id", "username", "ip_address", "times_seen", "first_seen"], axis=1, inplace=True)

    # Change the data type of "last_seen" to date
    big_df['last_seen'] = pd.to_datetime(big_df['last_seen'])
    big_df['last_seen'] = big_df['last_seen'].dt.date

    # Remove duplicates users
    big_df = big_df.drop_duplicates(keep='last')
       
    # Get the rows that satisfy the start and the end date
    no_of_users = big_df[(big_df['last_seen'] >= start_date) & (big_df['last_seen'] <= end_date)] 
    no_of_users_str = str(no_of_users.shape[0])

    # Print the no. of unique users that satisfy the date
    result_label.config(text="No. of unique users: " + no_of_users_str +" users.")

def date_convert(input_date):
    date_obj = datetime.strptime(input_date, '%m/%d/%y')
    new_date = datetime.strftime(date_obj, "%Y-%m-%d")
    final_date = datetime.strptime(new_date, '%Y-%m-%d').date()

    return final_date

title = tkinter.Label(main_window, text="\nPlease pick \n Start and End dates:\n")
title.pack()

start_title = tkinter.Label(main_window, text="\nStart date:")
start_title.pack()
cal1 = Calendar(main_window, selectmode="day")
cal1.pack(pady=5)

end_title = tkinter.Label(main_window, text="\nEnd date:")
end_title.pack()
cal2 = Calendar(main_window, selectmode="day")
cal2.pack(pady=5)

# Label to display date
result_label = tkinter.Label(main_window, text="")
result_label.pack(pady=10, padx=5)

# Button
button = tkinter.Button(main_window, text="submit", command=collect_start_end_date)
button.pack()

# mainloop() is to let the window run until it is closed
main_window.mainloop()

