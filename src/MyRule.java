import java.lang.reflect.Method;
import net.sourceforge.pmd.lang.java.ast.ASTVariableDeclaratorId;
import net.sourceforge.pmd.lang.java.rule.AbstractJavaRule;
import net.sourceforge.pmd.lang.symboltable.NameDeclaration;
import net.sourceforge.pmd.lang.java.ast.TypeNode;
import net.sourceforge.pmd.lang.symboltable.Scope;
import net.sourceforge.pmd.lang.java.ast.ASTClassOrInterfaceDeclaration;

public class MyRule extends AbstractJavaRule {

    static int counter = 0;

    @Override
    public Object visit(ASTClassOrInterfaceDeclaration node, Object data) {
	try{
        System.out.println(MyRule.counter+" name: " + node.getImage());
	MyRule.counter++;
        return super.visit(node, data);
	} catch (Error e){
	   return null;		
	}
    }

/**
    @Override
    public Object visit(ASTVariableDeclaratorId node, Object data) {
        System.out.println("Variable name: " + node.getImage());
	TypeNode typeNode = node.getTypeNode();
	System.out.println("Variable type: " + typeNode.toString());
	System.out.println("Variable type: " + typeNode.getType());


	System.out.println("");
        return super.visit(node, data);
    }
*/
}

