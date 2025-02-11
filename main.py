import argparse

from helper import compile_all, create_dataset_file, download

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--copy", action="store_true", help="Copys C files to specified folder.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints extra information.")
    parser.add_argument("--source_dir", default="sources", help="Directory for downloads.")
    parser.add_argument("--sources_file", default="sources/sources.txt", help="File with list of sources (links).")
    parser.add_argument("--copy_dir", default="copy", help="Directory to copy C files to. Only used if -c/--copy is set.")
    parser.add_argument("--assembly_dir", default="assembly", help="Directory to store assembly files.")
    parser.add_argument("--dataset_file", default="dataset.txt", help="File to store dataset.")
    parser.add_argument("--eos", default="<|endoftext|>", help="End of sequence token.")
    args = parser.parse_args()

    download(source_dir=args.source_dir, sources_file=args.sources_file, verbose=args.verbose)
    compile_all(source_dir=args.source_dir, copy=args.copy, copy_dir=args.copy_dir, verbose=args.verbose)
    create_dataset_file(source_dir=args.source_dir, dest_file=args.dataset_file, eos=args.eos)
