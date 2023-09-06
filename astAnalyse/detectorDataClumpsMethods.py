from .detectorOptions import DetectorOptions  # Assuming this is your DetectorOptions class
from typing import Dict, List, Optional, Any
import json

from .detectorUtils import DetectorUtils

class DetectorDataClumpsFields:
    def __init__(self, options):
        print("init DetectorDataClumpsFields")
        # Print the JSON-formatted string
        print(json.dumps(options, indent=4))
        self.options = options

    async def detect(self, software_project_dicts: Dict) -> Optional[Dict]:
        classes_dict = DetectorUtils.get_classes_dict(software_project_dicts)
        data_clumps_field_parameters = {}
        class_keys = list(classes_dict.keys())
        amount_of_classes = len(class_keys)
        index = 0

        for class_key in class_keys:
            current_class = classes_dict[class_key]

            if current_class.get('auxclass'):
                return None

            self.generate_member_field_parameters_related_to_for_class(current_class, classes_dict, data_clumps_field_parameters, software_project_dicts)

            index += 1

        return data_clumps_field_parameters

    def generate_member_field_parameters_related_to_for_class(self, current_class, classes_dict, data_clumps_field_parameters, software_project_dicts):
        member_field_parameters = self.get_member_parameters_from_class(current_class, software_project_dicts)
        amount_of_member_fields = len(member_field_parameters)
        if amount_of_member_fields < self.options['sharedFieldParametersMinimum']:
            return
        other_class_keys = list(classes_dict.keys())
        for other_class_key in other_class_keys:
            other_class = classes_dict[other_class_key]
            self.generate_member_field_parameters_related_to_for_class_to_other_class(current_class, other_class, data_clumps_field_parameters, software_project_dicts)


    def generate_member_field_parameters_related_to_for_class_to_other_class(self, current_class, other_class, data_clumps_field_parameters, software_project_dicts):
        if other_class['auxclass']:  # ignore auxclasses as they are not important for our project
            return

        current_class_key = current_class['key']
        other_class_key = other_class['key']
        if current_class_key == other_class_key:
            return  # skip the same class

        current_class_parameters = self.get_member_parameters_from_class(current_class, software_project_dicts)
        other_class_parameters = self.get_member_parameters_from_class(other_class, software_project_dicts)
        common_field_parameter_pair_keys = DetectorUtils.get_common_parameter_pair_keys(current_class_parameters, other_class_parameters)

        amount_of_common_field_parameters = len(common_field_parameter_pair_keys)
        if amount_of_common_field_parameters < self.options['sharedFieldParametersMinimum']:
            return

        current_parameters, common_field_parameter_keys_as_key = DetectorUtils.get_current_and_other_parameters_from_common_parameter_pair_keys(
            common_field_parameter_pair_keys, current_class_parameters, other_class_parameters, software_project_dicts, other_class, None)

        file_key = current_class['file_path']
        data_clump_context = {
            'type': 'data_clump',
            'key': f"{file_key}-{current_class_key}-{other_class_key}-{common_field_parameter_keys_as_key}",
            'from_file_path': file_key,
            'from_class_or_interface_name': current_class['name'],
            'from_class_or_interface_key': current_class_key,
            'from_method_name': None,
            'from_method_key': None,
            'to_file_path': other_class['file_path'],
            'to_class_or_interface_key': other_class_key,
            'to_class_or_interface_name': current_class['name'],
            'to_method_key': None,
            'to_method_name': None,
            'data_clump_type': 'field_data_clump',
            'data_clump_data': current_parameters
        }
        data_clumps_field_parameters[data_clump_context['key']] = data_clump_context


    def get_member_parameters_from_class(self, current_class, software_project_dicts):
        class_parameters = []

        field_parameters = current_class['fields']
        field_parameter_keys = list(field_parameters.keys())
        for field_key in field_parameter_keys:
            field_parameter = field_parameters[field_key]
            if not field_parameter['ignore']:
                class_parameters.append(field_parameter)

        if self.options['subclassInheritsAllMembersFromSuperclass']:
            superclasses_dict = current_class['extends']  # {'Batman': 'Batman.java/class/Batman'}
            superclass_names = list(superclasses_dict.keys())
            for superclassname in superclass_names:
                superclass_key = superclasses_dict[superclassname]
                superclass = software_project_dicts['dictClassOrInterface'][superclass_key]
                superclass_parameters = self.get_member_parameters_from_class(superclass, software_project_dicts)
                class_parameters.extend(superclass_parameters)

        return class_parameters

