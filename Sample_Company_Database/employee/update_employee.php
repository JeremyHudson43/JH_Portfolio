<?php

require "../config.php";
require "../common.php";

try {
    $connection = new PDO($dsn, $username, $password, $options);
    
    $sql = "SELECT * FROM Employee";
    
    $statement = $connection->prepare($sql);
    $statement->execute();
    
    $result = $statement->fetchAll();
} catch(PDOException $error) {
    echo $sql . "<br>" . $error->getMessage();
}
?>

<?php require "../templates/header.php"; ?>
        
<h2>Update Employee</h2>

<table>
    <thead>
        <tr>
         <th>Address</th>
        <th>DOB</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Middle Initial</th>
        <th>SSN</th>
        <th>Edit</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
        <tr>
        <td><?php echo escape($row["Address"]); ?></td>
        <td><?php echo escape($row["dob"]); ?></td>
        <td><?php echo escape($row["Fname"]); ?></td>
        <td><?php echo escape($row["Lname"]); ?></td>
        <td><?php echo escape($row["Minit"]); ?></td>
        <td><?php echo escape($row["SSN"]); ?></td>
            <td><a href="update_single_employee.php?SSN=<?php echo escape($row["SSN"]); ?>">Edit</a></td>
        </tr>
    <?php endforeach; ?>
    </tbody>
</table>

<br>
<a href="index.php">Back to home</a>
</br>

    <tr>
    </tr>
<?php require "../templates/footer.php"; ?>
