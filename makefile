.PHONY: all build run clean

all: clean build run

setup:
	./mvnw clean install

build:
	./mvnw clean install
	unzip -o ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT.zip -d ./pmd-java-dist/target/
	cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/pmd-java-custom-1.0.0-SNAPSHOT.jar ./pmd-bin-7.0.0-rc1/lib/

run:
#	./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/bin/pmd -d /Users/nbaumgartner/Desktop/javaAnalyzeProject -f text -R custom-java-ruleset.xml
	./pmd-bin-7.0.0-rc1/bin/pmd check -d /Users/nbaumgartner/Desktop/src -f text -R custom-java-ruleset.xml

designer:
	@echo "Starting PMD designer..."
	JAVAFX_HOME=/Users/nbaumgartner/Library/Java/JavaVirtualMachines/javafx-sdk-17.0.7 pmd-bin-7.0.0-rc1/bin/pmd designer

clean:
	rm -rf ./pmd-java-dist/target/
	rm -rf ./pmd-java-custom/target/
