.PHONY: all build run clean

all: clean build run

setup:
	./mvnw clean install

build:
	./mvnw clean install
	unzip -o ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT.zip -d ./pmd-java-dist/target/

run:
	./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/bin/run.sh pmd -d /Users/nbaumgartner/Desktop/flyway-core -f text -R custom-java-ruleset.xml

designer:
	@echo "Starting PMD designer..."
	JAVAFX_HOME=/Users/nbaumgartner/Library/Java/JavaVirtualMachines/javafx-sdk-17.0.7 && pmd-bin-7.0.0-rc2/bin/pmd designer

clean:
	rm -rf ./pmd-java-dist/target/
	rm -rf ./pmd-java-custom/target/
