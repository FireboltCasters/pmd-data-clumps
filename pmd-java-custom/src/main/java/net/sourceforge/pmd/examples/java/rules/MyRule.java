package net.sourceforge.pmd.examples.java.rules;

import net.sourceforge.pmd.lang.java.ast.*;
import net.sourceforge.pmd.lang.java.rule.AbstractJavaRule;
import net.sourceforge.pmd.properties.StringProperty;

public class MyRule extends AbstractJavaRule {

    static int count = 0;

    private static final StringProperty BAD_NAME = StringProperty.named("badName")
            .defaultValue("foo")
            .desc("The variable name that should not be used.")
            .uiOrder(1.0f)
            .build();

    public MyRule() {
        definePropertyDescriptor(BAD_NAME);
        addRuleChainVisit(ASTClassOrInterfaceDeclaration.class);
        addRuleChainVisit(ASTVariableDeclaratorId.class);
    }

    @Override
    public Object visit(ASTClassOrInterfaceDeclaration node, Object data) {
        String className = node.getQualifiedName().toString();
        System.out.println(count+" - "+className);
        MyRule.count++;
        return this.visit((JavaNode)node, data);
    }

    @Override
    public Object visit(ASTVariableDeclaratorId node, Object data) {
        //System.out.println("Hellop");
        String badName = getProperty(BAD_NAME);
        if (node.hasImageEqualTo(badName)) {
            addViolation(data, node, node.getImage());
        }
        return data;
    }
}
