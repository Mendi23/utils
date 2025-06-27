#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "chardet",
# ]
# ///

import argparse

import chardet


def convert_to_utf8(input_file_path, output_file_path):
    # Detect the encoding of the input file
    with open(input_file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        input_encoding = result["encoding"]
        confidence = result["confidence"]

    print(f"Detected encoding: {input_encoding} (confidence: {confidence:.2f})")

    # Open the input file with the detected encoding
    with open(input_file_path, "r", encoding=input_encoding) as input_file:
        # Read the content of the file
        content = input_file.read()

    # Open the output file with UTF-8 encoding
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        # Write the content to the output file
        output_file.write(content)

    print(f"Successfully converted {input_file_path} to UTF-8 encoding")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert file to UTF-8 encoding, overwriting the original file"
    )
    parser.add_argument("input_file", help="Path to the input file")
    args = parser.parse_args()
    convert_to_utf8(args.input_file, args.input_file)
