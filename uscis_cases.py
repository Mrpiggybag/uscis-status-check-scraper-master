import os
import csv
import re

# Replace this with the path to the directory containing the text files
Directory_Path = os.getcwd()

# Find all case id numbers from file contents
def all_cases(File_Contents):
    case_number_match =re.findall(r'[A-Z]{3}[0-9]{10}', File_Contents)
    if case_number_match:
        case_number = case_number_match
    else:
        case_number = ''
    return case_number



def file_data(directory_path=Directory_Path):

    # Create a list to store the file names and contents
    file_data = []
    # Loop through all the files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'r') as file:
                file_contents = file.readlines()
                case_ids=''.join(file_contents)
                file_data.append([file_name.replace('.txt',''), all_cases(case_ids)])
    return file_data

if 0:
    # Write the file names and contents to a CSV file
    with open('uscis_cases_combined_file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Name', 'File Contents'])
        for data in file_data:
            writer.writerow(data)
    print(file_data())