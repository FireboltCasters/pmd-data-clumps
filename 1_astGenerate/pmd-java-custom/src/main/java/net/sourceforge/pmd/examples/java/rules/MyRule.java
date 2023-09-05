package net.sourceforge.pmd.examples.java.rules;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import com.fasterxml.jackson.databind.SerializationFeature;
import net.sourceforge.pmd.RuleContext;
import net.sourceforge.pmd.examples.java.rules.parsedAstTypes.*;
import net.sourceforge.pmd.lang.java.ast.*;
import net.sourceforge.pmd.lang.java.rule.AbstractJavaRule;
import net.sourceforge.pmd.lang.java.symbols.JClassSymbol;
import net.sourceforge.pmd.lang.java.symbols.JTypeDeclSymbol;
import net.sourceforge.pmd.lang.java.types.JClassType;
import net.sourceforge.pmd.lang.java.types.JTypeMirror;
import net.sourceforge.pmd.lang.java.types.TypePrettyPrint;
import net.sourceforge.pmd.properties.StringProperty;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
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

    private AstPosition getAstPosition(ASTFieldDeclaration node){
        AstPosition position = new AstPosition();
        position.startLine = node.getBeginLine();
        position.startColumn = node.getBeginColumn();
        position.endLine = node.getEndLine();
        position.endColumn = node.getEndColumn();
        return position;
    }

        private AstPosition getAstPosition(ASTVariableDeclaratorId node){
            AstPosition position = new AstPosition();
            position.startLine = node.getBeginLine();
            position.startColumn = node.getBeginColumn();
            position.endLine = node.getEndLine();
            position.endColumn = node.getEndColumn();
            return position;
        }

    private void extractFields(ASTClassOrInterfaceDeclaration node, ClassOrInterfaceTypeContext classContext){
        List<ASTFieldDeclaration> fields = node.descendants(ASTFieldDeclaration.class).toList();

        String memberFieldKeyPre = getClassOrInterfaceKey(node)+"/memberField/";

        // search for rows like: private ArrayList javaArrayList, anotherArrayList[];
        for (ASTFieldDeclaration field : fields) {
            //String memberFieldKey = "";

            // now get from a row like: private ArrayList javaArrayList, anotherArrayList[];
            // the individual : javaArrayList and anotherArrayList[]
            List<ASTVariableDeclaratorId> fieldVariableDeclarators = field.descendants(ASTVariableDeclaratorId.class).toList();
            for(ASTVariableDeclaratorId fieldVariableDeclarator: fieldVariableDeclarators){
                String memberFieldKey = "";
                MemberFieldParameterTypeContext fieldContext = new MemberFieldParameterTypeContext();
                // Set the properties of the fieldContext based on the field
                fieldContext.name = fieldVariableDeclarator.getName();
                fieldContext.key = fieldVariableDeclarator.getName();

                // TODO: what is is varargs?
                fieldContext.type = this.getQualifiedNameUnsafe(fieldVariableDeclarator.getTypeMirror());

                // Set the position
                fieldContext.position = this.getAstPosition(fieldVariableDeclarator);

                fieldContext.classOrInterfaceKey = node.getCanonicalName();

                // Extract the modifiers
                ASTModifierList fieldModifiers = field.getFirstDescendantOfType(ASTModifierList.class);
                Set<JModifier> modifierSet = fieldModifiers.getEffectiveModifiers();
                if (modifierSet != null) {
                    fieldContext.modifiers = modifierSet.stream().map(Enum::name).collect(Collectors.toList());
                }

                // Add the fieldContext to the classContext.fields
                classContext.fields.put(fieldContext.name, fieldContext);
                memberFieldKey = memberFieldKeyPre+fieldContext.key;

                fieldContext.memberFieldKey = memberFieldKey;
            }
            /**
            // remove the last comma
            if(memberFieldKey.length()>0){
                memberFieldKey = memberFieldKey.substring(0, memberFieldKey.length()-1);
            }
            System.out.println("memberFieldKey: "+memberFieldKey);
            */
        }
    }

    private void extractMethods(ASTClassOrInterfaceDeclaration node, ClassOrInterfaceTypeContext classContext){

        String classOrInterfaceKey = getClassOrInterfaceKey(node);

        // If you want to only get the fields of the top-level class and not any inner classes, you would need to add a check to exclude fields that belong to inner classes. One way to do this could be to check the parent of each field and see if it's the top-level class node.
        List<ASTMethodDeclaration> methods = node.descendants(ASTMethodDeclaration.class).toList();
        for (ASTMethodDeclaration method : methods) {

            MethodTypeContext methodContext = new MethodTypeContext();
            // Set the properties of the methodContext based on the method
            methodContext.name = method.getMethodName();
            methodContext.key = classOrInterfaceKey+"/method/"+method.getMethodName(); // or other unique key
            methodContext.type = this.getQualifiedNameUnsafe(method.getResultTypeNode().getTypeMirror());

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
            ASTFormalParameters parameters = method.getFormalParameters();
            for (ASTFormalParameter parameter : parameters) {

                ASTVariableDeclaratorId parameterVariableDeclarator = parameter.getVarId();

                MethodParameterTypeContext parameterContext = new MethodParameterTypeContext();
                // Set the properties of the parameterContext based on the parameter
                // now get from a row like: private ArrayList javaArrayList, anotherArrayList[];
                // the individual : javaArrayList and anotherArrayList[]
                String memberFieldKey = "";
                // Set the properties of the fieldContext based on the field
                parameterContext.name = parameterVariableDeclarator.getName();
                parameterContext.key = parameterVariableDeclarator.getName();

                // TODO: what is is varargs?
                parameterContext.type = this.getQualifiedNameUnsafe(parameterVariableDeclarator.getTypeMirror());
                /**
                if (parameter.isVarargs()) {  // Hypothetical method; check PMD documentation
                    System.out.println("This is a varargs parameter: " + parameter.getImage());
                } else if (parameter.isArray()) {  // Hypothetical method; check PMD documentation
                    System.out.println("This is an array parameter: " + parameter.getImage());
                } else {
                    System.out.println("This is a regular parameter: " + parameter.getImage());
                }
                */


                // Set the position
                parameterContext.position = this.getAstPosition(parameterVariableDeclarator);

                // Extract the modifiers
                ASTModifierList fieldModifiers = parameter.getFirstDescendantOfType(ASTModifierList.class);
                Set<JModifier> modifierSet = fieldModifiers.getEffectiveModifiers();
                if (modifierSet != null) {
                    parameterContext.modifiers = modifierSet.stream().map(Enum::name).collect(Collectors.toList());
                }

                parameterContext.methodKey = methodContext.key;

                // Add the parameterContext to the methodContext.parameters
                methodContext.parameters.add(parameterContext);
            }


            // Add the methodContext to the classContext.methods
            classContext.methods.put(methodContext.name, methodContext);
        }
    }

    private String getClassOrInterfaceKey(ASTClassOrInterfaceDeclaration node){
        String classOrInterfaceKey = node.getCanonicalName();
        if(classOrInterfaceKey==null){
            classOrInterfaceKey = node.getSimpleName();
        }
        return classOrInterfaceKey;
    }

    private void extractClassInformations(ASTClassOrInterfaceDeclaration node, ClassOrInterfaceTypeContext classContext){

        // Set the properties of the classContext based on the node
        classContext.name = node.getSimpleName();
        classContext.key = getClassOrInterfaceKey(node);
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

    private String getQualifiedNameUnsafe(JTypeMirror typeMirror){
        JTypeDeclSymbol symbol = typeMirror.getSymbol();

        StringBuilder genericQualifiedNames = new StringBuilder();
        if(typeMirror instanceof JClassType){
            JClassType downCast = (JClassType) typeMirror;
            List<JTypeMirror> typeMirrors = downCast.getTypeArgs();
            boolean isGeneric = downCast.isGeneric();

            if(isGeneric){
                genericQualifiedNames.append("<");
                for(int i = 0; i < typeMirrors.size(); i++){
                    JTypeMirror innerTypeMirror = typeMirrors.get(i);
                    String innerTypeArgFullQualifiedName = this.getQualifiedNameUnsafe(innerTypeMirror);
                    genericQualifiedNames.append(innerTypeArgFullQualifiedName);
                    // Add a comma after each name, except the last one
                    if (i < typeMirrors.size() - 1) {
                        genericQualifiedNames.append(", ");
                    }
                }
                genericQualifiedNames.append(">");
            }
        }

        // Continue with your code
        if (symbol instanceof JClassSymbol) {
            JClassSymbol jClassSymbol = (JClassSymbol) symbol;
            String fullQualifiedName =jClassSymbol.getCanonicalName();

            // TODO check if * is found
            // Then count the amount of dots
            // *CodePiece --> no dots --> replace * by packagename
            // *CodePiece.InnerClass --> ?

            // org.flywaydb.core.Flyway#InnerClass --> we should replace the # to a dot
            fullQualifiedName = fullQualifiedName.replaceAll("#",".");

            // TODO
            // *org.flywaydb.core.api.configuration.FluentConfiguration --> technically we only need to remove the *

            String fullQualifiedNameWithGenerics = fullQualifiedName + genericQualifiedNames;
            String prettyString = TypePrettyPrint.prettyPrint(typeMirror);
//            System.out.println("-- prettyString: "+prettyString);
//            System.out.println("--> fullQualifiedNameWithGenerics: "+fullQualifiedNameWithGenerics);
            return fullQualifiedName;
        }
        return null;
    }

    private void extractExtendsAndImplements(ASTClassOrInterfaceDeclaration node, ClassOrInterfaceTypeContext classContext){

        // Extract the interfaces this class implements
        List<ASTImplementsList> implementsLists = node.findDescendantsOfType(ASTImplementsList.class);
        for (ASTImplementsList implementsList : implementsLists) {
            List<ASTClassOrInterfaceType> interfaces = implementsList.findDescendantsOfType(ASTClassOrInterfaceType.class);
            for (ASTClassOrInterfaceType interfaceType : interfaces) {
                String fullQualifiedName = this.getQualifiedNameUnsafe(interfaceType.getTypeMirror());
                if(fullQualifiedName != null){
                    classContext.implements_.add(fullQualifiedName);
                }
            }
        }

        // Extract the classes this class extends
        List<ASTExtendsList> extendsLists = node.findDescendantsOfType(ASTExtendsList.class);
        for (ASTExtendsList extendsList : extendsLists) {
            List<ASTClassOrInterfaceType> superclasses = extendsList.findDescendantsOfType(ASTClassOrInterfaceType.class);
            for (ASTClassOrInterfaceType superclass : superclasses) {
                String fullQualifiedName = this.getQualifiedNameUnsafe(superclass.getTypeMirror());
                if(fullQualifiedName != null){
                    classContext.extends_.add(fullQualifiedName);
                }
            }
        }
    }

    private ClassOrInterfaceTypeContext visitClassOrInterface(ASTClassOrInterfaceDeclaration node){
        //System.out.println("ASTClassOrInterfaceDeclaration");

        // Create a new instance of your ClassOrInterfaceTypeContext class
        ClassOrInterfaceTypeContext classContext = new ClassOrInterfaceTypeContext();
        this.extractClassInformations(node, classContext);

        // Extract the fields
        this.extractFields(node, classContext);

        // Extract the methods
        this.extractMethods(node, classContext);

        // Extract the interfaces this class implements
        // Extract the classes this class extends
        this.extractExtendsAndImplements(node, classContext);

        // Set the definedInClassOrInterfaceTypeKey
        ASTClassOrInterfaceDeclaration parentClassOrInterface = node.getFirstParentOfType(ASTClassOrInterfaceDeclaration.class);
        if (parentClassOrInterface != null) {
            classContext.definedInClassOrInterfaceTypeKey = parentClassOrInterface.getCanonicalName();
        }

        // recursive call for inner classes
        this.visitInnerClassesOrInterfaces(node, classContext);

        return classContext;
    }

    private void visitInnerClassesOrInterfaces(ASTClassOrInterfaceDeclaration node, ClassOrInterfaceTypeContext classContext){
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
    }

    public Object visit(ASTClassOrInterfaceDeclaration node, Object data) {
        //System.out.println(node.getCanonicalName());

        ClassOrInterfaceTypeContext classContext = this.visitClassOrInterface(node);

        //String outputFolder = System.getenv("DEBUG"); check if print debug or so
        boolean debug = false;

        // Convert the classContext to JSON and add it to the output
        String outputRow = MyRule.convertToJson(classContext) + ",\n";
        String fileName = classContext.key+".json";

        if(debug){
            System.out.println("fileName: "+fileName);
            System.out.println(outputRow);
            System.out.println("######################");
        } else {
            // Access the OUTPUT_FOLDER environment variable
            String outputFolder = System.getenv("OUTPUT_FOLDER");
            if (outputFolder == null) {
                outputFolder = "./output";  // Default to current directory if not set
            }

//            String fileName = classContext.key;

            // Create a File object
            File file = new File(outputFolder, fileName);

            // Create output folder if it doesn't exist
            new File(outputFolder).mkdirs();

            // Write the outputRow to a file
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(file, true))) {
                writer.write(outputRow);
            } catch (IOException e) {
                e.printStackTrace();
            }

            // Print the absolute path of the file
            System.out.println("AST Generated for: " + file.getAbsolutePath());
        }

        //return super.visit(node, data);
        return null;
    }



}
