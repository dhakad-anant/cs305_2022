# cs305_2022

## [Assignemnt 1](https://docs.google.com/document/d/1a1Foh7ni-N6KXhkDdST14_hk7sH-3rJJoXfhtxRKcC8/edit)

## [Repository Link](https://github.com/dhakad-anant/cs305_2022)

### Submitter name: Anant Dhakad

### Roll No.: 2019CSB1070

### Course: Software Engineering (CS305)

=================================


1. What does this program do

The programme takes SQL queries from an XML file and executes Create, Read, Update, and Delete SQL queries (CRUD). The data is parsed, and the input is used to replace the $values. The sakila Shell is where the programme logs. After that, the query is sent to the database. After that, the output is returned and printed. The LibraryTest.java programme runs a series of tests that include create, read, update, and delete, and reports errors if any of the queries are erroneous.


2. A description of how this program works (i.e. its logic)

My programme runs Create, Read, Update, and Delete SQL queries (CRUD).
The queries are read from an XML file. ${propert_name_here} is used to populate the properties of the XML statements. Then it replaces ${values} with the given input or multiple inputs. The queryId and query are saved in the dictionary when the XML file is parsed. In this case, the input can be in the form of a class or a data type. A homogeneous array or homogeneous ArrayList can be used as the input. If the input is in the form of a class, field in Java are used to extract the associated value. If the input is non-class, the data type is determined, and the programme is run accordingly.

The data type of the input object is now checked against the data type in the XML file. If they don't match, an error message is displayed.
The query is then executed in the terminal, and the results are provided to the reader. The number of rows matched is supplied to the reader if the query is an insert, update, or delete query. The output data is sent to the output if the query is a select query. The values are added to the classes using Field objects if the output is in the form of a class.

The following functions were implemented:
public int insert(String queryId, Object queryParam);
public int delete(String queryId, Object queryParam);
public int update(String queryId, Object queryParam);
public Object selectOne(String queryId, Object queryParam, Class resultType);
public List<?> selectMany(String queryId, Object queryParam, Class resultItemType);

The format of the xml file is as follows:
<sql id="array_string" paramType="org.foo.Bar">
   <![CDATA[
   INSERT INTO film_actor (actor_id, film_id, last_update) VALUES (${value});
   ]]>
</sql>
Here id contains the id of the query. 
The paramType contains the param type of the query. 
The query has ${value} where the value will be replaced by the input provided.

The main app is present at : \cs305_2022\assignment_1\app
The main codes are present at : \cs305_2022\assignment_1\app\src\main\java\assignment_1


3. How to compile and run this program

i) First extract from the zip file (downloaded either from the github or the classroom).

ii) Change the mysql password & username by going into the (\cs305_2022\assignment_1\app\src\test\java\assignment_1\LibraryTest.java)

iii) 
Method 1: Using IntelliJ IDEA
Press the run option in 'LibraryTest.java'. To check code coverage, press run with the coverage method

Method 2: Using CMD
-> gradle build
-> gradle test

