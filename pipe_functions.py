import os


def get_file_names_sorted(path):
    if os.path.isdir(path):
        files_list = ["/".join([path, file]) for file in os.listdir(path) if file.endswith(".csv")]
        files_list.sort()
        return files_list
    else:
        raise Exception("Directory not found")


def format_files(input_file_names, merged_file_path):
    for file_name in input_file_names:
        format_lines_and_append_to_merged_file(file_name, merged_file_path)
        print(file_name+" formatted and appended to "+merged_file_path)

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

def format_lines_and_append_to_merged_file(input_file_path, merged_file_path):
    input_file = open(input_file_path, 'r')
    output_file = open(merged_file_path, 'a+')
    while True:
        # Get next line from file
        line = input_file.readline()

        # if line is empty
        # end of file is reached
        if not line:
            break

        words = line.split(",")
        counter = 0
        for timestamp, x in pairwise(words):
            if timestamp and x:
                row = ",".join([timestamp, x])
                if row.endswith("\n"):
                    output_file.write(row)
                else:
                    output_file.write(row+"\n")
                counter += 1
            else:
                break

    input_file.close()
    output_file.close()