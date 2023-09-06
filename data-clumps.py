import argparse
import subprocess
import asyncio
import os
from astAnalyse.detector import detect
from astAnalyse.detectorOptions import generateDetectorOptionsFile, DetectorOptionsInformation

temp_ast_output_folder = "./temp_ast_output_folder"
default_detector_options_file = "./detector-options.json"
default_output_data_clumps_file = "./data-clumps-result.json"

def run_make_command(directory, ast_output_folder=temp_ast_output_folder):
    abs_directory = os.path.abspath(directory)
    abs_ast_output_folder = os.path.abspath(ast_output_folder)
    cmd = f"make run DIRECTORY={abs_directory} OUTPUT_FOLDER={abs_ast_output_folder}"
    subprocess.run(cmd, shell=True, cwd="./astGenerator")


# async def detect # defined in astAnalyse/detector.py

def main():
    parser = argparse.ArgumentParser(description="Data Clumps Script")

    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    parse_ast_parser = subparsers.add_parser("parseAst", help="Parse AST from source files")
    parse_ast_parser.add_argument("--source", required=True, help="Path to the source file")
    parse_ast_parser.add_argument("--output", help="Path to the output directory for parsed AST")

    analyse_ast_files_parser = subparsers.add_parser("analyseAstFiles", help="Analyse AST files")
    analyse_ast_files_parser.add_argument("--source", required=True, help="Path to the directory containing parsed AST files")
    analyse_ast_files_parser.add_argument("--output", help="Path to the detection output file", default=default_output_data_clumps_file)
    analyse_ast_files_parser.add_argument("--config", help="Path to the config file containing detector options")

    detect_parser = subparsers.add_parser("detect", help="Detect data clumps in source files")
    detect_parser.add_argument("--source", required=True, help="Path to the source file")
    detect_parser.add_argument("--output", help="Path to the detection output file", default=default_output_data_clumps_file)
    detect_parser.add_argument("--config", help="Path to the config file containing detector options. You can generate a default config file using 'python3 data-clumps.py config --generate'")

    config_parser = subparsers.add_parser("config", help="Create a config file for detector options")
    config_parser.add_argument("--show-info", action='store_true', help="Show detector options information")
    config_parser.add_argument("--generate", action='store_true', help="Generate a default config file")

    args = parser.parse_args()

    if args.command is None:
        print("Usage: python3 data-clumps.py detect --source <source_project_directory>")
        print("Run 'python3 data-clumps.py -h' for more information.")
        exit(1)

    if args.command == "parseAst":
        run_make_command(args.source, args.output)

    elif args.command == "analyseAstFiles":
        asyncio.run(detect(args.source, args.output, args.config))

    if args.command == "config":
        if args.show_info:
            print("Detector Options Information:")
            for key, value in DetectorOptionsInformation.items():
                print(f"{key}:")
                print(f"  Label: {value['label']}")
                print(f"  Description: {value['description']}")
                print(f"  Default Value: {value['defaultValue']}")
                print(f"  Group: {value['group']}")
                print(f"  Type: {value['type']}")
                print()
        elif args.generate:
            generateDetectorOptionsFile(default_detector_options_file)
        else:
            print("Usage for config command:")
            print("  --show-info : Show detector options information")
            print("  --generate  : Generate a default config file")
            exit(1)

    elif args.command == "detect":
        run_make_command(args.source, temp_ast_output_folder)
        asyncio.run(detect(temp_ast_output_folder, args.output, args.config))

if __name__ == "__main__":
    main()
