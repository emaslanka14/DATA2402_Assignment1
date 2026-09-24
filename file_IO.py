

def load_from_html(filename: str) -> list[dict]:
    """
    reads a dataset in HTML format. converts numeric data to float.
    raises an AttributeError if the table rows do not all have the same number of values.
    :param filename: the file path of the html data to read
    :return: the dataset as a list of dictionaries - one dict per object in the file
            each dictionary should map column names to values
    """    
    with open(filename, 'r') as file:
        contents = file.read()
        all_rows = []

        head, body = contents.split('</thead>')

        # process the head first, pull out the column names
        head_parts = head.split('<td>')

        columns = []
        for column_name in head_parts[1:]:
            columns.append(
                column_name.replace('</td>', '').replace('</tr>', '').strip()
            )
        
        # strip off some unecessary tags
        body = body.replace('</tr>', '')
        body = body.replace('</tbody>\n</table>', '')

        # process the rest of the text: the table body
        rows_text = body.split('<tr>')
        for row_text in rows_text[1:]: # skip the first, which just has a <tbody> tag
            row_text = row_text.replace('</td>', '')
            values = row_text.split('<td>')
            values = values[1:]

            # check the row has the right number of values in it
            if len(values) != len(columns):
                raise AttributeError(f'wrong number of values in row: {row_text}')

            this_row_dict = dict()
            for i in range(len(columns)):
                this_column = columns[i]
                this_value = values[i].strip()

                # convert to float if the value is a number
                try:
                    this_value = float(this_value)
                except ValueError:
                    pass

                this_row_dict[this_column] = this_value
            
            all_rows.append(this_row_dict)
    
    return all_rows

def load_from_csv(filename: str) -> list[dict]:

    with open(filename, 'r') as file:
        contents = file.read(200)

    all_rows = []

    lines = contents.strip().splitlines()

    if len(lines) < 2:
        raise ValueError('CSV needs a header and at least one row')

    columns = []
    for column_name in lines[0].split(','):
        columns.append(column_name.strip())

    all_rows = []
    for line in lines[1:]:
        if line.strip() == '':
            continue
        values = line.split(',')

        if len(values) != len(columns):
            raise AttributeError(f'Wrong number of values in row: {line}')

        this_row_dict = dict()
        for i in range(len(columns)):
            this_column = columns[i]
            this_value = values[i].strip()

            try:
                this_value = float(this_value)
            except ValueError:
                pass
            this_row_dict[this_column] = this_value

        all_rows.append(this_row_dict)

    return all_rows

    
def load_dataset(filename: str) -> list[dict]:
    with open(filename, 'r') as file:
        contents = file.read()

    # HTML check: look for a table tag, case-insensitive
    looks_like_html = '<table' in contents.lower()

    try:
        if looks_like_html:
            return load_from_html(filename)
        return load_from_csv(filename)
    except (ValueError, AttributeError, IndexError):
        raise AttributeError("Error, data must be in valid CSV or HTML format") from None


def save_to_json(data: list[dict], filename: str) -> None:
    with open(filename, 'w') as file:
        file.write('[\n')

        for i in range(len(data)):
            row = data[i]
            file.write('  {\n')

            keys = list(row.keys())
            for j in range(len(keys)):
                key = keys[j]
                value = row[key]

                if type(value) == float:
                    value_text = str(value)
                else:
                    value_text = '"' + str(value) + '"'

                if j < len(keys) - 1:
                    file.write(f'    "{key}": {value_text},\n')
                else:
                    file.write(f'    "{key}": {value_text}\n')

            if i < len(data) - 1:
                file.write('  },\n')
            else:
                file.write('  }\n')

        file.write(']\n')