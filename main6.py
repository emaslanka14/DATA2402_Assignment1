import file_IO
from data_processing import print_stats


# load data
filename = 'student_dataset.txt'
table = file_IO.load_dataset(filename)

# print table statistics
print_stats(table)

file_IO.save_to_json(table, 'output.txt')