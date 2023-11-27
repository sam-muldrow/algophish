from bs4 import BeautifulSoup
import csv
import os
import random

phish_directory_path = '../capture_data/phish_out'
real_directory_path = '../capture_data/real_out'

def createCsvFileFromLabeledDataLists(labeledDataList):
    print(f"Creating csv with label {labeledDataList}")
    data = [
        ["is_phish", "text"]
    ]
    for labeledData in labeledDataList:
        data.append(labeledData)
    csv_file_path = 'output.csv'
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)



def createListOfLabeledDataFromDir(directory_path, label):
    print(f"createListOfLabeledDataFromDir {directory_path}, {label}")
    cleaned_text_list = readFilesFromDirAndReturnText(directory_path)
    labeledData = []
    print(f"wowie {directory_path}, {label}")
    for clean_text in cleaned_text_list:
        labeledData.append(addCleanTextToListWithLabel(label, clean_text))
    return labeledData

def addCleanTextToListWithLabel(label, cleaned_text):
    print(f"addCleanTextToListWithLabel {label}")
    outputList = [label, cleaned_text]
    return outputList

def readFilesFromDirAndReturnText(directory_path):
    textList = []
    # Iterate through all files in the directory
    count = 0
    for filename in os.listdir(directory_path):
        print(f"doing file {count}/{len(os.listdir(directory_path))}")
        # Check if the path is a file (not a subdirectory)
        if os.path.isfile(os.path.join(directory_path, filename)):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                cleaned_text = ' '.join(soup.stripped_strings)
                print(cleaned_text)
                textList.append(cleaned_text)
        count +=1
    return textList

#process phish dir
phishLabels = createListOfLabeledDataFromDir('../capture_data/phish_out/', 1)
realLabels = createListOfLabeledDataFromDir('../capture_data/real_out/', 0)

labeledDataList = list(zip(phishLabels, realLabels))

random.shuffle(labeledDataList)

createCsvFileFromLabeledDataLists(labeledDataList)
