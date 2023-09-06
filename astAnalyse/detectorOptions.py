import json
import os

# Define default options and their metadata
# Define default options and their metadata
DetectorOptionsInformation = {
    "sharedFieldParametersMinimum": {
        "label": "Minimum Number of Shared Fields",
        "description": "The minimum number of fields that two or more classes must share to be considered related. Default value is 3.",
        "defaultValue": 3,
        "group": "field",
        "type": "number"
    },
    "sharedFieldParametersCheckIfAreSubtypes": {
        "label": "Check Subtyping of Shared Fields",
        "description": "If set to true, the detector will check if shared fields in related classes are subtypes of each other. Default value is false.",
        "defaultValue": False,
        "group": "field",
        "type": "boolean"
    },
    "subclassInheritsAllMembersFromSuperclass": {
        "label": "Subclass Inherits All Members",
        "description": "If set to true, the detector will consider a subclass related to its superclass only if it inherits all members fields from it. Default value is false.",
        "defaultValue": False,
        "group": "field",
        "type": "boolean"
    },
    "sharedMethodParametersMinimum": {
        "label": "Minimum Number of Shared Method Parameters",
        "description": "The minimum number of method parameters that two or more classes must share to be considered related. Default value is 3.",
        "defaultValue": 3,
        "group": "method",
        "type": "number"
    },
    "sharedMethodParametersHierarchyConsidered": {
        "label": "Consider Hierarchy for Shared Method Parameters",
        "description": "If set to true, the detector will consider the hierarchy of classes when checking for shared method parameters. Default value is false.",
        "defaultValue": False,
        "group": "method",
        "type": "boolean"
    },
    "analyseMethodsWithUnknownHierarchy": {
        "label": "Analyze Methods with Unknown Hierarchy",
        "description": "If set to true, the detector will analyze methods that are not part of a known hierarchy of related classes. Default value is false.",
        "defaultValue": False,
        "group": "method",
        "type": "boolean"
    }
}

def getDefaultValuesFromPartialOptions(partial_options):
    result = {}
    for key, parameter in DetectorOptionsInformation.items():
        if key in partial_options:
            result[key] = partial_options[key]
        else:
            result[key] = parameter["defaultValue"]
    return result

class DetectorOptions:
    def __init__(self, partial_options=None):
        self.options = getDefaultValuesFromPartialOptions(partial_options or {})
        # ... (other initializations)

    def save_config_to_file(self, filepath):
            absolute_filepath = os.path.abspath(filepath)
            with open(absolute_filepath, 'w') as f:
                json.dump(self.options, f, indent=4)

    @classmethod
    def load_config_from_file(cls, filepath):
        absolute_filepath = os.path.abspath(filepath)
        with open(absolute_filepath, 'r') as f:
            options = json.load(f)
        return cls(options)

def generateDetectorOptionsFile(detector_options_file):
    detector_options = DetectorOptions()
    detector_options.save_config_to_file(detector_options_file)
