from file_IO import load_from_html, load_from_csv, save_as_json
from data_processing import print_stats

# load data
filename = 'data/census_dataset.txt'
try:
    with open(filename, 'r') as file:
        while True:
            firstLine = file.readline().strip()
            # continue parsing until we find a non-empty line, to check the file format
            if firstLine == '':
                continue
            else:
                file.close()
                break
        #print(f"First line of the file: {firstLine}")
        if firstLine.startswith('<table>'):
            table = load_from_html(filename)
        elif firstLine.find(',') != -1:
            table = load_from_csv(filename)
        else:
            raise Exception(f"Incompatiable file format for file: {filename}, please provide a properly formatted table in CSV or HTML format.")
except FileNotFoundError:
    print(f"Error: Could not find the file '{filename}'. Please check the file path.")

except Exception as e:
    print(f"Error loading data: {e}")

else:
    # print stats
    print_stats(table)
    save_as_json(table, filename)
