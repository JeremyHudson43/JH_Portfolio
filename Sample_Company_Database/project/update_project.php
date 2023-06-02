<?php


require "../config.php";
require "../common.php";

try {
    $connection = new PDO($dsn, $username, $password, $options);
    
    $sql = "SELECT * FROM Project";
    
    $statement = $connection->prepare($sql);
    $statement->execute();
    
    $result = $statement->fetchAll();
} catch(PDOException $error) {
    echo $sql . "<br>" . $error->getMessage();
}
?>

<?php require "../templates/header.php"; ?>
        
<h2>Update Projects</h2>

<table>
    <thead>
        <tr>
         <th>ProjName</th>
        <th>ProjNum</th>
        <th>ProjDesc</th>
        <th>Edit</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
        <tr>
      <td><?php echo escape($row["ProjName"]); ?></td>
        <td><?php echo escape($row["ProjNum"]); ?></td>
        <td><?php echo escape($row["ProjDesc"]); ?></td>
            <td><a href="update_single_project.php?ProjNum=<?php echo escape($row["ProjNum"]); ?>">Edit</a></td>
        </tr>
    <?php endforeach; ?>
    </tbody>
</table>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>
