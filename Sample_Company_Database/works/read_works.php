<?php

require "../config.php";
require "../common.php";
        
if (isset($_POST['submit'])) {
    try  {
        
        $connection = new PDO($dsn, $username, $password, $options);
        
        $sql = "SELECT *
                        FROM Works
                        WHERE SSN = :SSN";
        
        $location = $_POST['SSN'];
        
        $statement = $connection->prepare($sql);
        $statement->bindParam(':SSN', $location, PDO::PARAM_STR);
        $statement->execute();
        
        $result = $statement->fetchAll();
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}
?>

<?php require "../templates/header.php"; ?>
        
<?php  
if (isset($_POST['submit'])) {
    if ($result && $statement->rowCount() > 0) { ?>
        <h2>Results</h2>

        <table>
            <thead>
                <tr>
        <th>DeptName</th>
        <th>ProjName</th>
        <th>ProjNum</th>
        <th>SSN</th>
                </tr>
            </thead>
            <tbody>
        <?php foreach ($result as $row) { ?>
            <tr>
        <td><?php echo escape($row["deptNum"]); ?></td>
        <td><?php echo escape($row["ProjName"]); ?></td>
        <td><?php echo escape($row["ProjNum"]); ?></td>
        <td><?php echo escape($row["SSN"]); ?></td>
            </tr>
        <?php } ?>
        </tbody>
    </table>
    <?php } else { ?>
        <blockquote>No results found for <?php echo escape($_POST['SSN']); ?>.</blockquote>
    <?php } 
} ?> 

<h2>Find  works relation based on SSN</h2>

<form method="post">
    <label for="SSN">SSN</label>
    <input type="text"  maxlength='9' minlength='9' id="SSN" name="SSN">
    <input type="submit" name="submit" value="View Results">
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
        
     
<h2>Existing Manager SSNs</h2>

<table>
    <thead>
        <tr>
        <th>Manager SSN</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
        <tr>
        <td><?php echo escape($row["managerSSN"]); ?></td>
        </tr>
    <?php endforeach; ?>
    </tbody>
</table>


<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>

