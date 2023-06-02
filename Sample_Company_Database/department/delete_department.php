<?php

require "../config.php";
require "../common.php";


$success = null;

try {
    $connection = new PDO($dsn, $username, $password, $options);
    
    $sql = "SELECT * FROM Department";
    
    $statement = $connection->prepare($sql);
    $statement->execute();
    
    $result = $statement->fetchAll();
} catch(PDOException $error) {
    echo $sql . "<br>" . $error->getMessage();
}

if (isset($_POST["submit"])) {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'])) die();
    
    try {
        $connection = new PDO($dsn, $username, $password, $options);
        
        $id = $_POST["submit"];
        
        $sql = "DELETE FROM Department WHERE deptNum = :deptNum";
        
        $statement = $connection->prepare($sql);
        $statement->bindValue(':deptNum', $id);
        $statement->execute();
        

    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}

?>
<?php require "../templates/header.php"; ?>
        
<h2>Delete department</h2>

<form method="post">
  <input name="csrf" type="hidden" value="<?php echo escape($_SESSION['csrf']); ?>">
  <table>
    <thead>
      <tr>
        <th>DeptName</th>
        <th>DeptNum</th>
        <th>Manager SSN</th>
        <th>Delete</th>
      </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
      <tr>
        <td><?php echo escape($row["deptNum"]); ?></td>
        <td><?php echo escape($row["deptName"]); ?></td>
        <td><?php echo escape($row["managerSSN"]); ?></td>
        <td><button type="submit" name="submit" value="<?php echo escape($row["deptNum"]); ?>">Delete</button></td>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table>
</form>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>

