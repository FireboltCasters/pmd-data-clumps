.PHONY: all build run clean

# Default value for the DIRECTORY variable
DIRECTORY := ./testSrc

all: clean build run

setup:
	./mvnw clean install

build:
	./mvnw clean install
	unzip -o ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT.zip -d ./pmd-java-dist/target/
	cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/pmd-java-custom-1.0.0-SNAPSHOT.jar ./pmd-bin-7.0.0-rc2/lib/
	cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/jackson-annotations-2.12.3.jar ./pmd-bin-7.0.0-rc2/lib/
		cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/jackson-core-2.12.3.jar ./pmd-bin-7.0.0-rc2/lib/
		cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/jackson-databind-2.12.3.jar ./pmd-bin-7.0.0-rc2/lib/

run:
#	./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/bin/pmd -d /Users/nbaumgartner/Desktop/javaAnalyzeProject -f text -R custom-java-ruleset.xml
	./pmd-bin-7.0.0-rc2/bin/pmd check -d $(DIRECTORY) -f text -R custom-java-ruleset.xml

clean:
	rm -rf ./pmd-java-dist/target/
	rm -rf ./pmd-java-custom/target/

designer:
	@echo "Starting PMD designer..."
	JAVAFX_HOME=/Users/nbaumgartner/Library/Java/JavaVirtualMachines/javafx-sdk-17.0.7 pmd-bin-7.0.0-rc1/bin/pmd designer
