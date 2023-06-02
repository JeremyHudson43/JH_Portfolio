<?php


require "../config.php";
require "../common.php";

try {
    $connection = new PDO($dsn, $username, $password, $options);
    
    $sql = "SELECT * FROM Department";
    
    $statement = $connection->prepare($sql);
    $statement->execute();
    
    $result = $statement->fetchAll();
} catch(PDOException $error) {
    echo $sql . "<br>" . $error->getMessage();
}
?>

<?php require "../templates/header.php"; ?>
        
<h2>Update Department</h2>

<table>
    <thead>
        <tr>
         <th>DeptName</th>
        <th>DeptNum</th>
        <th>ManagerSSN</th>
        <th>Edit</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
        <tr>
        <td><?php echo escape($row["deptName"]); ?></td>
        <td><?php echo escape($row["deptNum"]); ?></td>
        <td><?php echo escape($row["managerSSN"]); ?></td>
            <td><a href="update_single_department.php?deptNum=<?php echo escape($row["deptNum"]); ?>">Edit</a></td>
        </tr>
    <?php endforeach; ?>
    </tbody>
</table>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>
