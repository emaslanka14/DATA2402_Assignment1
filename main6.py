from file_IO import load_from_html, load_from_csv, save_as_json
from data_processing import print_stats
def main(filename: str='data/census_dataset.txt'): 
    # load data
    try:
        with open(filename, 'r') as file:

            firstLine = None
            for line in file:
                stripped = line.strip()
                if stripped:
                    firstLine = stripped
                    break

            if firstLine is None:
                raise Exception(f"File was found, but had no text content for file: {filename}")

            #print(f"First line of the file: {firstLine}")
            if firstLine.startswith('<table>'):
                table = load_from_html(filename)
            elif ',' in firstLine:
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

if __name__ == "__main__":
    main()
