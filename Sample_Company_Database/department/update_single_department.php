<?php

require "../config.php";
require "../common.php";

if (isset($_POST['submit'])) {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'])) die();
    
    try {
        $connection = new PDO($dsn, $username, $password, $options);
        
        
        $department =[
            "deptName" => $_POST['deptName'],
            "deptNum"     => $_POST['deptNum'],
            "managerSSN"  => $_POST['managerSSN']
        ];
        
        $sql = "UPDATE Department
               SET deptName = :deptName,
                deptNum = :deptNum,
                managerSSN = :managerSSN
                WHERE deptNum = :deptNum";
        
        $statement = $connection->prepare($sql);
        $statement->execute($department);
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}

?>

<?php require "../templates/header.php"; ?>

<?php

if (isset($_GET['deptNum'])) {
    try {
        $connection = new PDO($dsn, $username, $password, $options);
        $DeptNum = $_GET['deptNum'];
        
        $sql = "SELECT * FROM Department WHERE deptNum = :deptNum";
        $statement = $connection->prepare($sql);
        $statement->bindValue(':deptNum', $DeptNum);
        $statement->execute();
        
        $department = $statement->fetch(PDO::FETCH_ASSOC);
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
} else {
    echo "Something went wrong!";
    exit;
}
?>


<h2>Edit a Department</h2>

<form method="post">
    <input name="csrf" type="hidden" value="<?php echo escape($_SESSION['csrf']); ?>">
    <?php foreach ($department as $key => $value) : ?>
      <label for="<?php echo $key; ?>"><?php echo ucfirst($key); ?></label>
	    <input type="text" name="<?php echo $key; ?>" deptNum="<?php echo $key; ?>" value="<?php echo escape($value); ?>" <?php echo ($key === 'deptNum' ? 'readonly' : null); ?>>
    <?php endforeach; ?> 
    <input type="submit" name="submit" value="Submit">
</form>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>
