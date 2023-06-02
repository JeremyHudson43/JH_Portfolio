<?php

require "../config.php";
require "../common.php";
       

if (isset($_POST['submit'])) {
    try  {
        
        $connection = new PDO($dsn, $username, $password, $options);
        
        $sql = "SELECT *
                        FROM Department
                        WHERE deptNum = :deptNum";
        
        $location = $_POST['deptNum'];
        
        $statement = $connection->prepare($sql);
        $statement->bindParam(':deptNum', $location, PDO::PARAM_STR);
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
        <th>ProjName</th>
        <th>ProjNum</th>
        <th>ProjDesc</th>
                </tr>
            </thead>
            <tbody>
        <?php foreach ($result as $row) { ?>
            <tr>
      <td><?php echo escape($row["deptName"]); ?></td>
        <td><?php echo escape($row["deptNum"]); ?></td>
        <td><?php echo escape($row["managerSSN"]); ?></td>
            </tr>
        <?php } ?>
        </tbody>
    </table>
    <?php } else { ?>
        <blockquote>No results found for <?php echo escape($_POST['deptNum']); ?>.</blockquote>
    <?php } 
} ?> 

<h2>Find Department based on deptNum</h2>

<form method="post">
    <label for="deptNum">deptNum</label>
    <input type="text" id="deptNum" name="deptNum">
    <input type="submit" name="submit" value="View Results">
</form>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>
