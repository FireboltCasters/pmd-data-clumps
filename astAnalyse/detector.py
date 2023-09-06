# analysis.py
import asyncio
import os

# import DetectorOptions
from .detectorOptions import DetectorOptions

async def detect(ast_output_folder, output_data_clumps_file, detector_options_file):
    print("Analysis Started")
    abs_ast_output_folder = os.path.abspath(ast_output_folder)
    abs_output_data_clumps_file = os.path.abspath(output_data_clumps_file)
    abs_detector_options_file = os.path.abspath(detector_options_file)

    print(f"Loading detector options from {abs_detector_options_file}")
    detector_options = DetectorOptions.load_config_from_file(abs_detector_options_file)
    print(f"Loaded detector options")


    software_project_dicts = SoftwareProjectDicts(abs_ast_output_folder)


    # Initialize dataClumpsTypeContext dictionary
    data_clumps_type_context = {
        "report_version": "0.1.93",
        "report_timestamp": datetime.now().isoformat(),
        "target_language": "unknown",  # Replace with actual value
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
            "options": json.dumps(detector_options.options)
        },
        "data_clumps": {}
    }

    print("Detecting software project for data clumps")

    # Assuming DetectorDataClumpsMethods and DetectorDataClumpsFields are Python classes you've defined
    detector_data_clumps_methods = DetectorDataClumpsMethods(detector_options, None, None)
    common_method_parameters = await detector_data_clumps_methods.detect(abs_ast_output_folder)

    if common_method_parameters:
        for key, value in common_method_parameters.items():
            data_clumps_type_context['data_clumps'][value['key']] = value

    detector_data_clumps_fields = DetectorDataClumpsFields(detector_options, None, None)
    common_fields = await detector_data_clumps_fields.detect(abs_ast_output_folder)

    if common_fields:
        for key, value in common_fields.items():
            data_clumps_type_context['data_clumps'][value['key']] = value

    data_clumps_type_context['report_summary'] = {
        'amount_data_clumps': len(data_clumps_type_context['data_clumps'])
    }

    print("Detecting software project for data clumps (done)")

    # Save the result to abs_output_data_clumps_file
    with open(abs_output_data_clumps_file, 'w') as f:
        json.dump(data_clumps_type_context, f, indent=4)
