package assignment_1;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.Array;
import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Arrays;

public class Library implements SqlRunner{
    private String dbUrl, user, password;
    private HashMap<String, String> idQueryMap;
    private HashMap<String, String> idClassNameMap;

    // For db Connection.
    static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
    private Connection dbCon = null;
    private Statement stmt = null;

    Library(String dbUrl, String user, String password, String xmlFilePath){

        // Initializing HashMap.
        this.idQueryMap = new HashMap<String, String>();
        this.idClassNameMap = new HashMap<String, String>();

        // Setting dbLink, username & password (required for database connection)
        this.dbUrl = dbUrl;
        this.user = user;
        this.password = password;

        /*--- Parsing XML file and storing all queries in a hashmap (with key as id) --------*/
        XMLParser(xmlFilePath);
    } // parametric constructor ends

    private void XMLParser(String xmlFilePath) {
        try{
            /*--- Parsing XML file and storing all queries in a hashmap (with key as id) --------*/
            File xmlFile = new File(xmlFilePath);

            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = factory.newDocumentBuilder();

            // Parsing the XML file into a Document
            Document doc = dBuilder.parse(xmlFile);

            // Normalizing the document to ensure that correct results are generated.
            doc.getDocumentElement().normalize();

            // Getting the root element of the document.
            System.out.println("Name of Root element: " + doc.getDocumentElement().getNodeName());

            // Getting a NodeList of SQL queries in the document with getElementsByTagName.
            NodeList nList = doc.getElementsByTagName("sql");

            System.out.println("\nPrinting all queries:-------------------");

            // Iterating over all the sql queries to store them in HashMap.
            int i = 0;
            while(i < nList.getLength()){
                // Current SQL child.
                Node nNode = nList.item(i);

                if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element elem = (Element) nNode;

                    // Getting the queryId attribute with getAttribute.
                    String queryId = elem.getAttribute("id");

                    // Getting the query Statement
                    String queryStatement = nNode.getTextContent().trim();
                    // Storing the queryStatement (mapped to queryID)
                    this.idQueryMap.put(queryId, queryStatement);

                    // Getting the paramType attribute with getAttribute.
                    String className = elem.getAttribute("paramType");
                    // Storing the paramType className (mapped to queryID)
                    this.idClassNameMap.put(queryId, className);

                    System.out.println("-- queryId : "+queryId);
                    System.out.println("   query : "+queryStatement);
                } // if condition ends

                i++;
            } // while loop ends

            System.out.println("---------------------------------------------------------------------------------------\n");
        } // try ends
        catch (Exception excep){
            System.out.println("Error! : while parsing XML file");
            excep.printStackTrace();
        } // catch ends
    }

    private String getFieldValue(Object queryParam, String paramName) {
        StringBuilder fieldVal = new StringBuilder("'");

        try{
            Class className = queryParam.getClass();
            Field field = className.getDeclaredField(paramName);
            fieldVal.append(field.get(queryParam).toString());
            fieldVal.append("'");
        } // try ends
        catch (Exception exception){
            exception.printStackTrace();
        } // catch ends

        return fieldVal.toString();
    } // getFieldValue ends

    private int getParamType(String queryId, Object queryParam) {

        if(queryParam.getClass().getName().compareTo(this.idClassNameMap.get(queryId)) != 0){
            throw new java.lang.RuntimeException("The object passed as parameter is not a instance of the class mentioned in SQL query");
        }
        String className = queryParam.getClass().getName();

        // if queryParam is primitive data type
        if(
                className.equals("java.lang.Integer") ||
                className.equals("java.lang.Double") ||
                className.equals("java.lang.Character") ||
                className.equals("java.lang.Byte") ||
                className.equals("java.lang.Short") ||
                className.equals("java.lang.Boolean") ||
                className.equals("java.lang.Float") ||
                className.equals("java.lang.Long") ||
                className.equals("java.lang.String")
        )
        {
            return 0;
        }

        // if queryParam is collection of primitive data type
        if(
                className.equals("[F") ||
                className.equals("[Z") ||
                className.equals("[I") ||
                className.equals("[B") ||
                className.equals("[S") ||
                className.equals("[D") ||
                className.equals("[C") ||
                className.equals("[Ljava.lang.String;")
        )
        {
            return 1;
        }

        // if queryParam is a class of parameters itself.
        return 2;
    } // getParamType ends

    private String constructQuery(String queryId, String rawQuery, Object queryParam) {
        System.out.println("**constructQuery Begin**");
        StringBuffer queryWithParams = new StringBuffer();

        int paramType = getParamType(queryId, queryParam);
        int remainingStartIdx = 0;
        while(true){
            int dollarIdx = rawQuery.indexOf('$', remainingStartIdx);
            int openCurlyIdx = rawQuery.indexOf('{', remainingStartIdx);
            int closeCurlyIdx = rawQuery.indexOf('}', remainingStartIdx);

            if(dollarIdx == -1){
                queryWithParams.append(rawQuery.substring(remainingStartIdx));
                break;
            }
            queryWithParams.append(rawQuery.substring(remainingStartIdx, dollarIdx));
            String paramName = rawQuery.substring(openCurlyIdx+1, closeCurlyIdx);
            remainingStartIdx = closeCurlyIdx+1;

            StringBuilder value = new StringBuilder();
            // if queryParam is primitive data type
            if(paramType == 0){
                value.append("'").append(queryParam).append("'");
            }
            // if queryParam is collection of primitive data type
            else if(paramType == 1){
                int len = Array.getLength(queryParam), i = 0;

                value.append("(");
                while(i < len){
                    Object object = Array.get(queryParam, i);

                    value.append("'").append(object).append("'");

                    i++;
                    if(i == len) break;
                    value.append(",");
                }
                value.append(")");
            }
            // if queryParam is a class of parameters itself.
            else{
                value = new StringBuilder(getFieldValue(queryParam, paramName));
            }
            queryWithParams.append(value);
        }
        System.out.println("**constructQuery Ends**");
        return queryWithParams.toString();
    } // constructQuery ends

    private int getNumRows(ResultSet resultSet){
        int rows = 0;
        try {
            if(resultSet.last()){
                rows = resultSet.getRow();
                resultSet.beforeFirst();
            }
        } // try ends
        catch (Exception exception){
            exception.printStackTrace();
        } // catch ends
        return rows;
    } // getNumRows ends

    private ArrayList<String> getColumnNames(ResultSet resultSet) {
        ArrayList<String> ans = new ArrayList<String>();

        try {
            ResultSetMetaData resultSetMetaData = resultSet.getMetaData();
            for(int i = 1; i <= resultSetMetaData.getColumnCount(); i++){
                String colName = resultSetMetaData.getColumnName(i);
                ans.add(colName);
            }
        } // try ends
        catch (SQLException e) {
            e.printStackTrace();
        } // catch ends

        return ans;
    } // getColumnNames ends

    private void closedbConnection(){
        try{
            // clean-up enviroment.
            /*resultSet.close();*/
            this.stmt.close();
            this.dbCon.close();
        } // try ends
        catch (Exception excep){
            System.out.println("Error while closing connection");
            excep.printStackTrace();
        } // catch ends
        finally{
            System.out.println("Database Connection closed");
        } // finally ends
    } // closedbConnection ends

    private Object fireQuery(String query, boolean transact){
        System.out.println("**fireQuery Begin**");
        Object resultSet = null;
        this.dbCon = null;
        this.stmt = null;

        try{
            Class.forName(JDBC_DRIVER);
            //getting database connection to MySQL server
            dbCon = DriverManager.getConnection(this.dbUrl, this.user, this.password);

            //getting PreparedStatment to execute query
            stmt = dbCon.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);

            if(transact) {
                resultSet = stmt.executeUpdate(query);
            }
            else{
                resultSet = stmt.executeQuery(query);
            }
            System.out.println("**fireQuery Ends**");
            return resultSet;
        } // try ends

        catch(Exception excep){
            System.out.println("--Error in fireQuery--");
            excep.printStackTrace();
        } // catch ends
        return null;
    } // fireQuery ends

    @Override
    public Object selectOne(String queryId, Object queryParam, Class resultType) {

        String query = constructQuery(queryId, this.idQueryMap.get(queryId), queryParam);
        System.out.println("Current Query: "+query);
        System.out.println("Firing from selectOne: "+query);
        ResultSet resultSet = (ResultSet) fireQuery(query, false);

        // check if there are more than one row in the resultset.
        int numRows = getNumRows(resultSet);
        System.out.println("Number of rows for current query: "+numRows);
        if(numRows == 0){
            System.out.println("Zero Rows in the resultset for current query");
            return null;
        }
        if(numRows > 1){
            throw new RuntimeException("--More the one rows in result--");
        }

        // Get all the column names
        ArrayList<String> columnNames = getColumnNames(resultSet);
        System.out.println("Number of columns for current query: "+columnNames.size());

        // Populate resultSet into the resultType object.
        Object object = null;

        try {

            object = Class.forName(resultType.getName()).getDeclaredConstructor().newInstance();
            Class cls = object.getClass();

            while(resultSet.next()){
                for(int i = 0; i < columnNames.size(); i++){
                    String columnName = columnNames.get(i);
                    String columnValue = resultSet.getString(i+1);
                    /*Integer columnType = columnTypes.get(i);*/
                    Field field = cls.getDeclaredField(columnName);

                    field.set(object, columnValue);
                }
            }

            resultSet.close();
            closedbConnection();

            return object;
        } // try ends
        catch (Exception exception){
            System.out.println("--Error in selectOne--");
            exception.printStackTrace();
        } // catch ends
        return null;
    } // selectOne ends

    @Override
    public List<Object> selectMany(String queryId, Object queryParam, Class resultItemType) {

        String query = constructQuery(queryId, this.idQueryMap.get(queryId), queryParam);
        System.out.println("Current Query: "+query);
        System.out.println("Firing from selectMany: "+query);
        ResultSet resultSet = (ResultSet) fireQuery(query, false);

        // check if there are more than one row in the resultset.
        int numRows = getNumRows(resultSet);
        System.out.println("Number of rows for current query: "+numRows);
        if(numRows == 0){
            System.out.println("Zero Rows in the resultset for query");
            return null;
        }

        // Get all the column names
        ArrayList<String> columnNames = getColumnNames(resultSet);
        System.out.println("Number of columns for current query: "+columnNames.size());

        // Initializing Array<Object> for storing final results
        ArrayList<Object> fresults = new ArrayList<Object>();

        try {

            while(resultSet.next()){
                Object object = Class.forName(resultItemType.getName()).getDeclaredConstructor().newInstance();
                Class cls = object.getClass();
                for(int i = 0; i < columnNames.size(); i++){
                    String columnName = columnNames.get(i);
                    String columnValue = resultSet.getString(i+1);
                    Field field = cls.getDeclaredField(columnName);
                    field.set(object, columnValue);
                }
                fresults.add(object);
            } // while ends

            resultSet.close();
            closedbConnection();

            return fresults;
        } // try ends
        catch (Exception e) {
            System.out.println("--Error in selectMany--");
            e.printStackTrace();
        } // catch ends
        return null;
    } // selectMany Ends

    @Override
    public int update(String queryId, Object queryParam) {

        String query = constructQuery(queryId, this.idQueryMap.get(queryId), queryParam);
        System.out.println("Current Query: "+query);
        System.out.println("Firing from update: "+query);
        Object result = fireQuery(query, true);

        int res = (int) result;
        if(res == 0){
            System.out.println("Error: result is null for Current Query");
            return -1;
        }

        closedbConnection();

        return res;
    } // update ends

    @Override
    public int insert(String queryId, Object queryParam) {

        String query = constructQuery(queryId, this.idQueryMap.get(queryId), queryParam);
        System.out.println("Current Query: "+query);
        System.out.println("Firing from insert: "+query);
        Object result = fireQuery(query, true);

        int res = (int) result;
        if(res == 0){
            System.out.println("Error: result is null for Current Query");
            return -1;
        }

        closedbConnection();

        return res;
    } // insert ends

    @Override
    public int delete(String queryId, Object queryParam) {

        String query = constructQuery(queryId, this.idQueryMap.get(queryId), queryParam);
        System.out.println("Current Query: "+query);
        System.out.println("Firing from delete: "+query);
        Object result = fireQuery(query, true);

        int res = (int) result;
        if(res == 0){
            System.out.println("Error: result is null for Current Query(row doesn't exist)");
            return -1;
        }

        closedbConnection();

        return res;
    } // delete ends
}

class parameter1{
    public String propX;
}

class parameter1_int{
    public Integer propX;
}

class parameter2{
    public String propX;
    public String propY;
}

class parameter3{
    public String propX;
    public String propY;
    public String propZ;
}

class resultSetClass{
    public String actor_id;
    public String first_name, last_name, last_update;
}
