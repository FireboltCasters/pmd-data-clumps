# analysis.py
import asyncio
import os
import json
from datetime import datetime

# import DetectorOptions
from .detectorOptions import DetectorOptions
from .softwareProjectDicts import SoftwareProjectDicts
from .detectorDataClumpsFields import DetectorDataClumpsFields

async def detect(ast_output_folder, output_data_clumps_file, detector_options_file):
    print("Analysis Started")
    abs_ast_output_folder = os.path.abspath(ast_output_folder)
    abs_output_data_clumps_file = os.path.abspath(output_data_clumps_file)
    abs_detector_options_file = os.path.abspath(detector_options_file)

    print(f"Loading detector options from {abs_detector_options_file}")
    detector_options = DetectorOptions.load_config_from_file(abs_detector_options_file)
    print(f"Loaded detector options")

    print("SoftwareProjectDicts initialization started")
    software_project_dicts = SoftwareProjectDicts(abs_ast_output_folder)
    print("SoftwareProjectDicts initialization done")

    # Initialize dataClumpsTypeContext dictionary
    data_clumps_type_context = {
        "report_version": "0.1.93",
        "report_timestamp": datetime.now().isoformat(),
        "target_language": "Java",  # Replace with actual value
        "report_summary": {},
        "project_info": {
            "project_name": "Your Project Name",  # Replace with actual value
            "project_version": "Your Project Version",  # Replace with actual value
            "project_commit": "Your Project Commit",  # Replace with actual value
            "additional": "Additional Info"  # Replace with actual value
        },
        "detector": {
            "name": "FireboltCasters/pmd-data-clumps",
            "version": "0.1.93",
            "options": detector_options.options
        },
        "data_clumps": {}
    }

    print("Detecting software project for data clumps (done)")
    print("Detecting software project for data clumps")


    '''
    detector_data_clumps_methods = DetectorDataClumpsMethods(detector_options, None, None)
    common_method_parameters = await detector_data_clumps_methods.detect(abs_ast_output_folder)

    if common_method_parameters:
        for key, value in common_method_parameters.items():
            data_clumps_type_context['data_clumps'][value['key']] = value
    '''


    detector_data_clumps_fields = DetectorDataClumpsFields(detector_options.options)
    common_fields = await detector_data_clumps_fields.detect(software_project_dicts)

    if common_fields:
        for key, value in common_fields.items():
            data_clumps_type_context['data_clumps'][value['key']] = value

    data_clumps_type_context['report_summary'] = {
        'amount_data_clumps': len(data_clumps_type_context['data_clumps'])
    }


    # Save the result to abs_output_data_clumps_file
    with open(abs_output_data_clumps_file, 'w') as f:
        json.dump(data_clumps_type_context, f, indent=4)
