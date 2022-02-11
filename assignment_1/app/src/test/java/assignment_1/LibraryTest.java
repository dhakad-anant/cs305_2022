package assignment_1;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LibraryTest {
    private Library library;

    @BeforeEach
    public void setUp() throws Exception {
        String dbUrl = "jdbc:mysql://localhost/sakila";
        String user = "root";
        String password = "mysql";
        /*String testXmlFilePath = "C:\\Users\\Dhakad\\Desktop\\proj\\final\\app\\src\\main\\resources\\testQueries.xml";*/
        String testXmlFilePath = "src\\main\\resources\\testQueries.xml";
        library = new Library(dbUrl, user, password, testXmlFilePath);
    }

    @Test
    @DisplayName("Testing the update method!")
    public void testUpdate() {
        parameter2 param = new parameter2();
        param.propX = "cena";
        param.propY = "2";
        assertEquals(1, library.update("updateLastName", param));
    }

    @Test
    @DisplayName("Testing the update method! (non existing)")
    public void testUpdate_nonExisting() {
        parameter2 param = new parameter2();
        param.propX = "cena";
        param.propY = "204";
        assertEquals(-1, library.update("updateLastName", param));
    }

    @Test
    @DisplayName("Testing the insert method!")
    public void testInsert() {
        parameter2 param = new parameter2();
        param.propX = "Salman";
        param.propY = "Khan";
        assertEquals(1, library.insert("insertActor", param));
    }

    // @Todo : increment the actor_id (propX) everytime testcases are ran
    @Test
    @DisplayName("Testing the delete method!")
    public void testDelete() {
        parameter1 param = new parameter1();
        param.propX = "201";
        assertEquals(1, library.delete("deleteActor", param));
    }

    @Test
    @DisplayName("Testing the delete method (deleting non existing row)!")
    public void testDelete_nonExistingRow() {
        parameter1 param = new parameter1();
        param.propX = "205";
        assertEquals(-1, library.delete("deleteActor", param));
    }

    @Test
    @DisplayName("Testing the selectOne method on a null resultset!")
    public void testSelectOne_onNullResult() {
        parameter1 param = new parameter1();
        param.propX = "10110101";
        Object object = new Object();
        object = library.selectOne("findActorsby_actorID", param, resultSetClass.class);
        assertNull(object);
    }

    @Test
    @DisplayName("Testing the selectOne method on a not null resultset!")
    public void testSelectOne_onNotNullResult() {
        parameter1 param = new parameter1();
        param.propX = "198";
        Object object = new Object();
        object = library.selectOne("findActorsby_actorID", param, resultSetClass.class);
        assertNotNull(object);
    }

    @Test
    @DisplayName("Testing the selectOne method on more than row resultset!")
    public void testSelectOne_onMoreThanOneRowInResult() {
        assertThrows( RuntimeException.class, () -> {
            parameter1 param = new parameter1();
            param.propX = "MOSTEL";
            Object object = new Object();
            object = library.selectOne("findActorsby_lastName", param, resultSetClass.class);
        });
    }

    @Test
    @DisplayName("Testing the selectOne method by passing a primitive paramter")
    public void testSelectOne_primitiveParameter() {
        Object object = new Object();
        object = library.selectOne("passingPrimitive", 198, resultSetClass.class);
        assertNotNull(object);
    }

    @Test
    @DisplayName("Testing the selectOne method by passing a array paramter")
    public void testSelectOne_arrayParameter() {
        int []arr = new int[1];
        arr[0] = 4;
        Object object = new Object();
        object = library.selectOne("passingArray", arr, resultSetClass.class);
        assertNotNull(object);
    }

    @Test
    @DisplayName("Testing the selectMany method by passing Array Two values")
    public void testSelectMany_passingArrayTwovalues() {
        int []arr = new int[2];
        arr[0] = 4;
        arr[1] = 5;
        Object object = new Object();
        object = library.selectMany("passingArray", arr, resultSetClass.class);
        assertNotNull(object);
    }

    @Test
    @DisplayName("Testing the selectMany method on a not null resultset!")
    public void testSelectMany_onNotNullResult() {
        parameter1 param = new parameter1();
        param.propX = "MOSTEL";
        Object object = new Object();
        object = library.selectMany("findActorsby_lastName", param, resultSetClass.class);
        assertNotNull(object);
    }

    @Test
    @DisplayName("Testing the selectMany method on a null resultset!")
    public void testSelectMany_onNullResult() {
        parameter1 param = new parameter1();
        param.propX = "204";
        Object object = new Object();
        object = library.selectMany("findActorsby_actorID", param, resultSetClass.class);
        assertNull(object);
    }
}