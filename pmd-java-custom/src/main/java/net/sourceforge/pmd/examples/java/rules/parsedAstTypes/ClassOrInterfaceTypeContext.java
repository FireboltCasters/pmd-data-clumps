package net.sourceforge.pmd.examples.java.rules.parsedAstTypes;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ClassOrInterfaceTypeContext extends AstElementTypeContext {
    public List<String> modifiers = new ArrayList<String>();
    public Map<String, MemberFieldParameterTypeContext> fields = new HashMap<String, MemberFieldParameterTypeContext>();
    public Map<String, MethodTypeContext> methods = new HashMap<String, MethodTypeContext>();
    public String fileKey;
    public boolean anonymous;
    public List<String> implements_ = new ArrayList<String>();
    public List<String> extends_ = new ArrayList<String>();

    public String definedInClassOrInterfaceTypeKey;

    public Map<String, ClassOrInterfaceTypeContext> innerDefinedClasses = new HashMap<String, ClassOrInterfaceTypeContext>();
    public Map<String, ClassOrInterfaceTypeContext> innerDefinedInterfaces = new HashMap<String, ClassOrInterfaceTypeContext>();

    public ClassOrInterfaceTypeContext(){

    }
}