# les-2021Q3
Lab de Engenharia de Software

## How to build
cd asniffer
mvn clean package -P executable
cd ..

## Annotationtest
### Run project on tests
java -jar asniffer/target/asniffer.jar -p asniffer/annotationtest -r reports/2.4.8.2/
### Run original on tests
java -jar jars/asniffer2.4.7.jar -p asniffer/annotationtest -r reports/2.4.7/

## Spring
### Run project on spring
java -jar asniffer/target/asniffer.jar -p spring-boot-2.6.0-M3 -r reports/2.4.8.2/
### Run original on spring
java -jar jars/asniffer2.4.7.jar -p spring-boot-2.6.0-M3 -r reports/2.4.7/

## Compare
### Compare tests
python json-compare.py -f1 "reports/2.4.7/annotationtest.json" \
    -f2 "reports/2.4.8.1/annotationtest.json"

### Compare spring
python json-compare.py -f1 "reports/2.4.7/spring-boot-2.6.0-M3.json" \
    -f2 "reports/2.4.8.1/spring-boot-2.6.0-M3.json"
