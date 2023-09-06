from typing import List, Dict, Tuple, Any

class ParameterPair:
    def __init__(self, parameter_key: str, other_parameter_key: str):
        self.parameter_key = parameter_key
        self.other_parameter_key = other_parameter_key

class DetectorUtils:

    @staticmethod
    def count_common_parameters(parameters: List[Any], other_parameters: List[Any]) -> int:
        common_parameter_keys = DetectorUtils.get_common_parameter_pair_keys(parameters, other_parameters)
        amount_common_parameters = len(common_parameter_keys)
        return amount_common_parameters

    @staticmethod
    def get_common_parameter_pair_keys(parameters: List[Any], other_parameters: List[Any]) -> List[ParameterPair]:
        common_parameter_pair_keys = []
        for parameter in parameters:
            for other_parameter in other_parameters:
                if DetectorUtils.is_similar_to(parameter, other_parameter):
                    common_parameter_pair_key = ParameterPair(parameter["key"], other_parameter["key"])
                    common_parameter_pair_keys.append(common_parameter_pair_key)
        return common_parameter_pair_keys

    @staticmethod
    def is_similar_to(this_parameter, other_parameter):
        # TODO: we need to check the similarity of the name
        # https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5328371 page 164
        # not only the data fields with the same
        # signatures (same name, same data type, same access
        # modifier), but also data fields with similar signatures (similar
        # name, same data type, same access modifier)

        same_modifiers = DetectorUtils.have_same_modifiers(this_parameter, other_parameter)  # Assuming have_same_modifiers is a function you have
        same_type = this_parameter['type'] == other_parameter['type']
        same_name = this_parameter['name'] == other_parameter['name']

        return same_modifiers and same_type and same_name

    @staticmethod
    def have_same_modifiers(this_parameter, other_parameter):
        same_modifiers = True
        both_have_modifiers = 'modifiers' in this_parameter and 'modifiers' in other_parameter

        if both_have_modifiers:
            # Assuming all_keys_in_array is a function you have
            we_have_all_modifiers_other_has = DetectorUtils.all_keys_in_array(this_parameter['modifiers'], other_parameter['modifiers'])
            other_has_all_modifiers_we_have = DetectorUtils.all_keys_in_array(other_parameter['modifiers'], this_parameter['modifiers'])

            same_modifiers = we_have_all_modifiers_other_has and other_has_all_modifiers_we_have
        else:
            both_have_no_modifiers = 'modifiers' not in this_parameter and 'modifiers' not in other_parameter

            if both_have_no_modifiers:
                same_modifiers = True
            else:
                same_modifiers = False

        return same_modifiers

    @staticmethod
    def all_keys_in_array(array1, array2):
        for key in array1:
            if key not in array2:
                return False
        return True

    @staticmethod
    def get_current_and_other_parameters_from_common_parameter_pair_keys(
            common_field_parameter_pair_keys: List[ParameterPair],
            current_class_parameters: List[Any],
            other_class_parameters: List[Any],
            software_project_dicts: Dict,
            other_class: Any,
            other_method: Any) -> Tuple[Dict, str]:

        current_parameters = {}
        common_field_parameter_keys_as_key = ""

        for common_field_parameter_pair_key in common_field_parameter_pair_keys:
            current_field_parameter_key = common_field_parameter_pair_key.parameter_key
            for current_class_parameter in current_class_parameters:
                if current_class_parameter["key"] == current_field_parameter_key:
                    common_field_parameter_keys_as_key += current_class_parameter["name"]
                    related_to_context = None

                    other_field_parameter_key = common_field_parameter_pair_key.other_parameter_key
                    for other_class_parameter in other_class_parameters:
                        if other_class_parameter["key"] == other_field_parameter_key:
                            related_to_parameter = {
                                'key': other_class_parameter["key"],
                                'name': other_class_parameter["name"],
                                'type': other_class_parameter["type"],
                                'modifiers': other_class_parameter["modifiers"],
                                'position': other_class_parameter["position"]
                            }
                            related_to_context = related_to_parameter

                    current_parameters[current_class_parameter["key"]] = {
                        'key': current_class_parameter["key"],
                        'name': current_class_parameter["name"],
                        'type': current_class_parameter["type"],
                        'modifiers': current_class_parameter["modifiers"],
                        'to_variable': related_to_context,
                        'position': current_class_parameter["position"]
                    }

        return current_parameters, common_field_parameter_keys_as_key

    @staticmethod
    def get_classes_or_interfaces_dict(project: Any) -> Dict:
        # Implement this method
        pass

    @staticmethod
    def get_classes_dict(software_project_dicts):
        classes_or_interfaces_dict = software_project_dicts.dictClassOrInterface
        classes_dict = {}
        class_or_interface_keys = list(classes_or_interfaces_dict.keys())
        for class_or_interface_key in class_or_interface_keys:
            class_or_interface = classes_or_interfaces_dict[class_or_interface_key]
            type_ = class_or_interface['type']  # ClassOrInterfaceTypeContext type is either "class" or "interface"
            if type_ == "class":  # DataclumpsInspection.java line 407
                classes_dict[class_or_interface_key] = class_or_interface
        return classes_dict


    @staticmethod
    def get_classes_or_interfaces_from_file(file: Any) -> List[Any]:
        # Implement this method
        pass
