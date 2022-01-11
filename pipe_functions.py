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
        print(file_name + " formatted and appended to " + merged_file_path)


def calculate_y(x):
    y = (x / 6) + 511
    if y > 1023:
        y = 1023
    elif y < 0:
        y = 0
    return int(y)


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

        # if line is empty, end of file is reached
        if not line:
            break

        words = line.split(",")
        counter = 0
        for timestamp, x in pairwise(words):
            if timestamp and x:
                row = ",".join([timestamp, str(calculate_y(int(x)))])
                if row.endswith("\n"):
                    output_file.write(row)
                else:
                    output_file.write(row + "\n")
                counter += 1
            else:
                break

    input_file.close()
    output_file.close()


def sort_file(file_path, destination_file_path):
    # "sort {0} /o {1}", fileToSort, outputFileName
    os.system(f"sort {file_path} /o {destination_file_path}")


def get_timestamp_ecg_pair(line):
    words = line.split(",")
    return int(words[0]), int(words[1])


def get_file_name(line, dest_path, file_type):
    timestamp = get_timestamp_ecg_pair(line)[0]
    file_name = "".join([dest_path, "\ecg_", str(timestamp), f".{file_type}"])
    return file_name


def calculate_difference(prev_line, curr_line):
    prev_timestamp = get_timestamp_ecg_pair(prev_line)[0]
    curr_timestamp = get_timestamp_ecg_pair(curr_line)[0]
    return curr_timestamp - prev_timestamp


def how_many_missing_timestamps(prev_line, curr_line):
    diff = calculate_difference(prev_line, curr_line)
    if diff % 8 != 0:
        raise Exception("The difference between timestamps is not dividable by 8.")
    return (diff / 8) - 1


def are_there_missing_timestamps(prev_line, curr_line):
    return how_many_missing_timestamps(prev_line, curr_line) > 0


def get_missing_timestamps(prev_line, curr_line, dest_file):
    prev_timestamp = get_timestamp_ecg_pair(prev_line)[0]
    curr_timestamp = get_timestamp_ecg_pair(curr_line)[0]

    for to_add in range(prev_timestamp + 8, curr_timestamp, 8):
        dest_file.write("".join([str(to_add), ",-1\n"]))


def remove_timestamp(line):
    words = line.split(",")
    return words[1]


def convert_to_ecg(src_file_path, dest_file_path):
    src_file = open(src_file_path, "r")
    ecg_file = open(dest_file_path, "a+")
    while True:
        line = src_file.readline()

        if not line:
            break

        if line != '\n':
            ecg_file.write(remove_timestamp(line))

    print(f"Converted {src_file_path} to ECG.")
    return dest_file_path


def check_and_fill_in_blanks(src_file_path, csv_dest_dir_path, ecg_dest_dir_path):
    src_file = open(src_file_path, "r")
    prev_line = src_file.readline()
    temp_csv_file_name = get_file_name(prev_line, csv_dest_dir_path, "csv")
    dest_ecg_file_name = get_file_name(prev_line, ecg_dest_dir_path, "ecg")
    dest_file = open(temp_csv_file_name, "a+")
    while True:
        # Get next line from file
        curr_line = src_file.readline()

        # if line is empty, end of file is reached
        if not curr_line:
            break

        if are_there_missing_timestamps(prev_line, curr_line):
            if calculate_difference(prev_line, curr_line) > 30000:
                dest_file.write(prev_line)
                dest_file.close()
                convert_to_ecg(temp_csv_file_name, dest_ecg_file_name)
                prev_line = curr_line
                temp_csv_file_name = get_file_name(prev_line, csv_dest_dir_path, "csv")
                dest_ecg_file_name = get_file_name(prev_line, ecg_dest_dir_path, "ecg")
                dest_file = open(temp_csv_file_name, "a+")
                continue
            else:
                get_missing_timestamps(prev_line, curr_line, dest_file)

        dest_file.write(prev_line)
        prev_line = curr_line

    dest_file.close()
    convert_to_ecg(temp_csv_file_name, dest_ecg_file_name)
