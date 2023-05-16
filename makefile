.PHONY: all build run clean

all: clean build run

build:
	mkdir -p build
	javac -d build -cp 'pmd-bin-7.0.0-rc2/lib/*' src/*.java
	cp src/myrule.xml build
	jar -c -f custom-rule-example.jar -C build .

run:
	CLASSPATH=custom-rule-example.jar pmd-bin-7.0.0-rc2/bin/pmd check --no-cache -f text -d testsrc -R build/myrule.xml

designer:
	@echo "Starting PMD designer..."
	JAVAFX_HOME=/Users/nbaumgartner/Library/Java/JavaVirtualMachines/javafx-sdk-17.0.7 && pmd-bin-7.0.0-rc2/bin/pmd designer

clean:
	rm -rf build
	rm -rf custom-rule-example.jar
