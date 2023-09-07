from typing import Optional, Dict, Any, Union
import json

from .detectorUtils import DetectorUtils

class DetectorDataClumpsMethods:
    def __init__(self, options, myProgress):
        self.options = options
        self.myProgress = myProgress

    def addAmountOfTasksToProgress(self, software_project_dicts):
        methods_dict = software_project_dicts.dictMethod
        method_keys = list(methods_dict.keys())
        amount_methods = len(method_keys)
        self.myProgress.addAmountOfTasks(amount_methods)

    async def detect(self, software_project_dicts):
        # print("Detecting software project for data clumps in methods")
        methods_dict = software_project_dicts.dictMethod
        method_keys = list(methods_dict.keys())
        data_clumps_method_parameter_data_clumps = {}

        for method_key in method_keys:
            method = methods_dict[method_key]
            self.myProgress.increaseCounter(1)
            self.myProgress.printProgress(f"DetectorDataClumpsMethods: {method['key']}")


            self.analyze_method(method, software_project_dicts, data_clumps_method_parameter_data_clumps)

        return data_clumps_method_parameter_data_clumps

    def get_parameters_from_method(self, method):
        method_parameters = []

        variableTypesConsidered = self.options['typeVariablesConsidered']

        #print(json.dumps(method, indent=4, sort_keys=True))
        list_method_parameters = method["parameters"]
        # print len
        #print(f"len(method_parameters): {len(list_method_parameters)}")
        for method_parameter in list_method_parameters:
            # print json dump
            if method_parameter['hasTypeVariable'] and not variableTypesConsidered:
                continue # skip type variables like List<T> but not List<String>

            if not method_parameter['ignore']:
                method_parameters.append(method_parameter)

        return method_parameters


    def analyze_method(self, method, software_project_dicts, data_clumps_method_parameter_data_clumps):
        current_class_or_interface = DetectorUtils.method_get_class_or_interface(method, software_project_dicts)

        if current_class_or_interface["auxclass"]:  # ignore auxclasses as they are not important for our project
            return

        # print(f"Analyze method: {method.key}")
        method_parameters = self.get_parameters_from_method(method)
        amount_of_method_parameters = len(method_parameters)

        if amount_of_method_parameters < self.options["sharedMethodParametersMinimum"]:
            # print(f"Method {method.key} has less than {self.options.shared_method_parameters_minimum} parameters. Skipping this method.")
            return

        if not self.options["analyseMethodsWithUnknownHierarchy"]:
            # print("- check if methods hierarchy is complete")
            whole_hierarchy_known = DetectorUtils.method_is_whole_hierarchy_known(method, software_project_dicts)
            if not whole_hierarchy_known:  # since we don't know the complete hierarchy, we can't detect if a method is inherited or not
                # print("-- check if methods hierarchy is complete")
                return  # therefore we stop here

        this_method_is_inherited = DetectorUtils.method_is_inherited_from_parent_class_or_interface(method, software_project_dicts)
        if this_method_is_inherited:  # if the method is inherited
            # then skip this method
            return

        # we assume that all methods are not constructors
        self.check_parameter_data_clumps(method, software_project_dicts, data_clumps_method_parameter_data_clumps)


    def check_parameter_data_clumps(self, method, software_project_dicts, data_clumps_method_parameter_data_clumps):
        # print(f"Checking parameter data clumps for method {method.key}")

        classes_or_interfaces_dict = software_project_dicts.dictClassOrInterface
        other_classes_or_interfaces_keys = list(classes_or_interfaces_dict.keys())

        for class_or_interface_key in other_classes_or_interfaces_keys:
            other_class_or_interface = classes_or_interfaces_dict[class_or_interface_key]

            if other_class_or_interface['auxclass']:  # ignore auxclasses as they are not important for our project
                return

            other_methods = other_class_or_interface['methods']
            other_methods_keys = list(other_methods.keys())

            for other_method_key in other_methods_keys:
                other_method = other_methods[other_method_key]

                found_data_clumps = self.check_method_parameters_for_data_clumps(
                    method, other_method, software_project_dicts, data_clumps_method_parameter_data_clumps
                )
                # TODO: DataclumpsInspection.java line 512

    def check_method_parameters_for_data_clumps(self, method, other_method, software_project_dicts, data_clumps_method_parameter_data_clumps):
        is_same_method = method['key'] == other_method['key']
        if is_same_method:
            return

        current_class_or_interface_key = method['classOrInterfaceKey']
        current_class_or_interface = software_project_dicts.dictClassOrInterface[current_class_or_interface_key]
        other_class_or_interface_key = other_method['classOrInterfaceKey']
        other_class_or_interface = software_project_dicts.dictClassOrInterface[other_class_or_interface_key]

        other_method_parameters = self.get_parameters_from_method(other_method)
        other_method_parameters_amount = len(other_method_parameters)

        if other_method_parameters_amount < self.options['sharedMethodParametersMinimum']:
            return

        if not self.options['analyseMethodsWithUnknownHierarchy']:
            whole_hierarchy_known_of_other_method = DetectorUtils.method_is_whole_hierarchy_known(other_method, software_project_dicts)
            if not whole_hierarchy_known_of_other_method:
                return

        is_different_class_or_interface = other_class_or_interface['key'] != current_class_or_interface['key']
        if is_different_class_or_interface:
            if DetectorUtils.method_has_same_signature_as(method, other_method):
                other_method_is_inherited = DetectorUtils.method_is_inherited_from_parent_class_or_interface(other_method, software_project_dicts)
                if other_method_is_inherited:
                    return

        amount_common_parameters = self.count_common_parameters_between_methods(method, other_method)
        if amount_common_parameters < self.options['sharedMethodParametersMinimum']:
            return
        else:
            common_method_parameter_pair_keys = DetectorUtils.get_common_parameter_pair_keys(
                method['parameters'], other_method['parameters']
            )

            other_class_or_interface = software_project_dicts.dictClassOrInterface[other_method['classOrInterfaceKey']]

            current_parameters, common_field_parameter_keys_as_key = DetectorUtils.get_current_and_other_parameters_from_common_parameter_pair_keys(
                common_method_parameter_pair_keys, method['parameters'], other_method['parameters'],
                software_project_dicts, other_class_or_interface, other_method
            )

            current_class_or_interface = software_project_dicts.dictClassOrInterface[method['classOrInterfaceKey']]

            file_key = current_class_or_interface['file_path']

            data_clump_context = {
                'type': 'data_clump',
                'key': f"{file_key}-{current_class_or_interface['key']}-{other_class_or_interface['key']}-{common_field_parameter_keys_as_key}",
                'from_file_path': file_key,
                'from_class_or_interface_name': current_class_or_interface['name'],
                'from_class_or_interface_key': current_class_or_interface['key'],
                'from_method_name': method['name'],
                'from_method_key': method['key'],
                'to_file_path': other_class_or_interface['file_path'],
                'to_class_or_interface_name': other_class_or_interface['name'],
                'to_class_or_interface_key': other_class_or_interface['key'],
                'to_method_name': other_method['name'],
                'to_method_key': other_method['key'],
                'data_clump_type': 'parameter_data_clump',
                'data_clump_data': current_parameters
            }

            data_clumps_method_parameter_data_clumps[data_clump_context['key']] = data_clump_context


    def count_common_parameters_between_methods(self, method, other_method):
        # print(f"Counting common parameters between method {method['key']} and method {other_method['key']}")
        parameters = method['parameters']
        other_parameters = other_method['parameters']
        amount_common_parameters = DetectorUtils.count_common_parameters(parameters, other_parameters)
        return amount_common_parameters

