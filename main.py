import pipe_functions as pipeline
import time

if __name__ == '__main__':
    input_files_directory = "input_files"
    merged_file_directory = "merged_file"
    sorted_file_directory = "sorted_file"
    output_csv_files_directory = "output_csv_files"
    output_ecg_files_directory = "output_ecg_files"

    file_names_sorted = pipeline.get_file_names_sorted(input_files_directory)
    print("File names read.")

    path_to_merged_file = merged_file_directory + "\\merged.csv"
    print("Starting file formatting and merging")
    pipeline.format_files(file_names_sorted, path_to_merged_file)
    print("Finished file formatting and merging")

    path_to_sorted_file = sorted_file_directory + "\\sorted.csv"
    print("Starting merged file sorting")
    start = time.time()
    pipeline.sort_file(path_to_merged_file, path_to_sorted_file)
    end = time.time()
    print(f"Finished sorting file {path_to_merged_file} in {end - start} seconds. Result is in {path_to_sorted_file}.")

    print("Filling in the blanks")
    pipeline.check_and_fill_in_blanks(path_to_sorted_file, output_csv_files_directory, output_ecg_files_directory)
    print("FINISHED")


