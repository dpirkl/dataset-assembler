import argparse

from helper import compile_all, create_dataset_file, download

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints extra information.")
    parser.add_argument("--full_code", action="store_true", help="Store full code in dataset and not only instructions.")
    parser.add_argument("--source_dir", default="sources", help="Directory for downloads.")
    parser.add_argument("--sources_file", default="sources/sources.txt", help="File with list of sources (links).")
    parser.add_argument("-c", "--copy", action="store_true", help="Copys C files to specified folder.")
    parser.add_argument("--copy_dir", default="copy", help="Directory to copy C files to. Only used if -c/--copy is set.")
    parser.add_argument("--assembly_dir", default="assembly", help="Directory to store assembly files.")
    parser.add_argument("--dataset_file", default="dataset.txt", help="File to store dataset.")
    parser.add_argument("--tokenized_dataset_file", default="dataset_tokenized.txt", help="File to store tokenized dataset.")
    parser.add_argument("--eos", default="<|endoftext|>", help="End of sequence token.")
    parser.add_argument("--skip_tokenize", action="store_true", help="Skip tokenization.")
    parser.add_argument("--model_name", default="Qwen/Qwen2.5-Coder-0.5", help="Model name for tokenizer. Uses Huggingface's transformers.")
    parser.add_argument("--skip_download", action="store_true", help="Skip download.")
    parser.add_argument("--skip_compile", action="store_true", help="Skip compile.")
    args = parser.parse_args()

    if not args.skip_download:
        download(source_dir=args.source_dir, sources_file=args.sources_file, verbose=args.verbose)
    if not args.skip_compile:
        compile_all(source_dir=args.source_dir, copy=args.copy, copy_dir=args.copy_dir, verbose=args.verbose)
    create_dataset_file(
        assembly_dir=args.assembly_dir,
        dataset_file=args.dataset_file,
        toknized_dataset_file=args.tokenized_dataset_file,
        eos=args.eos,
        full_code=args.full_code,
        skip_tokenize=args.skip_tokenize,
        model_name=args.model_name
    )
