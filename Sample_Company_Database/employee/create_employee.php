<?php

require "../config.php";
require "../common.php";
    

if (isset($_POST['submit'])) {

    
    try  {
        $connection = new PDO($dsn, $username, $password, $options);
        
        $new_user = array(
            "Address" => $_POST['Address'],
            "dob"  => $_POST['dob'],
            "Fname"     => $_POST['Fname'],
            "Lname"       => $_POST['Lname'],
            "Minit"  => $_POST['Minit'],
            "SSN"  => $_POST['SSN']
        );
        
        $sql = sprintf(
            "INSERT INTO %s (%s) values (%s)",
            "Employee",
            implode(", ", array_keys($new_user)),
            ":" . implode(", :", array_keys($new_user))
            );
        
        $statement = $connection->prepare($sql);
        $statement->execute($new_user);
        
        
        
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}
?>


<?php require "../templates/header.php"; ?>

<?php if (isset($_POST['submit']) && $statement) { ?>
<?php } ?>

<h2>Add an employee</h2>

<form method="post">

 	<label for="Address">Address</label>
    <input type="text" name="Address" id="Address">
    
    <label for="dob">Date of Birth</label>
    <input type="text" name="dob" id="dob">
    
    <label for="Fname">First Name</label>
    <input type="text" name="Fname" id="Fname">
    
     <label for="Lname">Last Name</label>
    <input type="text" name="Lname" id="Lname">
    
     <label for="Minit">Middle Initial</label>
    <input type="text" maxlength='1' minlength='1' name="Minit" id="Minit">
    
      <label for="SSN">SSN</label>
    <input type="text" maxlength='9' minlength='9' name="SSN" id="SSN">
    
    <input type="submit" name="submit" value="Submit">
</form>


<?php


try {
    $connectionTwo = new PDO($dsn, $username, $password, $options);
    
    $sqlTwo = "SELECT * FROM Employee";
    
    $statementTwo = $connectionTwo->prepare($sqlTwo);
    $statementTwo->execute();
    
    $result = $statementTwo->fetchAll();
} catch(PDOException $error) {
    echo $sqlTwo . "<br>" . $error->getMessage();
}
?>
        
     
<h2>Existing SSNs</h2>

<table>
    <thead>
        <tr>
        <th>SSN</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
        <tr>
        <td><?php echo escape($row["SSN"]); ?></td>
        </tr>
    <?php endforeach; ?>
    </tbody>
</table>


<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>
