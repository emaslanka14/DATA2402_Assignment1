def load_from_csv(filename: str) -> list[dict]:
    """
    reads a dataset in CSV format. converts numeric data to float.
    raises an AttributeError if the table rows do not all have the same number of values.
    :param filename: the file path of the csv data to read
    :return: the dataset as a list of dictionaries - one dict per object in the file
            each dictionary should map column names to values
    """
    with open(filename, 'r') as file:
        all_rows = []

        # process the first line, pull out the column names
        first_line = file.readline().strip()
        columns = first_line.split(',')

        # process the rest of the text: the table body
        for line in file:
            line = line.strip()
            values = line.split(',')

            # check the row has the right number of values in it
            if len(values) != len(columns):
                raise Exception(f'wrong number of values in row: {line}')

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
                raise Exception(f'wrong number of values in row: {row_text}')

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

def save_as_json(table: list[dict], filename:str) -> None:
    """
    saves a dataset in JSON format.
    :param table: the dataset to save
    :param filename: the file path of the json data to write
    """
    jsonName = filename + '.json'
    all_formatted_rows = []

    for row in table:
        formatted_items = []
        for key, value in row.items():
            #print("key: ", key, "type: ", type(key), "value: ", value, "type: ", type(value))
            jsonKey = f'"{key}"'

            if type(value) == str:
                jsonValue = f'"{value}"'
            else:
                jsonValue = str(value)

            formatted_items.append(f"{jsonKey}: {jsonValue}")

        row_string = "{" + ", ".join(formatted_items) + "}"

        #print("row_string: ", row_string)
        all_formatted_rows.append(row_string)

    final_json_string = "[\n  " + ",\n  ".join(all_formatted_rows) + "\n]"


    with open(jsonName, 'w') as file:
        file.write(final_json_string)

    




