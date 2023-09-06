import json
import os

class SoftwareProjectDicts:
    def __init__(self, folder_path):
        self.dictClassOrInterface = {}
        self.dictMemberFieldParameters = {}
        self.dictMethod = {}
        self.dictMethodParameters = {}

        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                with open(os.path.join(folder_path, filename), 'r') as f:
                    dictClassOrInterface = json.load(f)
                    self.handleClassOrInterface(ClassOrInterfaceTypeContext.from_dict(dictClassOrInterface))

    def fillMethodsForClassOrInterface(self, classOrInterface):
        methodsDictForClassOrInterface = classOrInterface.get('methods', {})
        for methodKey, method in methodsDictForClassOrInterface.items():
            self.dictMethod[methodKey] = method
            methodParametersDictForMethod = method.get('parameters', {})
            for methodParameterKey, methodParameter in methodParametersDictForMethod.items():
                self.dictMethodParameters[methodParameterKey] = methodParameter

    def fillMemberFieldsForClassOrInterface(self, classOrInterface):
        memberFieldParametersDictForClassOrInterface = classOrInterface.get('fields', {})
        for memberFieldParameterKey, memberFieldParameter in memberFieldParametersDictForClassOrInterface.items():
            self.dictMemberFieldParameters[memberFieldParameterKey] = memberFieldParameter

    def handleClassOrInterface(self, classOrInterface):
        self.fillClassOrInterfaceDicts(classOrInterface)
        self.fillMemberFieldsForClassOrInterface(classOrInterface)
        self.fillMethodsForClassOrInterface(classOrInterface)

    def fillClassOrInterfaceDicts(self, classOrInterface):
        self.dictClassOrInterface[classOrInterface['key']] = classOrInterface
        innerDefinedClassesDict = classOrInterface.get('innerDefinedClasses', {})
        for innerDefinedClassKey, innerDefinedClass in innerDefinedClassesDict.items():
            self.handleClassOrInterface(innerDefinedClass)
        innerDefinedInterfacesDict = classOrInterface.get('innerDefinedInterfaces', {})
        for innerDefinedInterfaceKey, innerDefinedInterface in innerDefinedInterfacesDict.items():
            self.handleClassOrInterface(innerDefinedInterface)
