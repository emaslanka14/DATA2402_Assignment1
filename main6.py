from file_IO import load_from_html, load_from_csv
from data_processing import print_stats

# load data
filename = 'data/student_dataset.txt'

try:
    file = open(filename, 'r')
except FileNotFoundError:
    print(f"Error: File not found - {filename}")
    exit(1)

try:
    while True:
        firstLine = file.readline().strip()
        # continue parsing until we find a non-empty line, to check the file format
        if firstLine == '':
            continue
        else:
            file.close()
            break
    
    if firstLine.startswith('<table>'):
        table = load_from_html(filename)
    elif firstLine.find(',') != -1:
        table = load_from_csv(filename)
    else:
        raise Exception(f"Incompatiable file format for file: {filename}, please provide a properly formatted table in CSV or HTML format.")

except Exception as e:
    print(f"Error loading data: {e}")

else:
    # print stats
    print_stats(table)