package net.sourceforge.pmd.examples.java.rules;

import net.sourceforge.pmd.RuleContext;
import net.sourceforge.pmd.lang.ast.Node;
import net.sourceforge.pmd.lang.ast.NodeStream;
import net.sourceforge.pmd.lang.java.ast.*;
import net.sourceforge.pmd.lang.java.rule.AbstractJavaRule;
import net.sourceforge.pmd.properties.StringProperty;
import org.checkerframework.checker.nullness.qual.NonNull;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;

public class MyRule extends AbstractJavaRule {

    static int count = 0;
    static String output = "";

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

    public Object visit(ASTClassOrInterfaceDeclaration node, Object data) {
        String className = node.getCanonicalName();
        String simpleName = node.getSimpleName();
        String outputRow = "\t\""+className+"\": \""+simpleName+"\",\n";
        System.out.println(outputRow);

        //TODO Add this row to the output file saved on the desktop

        try {
            // Create file
            String desktopPath = System.getProperty("user.home") + "/Desktop/";
            File outputFile = new File(desktopPath + "pmd-data-clumps-classAndInterfaces.csv");

            // If file does not exist, create it
            if (!outputFile.exists()) {
                outputFile.createNewFile();
            }

            // Create FileWriter and BufferedWriter (in append mode)
            FileWriter fileWriter = new FileWriter(outputFile, true);
            BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);

            // Write the outputRow to the file
            bufferedWriter.write(outputRow);

            // Always close writers
            bufferedWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


//        System.out.println(count+" - "+className);
//        MyRule.count++;
        return super.visit(node, data);
    }
}
