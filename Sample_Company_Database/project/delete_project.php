<?php


require "../config.php";
require "../common.php";

$success = null;

  try {
  $connection = new PDO($dsn, $username, $password, $options);

  $sql = "SELECT * FROM Project";

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

    $sql = "DELETE FROM Project WHERE ProjNum = :ProjNum";

    $statement = $connection->prepare($sql);
    $statement->bindValue(':ProjNum', $id);
    $statement->execute();

    $success = "Project successfully deleted";
  } catch(PDOException $error) {
    echo $sql . "<br>" . $error->getMessage();
  }
  }



?>
<?php require "../templates/header.php"; ?>
        
<h2>Delete Projects</h2>

<?php if ($success) echo $success; ?>

<form method="post">
  <input name="csrf" type="hidden" value="<?php echo escape($_SESSION['csrf']); ?>">
  <table>
    <thead>
      <tr>
        <th>ProjName</th>
        <th>ProjNum</th>
        <th>ProjDesc</th>
        <th>Delete</th>
      </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row) : ?>
      <tr>
        <td><?php echo escape($row["ProjName"]); ?></td>
        <td><?php echo escape($row["ProjNum"]); ?></td>
        <td><?php echo escape($row["ProjDesc"]); ?></td>
        <td><button type="submit" name="submit" value="<?php echo escape($row["ProjNum"]); ?>">Delete</button></td>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table>
</form>

<br>
<a href="index.php">Back to home</a>
</br>
<?php require "../templates/footer.php"; ?>
