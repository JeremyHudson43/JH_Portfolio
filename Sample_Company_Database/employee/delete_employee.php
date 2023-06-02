<?php


require "../config.php";
require "../common.php";

$success = null;


try {
  $connection = new PDO($dsn, $username, $password, $options);

  $sql = "SELECT * FROM Employee";

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

    $sql = "DELETE FROM Employee WHERE SSN = :SSN";

    $statement = $connection->prepare($sql);
    $statement->bindValue(':SSN', $id);
    $statement->execute();

  } catch(PDOException $error) {
    echo $sql . "<br>" . $error->getMessage();
  }
}

?>

<?php require "../templates/header.php"; ?>
        
<h2>Delete Employees</h2>

<form method="post">
  <input name="csrf" type="hidden" value="<?php echo escape($_SESSION['csrf']); ?>">
  <table>
    <thead>
      <tr>
        <th>Address</th>
        <th>DOB</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Middle Initial</th>
        <th>SSN</th>
        <th>Delete</th>
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
        <td><button type="submit" name="submit" value="<?php echo escape($row["SSN"]); ?>">Delete</button></td>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table>
</form>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>

