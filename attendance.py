import csv
import sys
import os
import pandas as pd
from tempfile import NamedTemporaryFile
import shutil


def create_df(csv_file):
    df = pd.read_csv(csv_file, sep="\t", encoding='utf-16')
    return df


def calculate_total_time(csv_df):
    emails = csv_df['Attendee Email'].unique()
    participants = {}  # {email: total time}
    for email in emails:
        email_df = csv_df.loc[csv_df['Attendee Email'] == email]
        for row in email_df['Attendance Duration']:

            if email in participants:
                participants[email] += int(row[:-5])
            else:
                participants[email] = int(row[:-5])
    return participants


def write_to_new_file(output_file, par_dict):
    # header = ["E-mail", "Total time"]
    data = []
    for name, time in par_dict.items():
        data.append([name, time])
    with open(output_file, "w", encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(header)
        writer.writerows(data)


def update_attendance(new_input, output):
    """parse new webex summary"""
    new_csv_df = create_df(input_file)
    new_participants_dict = calculate_total_time(new_csv_df)
    tempfile = NamedTemporaryFile(mode='w', newline='', delete=False)
    fields = ["E-mail", "Total time"]

    old_participants = []
    with open(output, 'r', newline='') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        # next(reader, None)  # skip the header
        writer = csv.DictWriter(tempfile, fieldnames=fields)

        for row in reader:
            old_participants.append(row['E-mail'])
            if row['E-mail'] in new_participants_dict:
                # updating row
                row['Total time'] = str(int(row['Total time']) + int(new_participants_dict[row['E-mail']]))
                row = {'E-mail': row['E-mail'], 'Total time': row['Total time']}
            """ student did not come today so no update (  row['E-mail'] not in new_participants_dict  ) """
            writer.writerow(row)
    
    # replace output file with temp
    shutil.move(tempfile.name, output)
    csvfile.close()
    """ In case we have a new student """
    new_students = get_new_student(old_participants, new_participants_dict)
    if len(new_students) > 0:
        data = []
        for student in new_students:
            data.append([student[0], student[1]])
        print(data)
        with open(output, "a", encoding='UTF8', newline='') as f_out:
            writer = csv.writer(f_out)
            writer.writerows(data)
    f_out.close()


def get_new_student(old_participants_list, new_participants_dict):
    new_students = []
    for key, val in new_participants_dict.items():
        if key not in old_participants_list:
            new_students.append([key, val])
    return new_students


if __name__ == '__main__':

    input_file = sys.argv[-2]
    output_file = sys.argv[-1]
    
    # input_file = 'participants_input.csv'
    # output_file = 'participants_output_email.csv'
    
    """ check if output file is empty - if so, create one. Else, update current one  """
    if os.stat(output_file).st_size == 0:
        csv_df = create_df(input_file)
        participants_dict = calculate_total_time(csv_df)
        write_to_new_file(output_file, participants_dict)
    else:
        update_attendance(input_file, output_file)

