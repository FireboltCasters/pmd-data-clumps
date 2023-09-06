from typing import List, Dict, Tuple, Any, Union
import json

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


    @staticmethod
    def method_get_class_or_interface(method, software_project_dicts):
        # print json dumps
        current_class_or_interface_key = method["classOrInterfaceKey"]
        current_class_or_interface = software_project_dicts.dictClassOrInterface[current_class_or_interface_key]
        return current_class_or_interface

    @staticmethod
    def method_is_whole_hierarchy_known(method, software_project_dicts) -> bool:
        # TODO: check if we can find all parents
        # print("isWholeHierarchyKnown?")
        # print("softwareProjectDicts.dictClassOrInterface")
        # print(software_project_dicts.dict_class_or_interface)

        current_class_or_interface = DetectorUtils.method_get_class_or_interface(method, software_project_dicts)
        super_classes_or_interfaces_keys = DetectorUtils.get_super_classes_and_interfaces_keys(current_class_or_interface, software_project_dicts, True)
        # print(super_classes_or_interfaces_keys)

        for super_classes_or_interface_key in super_classes_or_interfaces_keys:
            #print(f"superClassesOrInterfaceKey: {super_classes_or_interface_key}")
            if super_classes_or_interface_key in software_project_dicts.dictClassOrInterface:
                super_classes_or_interface = software_project_dicts.dictClassOrInterface[super_classes_or_interface_key]
                if not super_classes_or_interface:
                    # print(f"Found no superClassesOrInterface for: {super_classes_or_interface_key}")
                    # print("The hierarchy is therefore not complete")
                    return False
            else:
                # print(f"Found no superClassesOrInterface for: {super_classes_or_interface_key}")
                # print("The hierarchy is therefore not complete")
                return False

        return True


    @staticmethod
    def get_super_classes_and_interfaces_keys(class_or_interface_instance, software_project_dicts: Dict[str, Any], recursive: bool) -> List[Any]:
        # print(f"getSuperClassesAndInterfacesKeys for: {class_or_interface_instance.key}")
        found_keys: Dict[str, Union[str, None]] = {}

        extending_classes_or_interfaces_keys: List[str] = []
        #print(json.dumps(class_or_interface_instance, indent=4, sort_keys=True))
        extending_keys = class_or_interface_instance["extends_"]
        for extending_key in extending_keys:
            extending_classes_or_interfaces_keys.append(extending_key)

        implements_keys = class_or_interface_instance["implements_"]
        for implements_key in implements_keys:
            extending_classes_or_interfaces_keys.append(implements_key)

        # print("implements and extends")
        # print(json.dumps(extending_classes_or_interfaces_keys))

        for extending_classes_or_interfaces_key in extending_classes_or_interfaces_keys:
            new_finding = extending_classes_or_interfaces_key not in found_keys
            if new_finding:
                found_keys[extending_classes_or_interfaces_key] = extending_classes_or_interfaces_key
                if recursive:
                    found_class_or_interface = software_project_dicts.dictClassOrInterface.get(extending_classes_or_interfaces_key)
                    if found_class_or_interface:
                        # print(f"--> Recursive call for: {found_class_or_interface.key}")
                        recursive_findings = DetectorUtils.get_super_classes_and_interfaces_keys(found_class_or_interface, software_project_dicts, recursive)
                        # print("<-- Recursive call ended")
                        for recursive_finding_key in recursive_findings:
                            new_recursive_finding = recursive_finding_key not in found_keys
                            if new_recursive_finding:
                                found_keys[recursive_finding_key] = recursive_finding_key

        super_classes_and_interfaces_keys = list(found_keys.keys())
        return super_classes_and_interfaces_keys



    @staticmethod
    def method_is_inherited_from_parent_class_or_interface(method: Any, software_project_dicts: Dict[str, Any]) -> bool:
        # In Java we can't rely on @Override annotation because it is not mandatory
        if method["overrideAnnotation"]:
            return True

        # Since the @Override is not mandatory, we need to dig down deeper by ourselves
        is_inherited = False
        current_class_or_interface = software_project_dicts.dictClassOrInterface[method["classOrInterfaceKey"]]

        if current_class_or_interface:
            # DONE: we should check if all superClassesAndInterfaces are found
            # We will check this in DetectorDataClumpsMethods.py with method: is_whole_hierarchy_not_known()

            super_classes_or_interfaces_keys = DetectorUtils.get_super_classes_and_interfaces_keys(current_class_or_interface, software_project_dicts, True)

            for super_class_or_interface_key in super_classes_or_interfaces_keys:
                # print(f"superClassOrInterfaceKey: {super_class_or_interface_key}")
                super_class_or_interface = software_project_dicts.dictClassOrInterface[super_class_or_interface_key]

                if super_class_or_interface:
                    super_class_or_interface_methods_dict = super_class_or_interface["methods"]
                    super_class_or_interface_methods_keys = list(super_class_or_interface_methods_dict.keys())

                    for super_class_or_interface_methods_key in super_class_or_interface_methods_keys:
                        # print(f"-- superClassOrInterfaceMethodsKey: {super_class_or_interface_methods_key}")
                        super_class_or_interface_method = super_class_or_interface_methods_dict[super_class_or_interface_methods_key]

                        if DetectorUtils.method_has_same_signature_as(method, super_class_or_interface_method):
                            is_inherited = True
                            return is_inherited
                #else:
                    # print(f"A superClassOrInterface could not be found: {super_class_or_interface_key}")
                    # print("It might be, that this is a library import")

        # print("++++++++++++++")
        return is_inherited

    @staticmethod
    def method_has_same_signature_as(method, other_method):
        has_same_signature = True

        if len(method["parameters"]) != len(other_method["parameters"]):
            has_same_signature = False
        else:
            this_method_signature = DetectorUtils.get_method_signature(method)
            other_method_signature = DetectorUtils.get_method_signature(other_method)
            if this_method_signature != other_method_signature:
                has_same_signature = False

        return has_same_signature

    @staticmethod
    def get_method_signature(method):
        #print(json.dumps(method, indent=4, sort_keys=True))
        method_signature = method["name"] + "("
        for i in range(len(method["parameters"])):
            parameter = method["parameters"][i]
            #print(f"parameter: {parameter}")
            #print(json.dumps(parameter, indent=4, sort_keys=True))
            method_signature += parameter["type"]
            if i < len(method["parameters"]) - 1:
                method_signature += ", "
        method_signature += ")"
        return method_signature

