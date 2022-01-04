import pipe_functions as pipeline

if __name__ == '__main__':
    file_names_sorted = pipeline.get_file_names_sorted("input_files")

    print("Starting file formatting")
    pipeline.format_files(file_names_sorted, "merged_file/merged.csv")
    print("Finished file formatting")
