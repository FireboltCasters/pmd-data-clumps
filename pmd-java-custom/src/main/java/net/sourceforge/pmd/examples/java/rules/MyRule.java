package net.sourceforge.pmd.examples.java.rules;

import com.fasterxml.jackson.databind.SerializationFeature;
import net.sourceforge.pmd.RuleContext;
import net.sourceforge.pmd.examples.java.rules.parsedAstTypes.*;
import net.sourceforge.pmd.lang.java.ast.*;
import net.sourceforge.pmd.lang.java.rule.AbstractJavaRule;
import net.sourceforge.pmd.properties.StringProperty;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import com.fasterxml.jackson.databind.ObjectMapper;

public class MyRule extends AbstractJavaRule {

    static int count = 0;
    static String output = "";

    public static String convertToJson(Object obj) {
        ObjectMapper mapper = new ObjectMapper();
        mapper.enable(SerializationFeature.INDENT_OUTPUT); // Enable pretty printing
        try {
            return mapper.writeValueAsString(obj);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    private static final StringProperty BAD_NAME = StringProperty.named("badName")
            .defaultValue("foo")
            .desc("The variable name that should not be used.")
            .uiOrder(1.0f)
            .build();

    public MyRule() {
        definePropertyDescriptor(BAD_NAME);
    }

    @Override
    public void start(RuleContext ctx) {
        // Override as needed
        //System.out.println("Start");
        //System.out.println("================");
    }

    @Override
    public void end(RuleContext ctx) {
        // Override as needed
        //System.out.println("================");
        //System.out.println("Finished");
    }

    /**
     * Gets called before we get into the class declaration
    public Object visit(ASTFieldDeclaration node, Object data){
        System.out.println("ASTFieldDeclaration");

        return super.visit(node, data);
    }
     */

    private void extractFields(ASTClassOrInterfaceDeclaration node, ClassOrInterfaceTypeContext classContext){
        List<ASTFieldDeclaration> fields = node.descendants(ASTFieldDeclaration.class).toList();

        for (ASTFieldDeclaration field : fields) {


            MemberFieldParameterTypeContext fieldContext = new MemberFieldParameterTypeContext();
            // Set the properties of the fieldContext based on the field
            fieldContext.name = field.getVariableName();
            fieldContext.key = field.getVariableName();
            fieldContext.type = field.getTypeNode().getTypeMirror().toString();
            // Set the position
            AstPosition position = new AstPosition();
            position.startLine = field.getBeginLine();
            position.startColumn = field.getBeginColumn();
            position.endLine = field.getEndLine();
            position.endColumn = field.getEndColumn();
            fieldContext.position = position;

            fieldContext.classOrInterfaceKey = node.getCanonicalName();

            // Extract the modifiers
            ASTModifierList fieldModifiers = field.getFirstDescendantOfType(ASTModifierList.class);
            Set<JModifier> modifierSet = fieldModifiers.getEffectiveModifiers();
            if (modifierSet != null) {
                fieldContext.modifiers = modifierSet.stream().map(Enum::name).collect(Collectors.toList());
            }

            // Add the fieldContext to the classContext.fields
            classContext.fields.put(fieldContext.name, fieldContext);
        }
    }

    private void extractMethods(ASTClassOrInterfaceDeclaration node, ClassOrInterfaceTypeContext classContext){

        // If you want to only get the fields of the top-level class and not any inner classes, you would need to add a check to exclude fields that belong to inner classes. One way to do this could be to check the parent of each field and see if it's the top-level class node.
        List<ASTMethodDeclaration> methods = node.descendants(ASTMethodDeclaration.class).toList();
        for (ASTMethodDeclaration method : methods) {

            MethodTypeContext methodContext = new MethodTypeContext();
            // Set the properties of the methodContext based on the method
            methodContext.name = method.getMethodName();
            methodContext.key = method.getMethodName(); // or other unique key
            methodContext.type = method.getResultTypeNode().getTypeMirror().toString();

            // Set the position
            AstPosition position = new AstPosition();
            position.startLine = method.getBeginLine();
            position.startColumn = method.getBeginColumn();
            position.endLine = method.getEndLine();
            position.endColumn = method.getEndColumn();
            methodContext.position = position;

            methodContext.classOrInterfaceKey = node.getCanonicalName();

            // Extract the modifiers and check for @Override annotation
            ASTModifierList methodModifiers = method.getFirstDescendantOfType(ASTModifierList.class);
            Set<JModifier> methodModifierSet = methodModifiers.getEffectiveModifiers();
            if (methodModifierSet != null) {
                methodContext.modifiers = methodModifierSet.stream().map(Enum::name).collect(Collectors.toList());
            }

            methodContext.overrideAnnotation = method.isOverridden();


            // Extract the parameters
            List<ASTFormalParameter> parameters = method.findChildrenOfType(ASTFormalParameter.class);
            for (ASTFormalParameter parameter : parameters) {

                MethodParameterTypeContext parameterContext = new MethodParameterTypeContext();
                // Set the properties of the parameterContext based on the parameter
                parameterContext.name = parameter.getImage();
                parameterContext.key = parameter.getImage(); // or other unique key
                parameterContext.type = parameter.getTypeMirror().toString();

                // Set the position
                AstPosition parameter_position = new AstPosition();
                parameter_position.startLine = parameter.getBeginLine();
                parameter_position.startColumn = parameter.getBeginColumn();
                parameter_position.endLine = parameter.getEndLine();
                parameter_position.endColumn = parameter.getEndColumn();
                parameterContext.position = parameter_position;

                // Extract the modifiers
                ASTModifierList parameterModifiers = parameter.getFirstDescendantOfType(ASTModifierList.class);
                Set<JModifier> parameterModifierSet = parameterModifiers.getEffectiveModifiers();
                if (parameterModifierSet != null) {
                    parameterContext.modifiers = parameterModifierSet.stream().map(Enum::name).collect(Collectors.toList());
                }

                // Add the parameterContext to the methodContext.parameters
                methodContext.parameters.add(parameterContext);
            }


            // Add the methodContext to the classContext.methods
            classContext.methods.put(methodContext.name, methodContext);
        }
    }

    private void extractClassInformations(ASTClassOrInterfaceDeclaration node, ClassOrInterfaceTypeContext classContext){

        // Set the properties of the classContext based on the node
        classContext.name = node.getSimpleName();
        classContext.key = node.getCanonicalName();
        classContext.type = node.isInterface() ? "interface" : "class";
        // Set the position
        AstPosition class_position = new AstPosition();
        class_position.startLine = node.getBeginLine();
        class_position.startColumn = node.getBeginColumn();
        class_position.endLine = node.getEndLine();
        class_position.endColumn = node.getEndColumn();
        classContext.position = class_position;

        classContext.anonymous = node.isAnonymous();

        // Extract the modifiers
        ASTModifierList classModifiers = node.getFirstDescendantOfType(ASTModifierList.class);
        Set<JModifier> classModifierSet = classModifiers.getEffectiveModifiers();
        if (classModifierSet != null) {
            classContext.modifiers = classModifierSet.stream().map(Enum::name).collect(Collectors.toList());
        }
    }

    private ClassOrInterfaceTypeContext visitClassOrInterface(ASTClassOrInterfaceDeclaration node){
        System.out.println("ASTClassOrInterfaceDeclaration");

        // Create a new instance of your ClassOrInterfaceTypeContext class
        ClassOrInterfaceTypeContext classContext = new ClassOrInterfaceTypeContext();
        this.extractClassInformations(node, classContext);

        // Extract the fields
        //this.extractFields(node, classContext);

        // Extract the methods
        //this.extractMethods(node, classContext);


// Extract the interfaces this class implements
        List<ASTImplementsList> implementsLists = node.findDescendantsOfType(ASTImplementsList.class);
        for (ASTImplementsList implementsList : implementsLists) {
            List<ASTClassOrInterfaceType> interfaces = implementsList.findDescendantsOfType(ASTClassOrInterfaceType.class);
            for (ASTClassOrInterfaceType interfaceType : interfaces) {
                classContext.implements_.add(interfaceType.getSimpleName());
            }
        }

// Extract the classes this class extends
        List<ASTExtendsList> extendsLists = node.findDescendantsOfType(ASTExtendsList.class);
        for (ASTExtendsList extendsList : extendsLists) {
            List<ASTClassOrInterfaceType> superclasses = extendsList.findDescendantsOfType(ASTClassOrInterfaceType.class);
            for (ASTClassOrInterfaceType superclass : superclasses) {
                classContext.extends_.add(superclass.getSimpleName());
            }
        }


        // Set the definedInClassOrInterfaceTypeKey
        ASTClassOrInterfaceDeclaration parentClassOrInterface = node.getFirstParentOfType(ASTClassOrInterfaceDeclaration.class);
        if (parentClassOrInterface != null) {
            classContext.definedInClassOrInterfaceTypeKey = parentClassOrInterface.getCanonicalName();
        }


        // Write the outputRow to the file
        // ...

        return classContext;
    }

    public Object visit(ASTClassOrInterfaceDeclaration node, Object data) {
        ClassOrInterfaceTypeContext classContext = this.visitClassOrInterface(node);

        // Extract the inner classes and interfaces
        List<ASTClassOrInterfaceDeclaration> innerClassesAndInterfaces = node.findDescendantsOfType(ASTClassOrInterfaceDeclaration.class);
        for (ASTClassOrInterfaceDeclaration innerClassOrInterface : innerClassesAndInterfaces) {
            ClassOrInterfaceTypeContext innerClassOrInterfaceContext = this.visitClassOrInterface(innerClassOrInterface);
            // Set the properties of the innerClassOrInterfaceContext based on the innerClassOrInterface
            // Add the innerClassOrInterfaceContext to the appropriate map
            if (innerClassOrInterface.isInterface()) {
                classContext.innerDefinedInterfaces.put(innerClassOrInterface.getCanonicalName(), innerClassOrInterfaceContext);
            } else {
                classContext.innerDefinedClasses.put(innerClassOrInterface.getCanonicalName(), innerClassOrInterfaceContext);
            }
        }

        // Convert the classContext to JSON and add it to the output
        String outputRow = MyRule.convertToJson(classContext) + ",\n";

        System.out.println(outputRow);

        System.out.println("######################");

        //return super.visit(node, data);
        return null;
    }



}
