def print_stats(data: list[dict]) -> None:
    """
    Accepts a dataset stored as a list of dictionaries.
    Prints each column's name, and its most common value (for text columns)
    or it's average value (for numeric columns)
    """
    
    # assuming that all dictionaries in the list will have same keys
    columns = data[0].keys()

    for column in columns:
        # determine if this is a text or numeric column
        if type(data[0][column]) == float:
            # process this as a numeric column
            total = 0
            count = 0
            for row in data:
                try:
                    value = float(row[column])
                    total += value
                    count += 1
                except ValueError:
                    pass
            if count > 0:
                average = total / count
                print(f"average value for {column}: {average}")

        else:  # this is a text column
            
            # build a dict that counts number of times we've seen each value
            # within this column
            value_counts = dict()
            for row in data:
                value_counts[row[column]] = value_counts.get(row[column], 0) + 1

            # identify the key correponding to the max value
            biggest_count = 0
            most_common = None
            for value, count in value_counts.items():
                if count > biggest_count:
                    biggest_count = count
                    most_common = value
            
            print(f"most common value for {column}: {most_common}")
