import pipe_functions as pipeline

if __name__ == '__main__':
    input_files_directory = "input_files"
    merged_file_directory = "merged_file"

    file_names_sorted = pipeline.get_file_names_sorted(input_files_directory)

    print("Starting file formatting")
    pipeline.format_files(file_names_sorted, merged_file_directory + "\\merged.csv")
    print("Finished file formatting")
