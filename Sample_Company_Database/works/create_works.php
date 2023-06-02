<?php

require "../config.php";
require "../common.php";

if (isset($_POST['submit'])) {
    
    try  {
        $connection = new PDO($dsn, $username, $password, $options);
        
        $new_works = array(
            "deptNum" => $_POST['deptNum'],
            "ProjName"  => $_POST['ProjName'],
            "ProjNum"     => $_POST['ProjNum'],
            "SSN"     => $_POST['SSN']
        );
        
        $sql = sprintf(
            "INSERT INTO %s (%s) values (%s)",
            "Works",
            implode(", ", array_keys($new_works)),
            ":" . implode(", :", array_keys($new_works))
            );
        
        $statement = $connection->prepare($sql);
        $statement->execute($new_works);
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}
?>

<?php require "../templates/header.php"; ?>

<?php if (isset($_POST['submit']) && $statement) { ?>
<?php } ?>

<h2>Add a Works relation</h2>

<form method="post">

 	<label for="deptNum">DeptNum</label>
    <input type="text" name="deptNum" id="deptNum">
    
    <label for="ProjName">ProjName</label>
    <input type="text" name="ProjName" id="ProjName">
    
    <label for="ProjNum"">ProjNum</label>
    <input type="text" name="ProjNum" id="ProjNum">
    
    <label for="SSN"">SSN</label>
    <input type="text" name="SSN"" id="SSN"">

    <input type="submit" name="submit" value="Submit">
</form>

<?php

try {
    $connectionTwo = new PDO($dsn, $username, $password, $options);
    
    $sqlTwo = "SELECT * FROM Works";
    
    $statementTwo = $connectionTwo->prepare($sqlTwo);
    $statementTwo->execute();
    
    $result = $statementTwo->fetchAll();
} catch(PDOException $error) {
    echo $sqlTwo . "<br>" . $error->getMessage();
}
?>
        
     
<h2>Existing Key Constraints</h2>

<table>
    <thead>
        <tr>
        <th>deptNum</th>
        <th>ProjName</th>
        <th>ProjNum</th>
        <th>SSN</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
        <tr>
        <td><?php echo escape($row["deptNum"]); ?></td>
        <td><?php echo escape($row["ProjName"]); ?></td>
        <td><?php echo escape($row["ProjNum"]); ?></td>
        <td><?php echo escape($row["SSN"]); ?></td>
        </tr>
    <?php endforeach; ?>
    </tbody>
</table>


<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>

