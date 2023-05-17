package net.sourceforge.pmd.examples.java.rules;

import net.sourceforge.pmd.RuleContext;
import net.sourceforge.pmd.lang.ast.Node;
import net.sourceforge.pmd.lang.ast.NodeStream;
import net.sourceforge.pmd.lang.java.ast.*;
import net.sourceforge.pmd.lang.java.rule.AbstractJavaRule;
import net.sourceforge.pmd.properties.StringProperty;
import org.checkerframework.checker.nullness.qual.NonNull;

import java.util.Iterator;
import java.util.List;

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

    public Object visit(ASTClassOrInterfaceDeclaration node, Object data) {
        String className = node.getCanonicalName();
        System.out.println(count+" - "+className);
        ASTClassOrInterfaceType superClass = node.getSuperClassTypeNode();
        if(superClass!=null){
            System.out.println("extends: "+superClass.getSimpleName());
        }

        MyRule.count++;
        return null;
    }
}
