from helper import compile_all, create_dataset_file, download, extract_c_files

if __name__ == "__main__":
    download()
    extract_c_files()
    compile_all()
    create_dataset_file()
