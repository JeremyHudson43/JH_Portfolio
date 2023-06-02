<?php

require "../config.php";
require "../common.php";


if (isset($_POST['submit'])) {
    
    
    try  {
        $connection = new PDO($dsn, $username, $password, $options);
        
        $new_project = array(
            "ProjDesc" => $_POST['ProjDesc'],
            "ProjName"  => $_POST['ProjName'],
            "ProjNum"     => $_POST['ProjNum']
        );
        
        $sql = sprintf(
            "INSERT INTO %s (%s) values (%s)",
            "Project",
            implode(", ", array_keys($new_project)),
            ":" . implode(", :", array_keys($new_project))
            );
        
        $statement = $connection->prepare($sql);
        $statement->execute($new_project);
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}
?>

<?php require "../templates/header.php"; ?>

<?php if (isset($_POST['submit']) && $statement) { ?>
<?php } ?>

<h2>Add a Project</h2>

<form method="post">

 	<label for="ProjDesc">ProjDesc</label>
    <input type="text" name="ProjDesc" id="ProjDesc">
    
    <label for="ProjName">ProjName</label>
    <input type="text" name="ProjName" id="ProjName">
    
    <label for="ProjNum">ProjNum</label>
    <input type="text" name="ProjNum" id="ProjNum">

    <input type="submit" name="submit" value="Submit">
</form>



<?php

try {
    $connectionTwo = new PDO($dsn, $username, $password, $options);
    
    $sqlTwo = "SELECT * FROM Project";
    
    $statementTwo = $connectionTwo->prepare($sqlTwo);
    $statementTwo->execute();
    
    $result = $statementTwo->fetchAll();
} catch(PDOException $error) {
    echo $sqlTwo . "<br>" . $error->getMessage();
}
?>
      
<h2>Existing Project names and numbers</h2>

<table>
    <thead>
        <tr>
         <th>ProjName</th>
        <th>ProjNum</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
        <tr>
      <td><?php echo escape($row["ProjName"]); ?></td>
        <td><?php echo escape($row["ProjNum"]); ?></td>

        </tr>
    <?php endforeach; ?>
    </tbody>
</table>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>
