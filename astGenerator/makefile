.PHONY: all build run clean

# Default value for the DIRECTORY variable
DIRECTORY := ./testSrc/java
OUTPUT_FOLDER := ./parsedFiles

all: clean build run

setup:
	./mvnw clean install

build:
	./mvnw clean install
	unzip -o ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT.zip -d ./pmd-java-dist/target/
	cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/pmd-java-custom-1.0.0-SNAPSHOT.jar ./pmd-bin-7.0.0-rc3/lib/
	cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/jackson-annotations-2.12.3.jar ./pmd-bin-7.0.0-rc3/lib/
		cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/jackson-core-2.12.3.jar ./pmd-bin-7.0.0-rc3/lib/
		cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/jackson-databind-2.12.3.jar ./pmd-bin-7.0.0-rc3/lib/

#	./mvnw clean install
#	unzip -o ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT.zip -d ./pmd-java-dist/target/
#	cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/pmd-java-custom-1.0.0-SNAPSHOT.jar ./pmd-bin-7.0.0-rc2/lib/
#	cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/jackson-annotations-2.12.3.jar ./pmd-bin-7.0.0-rc2/lib/
#		cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/jackson-core-2.12.3.jar ./pmd-bin-7.0.0-rc2/lib/
#		cp ./pmd-java-dist/target/pmd-java-bin-1.0.0-SNAPSHOT/lib/jackson-databind-2.12.3.jar ./pmd-bin-7.0.0-rc2/lib/

run:
	@echo "Start time: $$(date)"; \
	START_TIME=$$(date +%s); \
	export OUTPUT_FOLDER=$(OUTPUT_FOLDER); \
	export DIRECTORY=$(DIRECTORY); \
	rm -rf $(OUTPUT_FOLDER); \
	./pmd-bin-7.0.0-rc3/bin/pmd check -d $(DIRECTORY) -f text -R custom-java-ruleset.xml; \
	echo "End time: $$(date)"; \
	END_TIME=$$(date +%s); \
	ELAPSED_TIME=$$((END_TIME - START_TIME)); \
	echo "Elapsed time: $$ELAPSED_TIME seconds"


clean:
	rm -rf ./pmd-java-dist/target/
	rm -rf ./pmd-java-custom/target/

designer:
	@echo "Starting PMD designer..."
	JAVAFX_HOME=/Users/nbaumgartner/Library/Java/JavaVirtualMachines/javafx-sdk-17.0.7 pmd-bin-7.0.0-rc1/bin/pmd designer
