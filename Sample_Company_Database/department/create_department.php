<?php

require "../config.php";
require "../common.php";


if (isset($_POST['submit'])) {

    try  {
        $connection = new PDO($dsn, $username, $password, $options);
        
        $new_department = array(
            "deptName" => $_POST['deptName'],
            "deptNum"  => $_POST['deptNum'],
            "managerSSN"     => $_POST['managerSSN']
        );
        
        $sql = sprintf(
            "INSERT INTO %s (%s) values (%s)",
            "Department",
            implode(", ", array_keys($new_department)),
            ":" . implode(", :", array_keys($new_department))
            );
        
        $statement = $connection->prepare($sql);
        $statement->execute($new_department);
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}
?>

<?php require "../templates/header.php"; ?>

<?php if (isset($_POST['submit']) && $statement) { ?>
<?php } ?>

<h2>Add a Department</h2>

<form method="post">

 	<label for="DeptName">DeptName</label>
    <input type="text" name="deptName" id="deptName">
    
    <label for="deptNum">DeptNum</label>
    <input type="text" name="deptNum" id="deptNum">
    
    <label for="managerSSN">ManagerSSN</label>
    <input type="text" maxlength='9' minlength='9' name="managerSSN" id="managerSSN">

    <input type="submit" name="submit" value="Submit">
</form>



<?php


try {
    $connectionTwo = new PDO($dsn, $username, $password, $options);
    
    $sqlTwo = "SELECT * FROM Department";
    
    $statementTwo = $connectionTwo->prepare($sqlTwo);
    $statementTwo->execute();
    
    $result = $statementTwo->fetchAll();
} catch(PDOException $error) {
    echo $sqlTwo . "<br>" . $error->getMessage();
}
?>
      
<h2>Existing department numbers and manager SSNs </h2>

<table>
    <thead>
        <tr>
         <th>DeptNum</th>
        <th>Manager SSN</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
        <tr>
      <td><?php echo escape($row["deptNum"]); ?></td>
        <td><?php echo escape($row["managerSSN"]); ?></td>

        </tr>
    <?php endforeach; ?>
    </tbody>
</table>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>
