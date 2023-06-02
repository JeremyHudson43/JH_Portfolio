<?php

require "../config.php";
require "../common.php";

if (isset($_POST['submit'])) {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'])) die();
    
    try {
        $connection = new PDO($dsn, $username, $password, $options);
        
        
        $project =[
            "ProjName" => $_POST['ProjName'],
            "ProjNum"  => $_POST['ProjNum'],
            "ProjDesc"     => $_POST['ProjDesc'],
        ];
        
        $sql = "UPDATE Project
               SET ProjName = :ProjName,
               ProjNum = :ProjNum,
               ProjDesc = :ProjDesc
                WHERE ProjNum = :ProjNum";
        
        $statement = $connection->prepare($sql);
        $statement->execute($project);
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}

?>

<?php require "../templates/header.php"; ?>


<?php

if (isset($_GET['ProjNum'])) {
    try {
        $connection = new PDO($dsn, $username, $password, $options);
        $ProjNum = $_GET['ProjNum'];
        
        $sql = "SELECT * FROM Project WHERE ProjNum = :ProjNum";
        $statement = $connection->prepare($sql);
        $statement->bindValue(':ProjNum', $ProjNum);
        $statement->execute();
        
        $project = $statement->fetch(PDO::FETCH_ASSOC);
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
} else {
    echo "Something went wrong!";
    exit;
}
?>


<h2>Edit a Project</h2>

<form method="post">
    <input name="csrf" type="hidden" value="<?php echo escape($_SESSION['csrf']); ?>">
    <?php foreach ($project as $key => $value) : ?>
      <label for="<?php echo $key; ?>"><?php echo ucfirst($key); ?></label>
	    <input type="text" name="<?php echo $key; ?>" ProjNum="<?php echo $key; ?>" value="<?php echo escape($value); ?>" <?php echo ($key === 'ProjNum' ? 'readonly' : null); ?>>
    <?php endforeach; ?> 
    <input type="submit" name="submit" value="Submit">
</form>

<a href="index.php">Back to home</a>

<?php require "../templates/footer.php"; ?>
