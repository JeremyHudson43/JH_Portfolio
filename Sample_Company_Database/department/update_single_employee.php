<?php

require "../config.php";
require "../common.php";

if (isset($_POST['submit'])) {
    if (!hash_equals($_SESSION['csrf'], $_POST['csrf'])) die();
    
    try {
        $connection = new PDO($dsn, $username, $password, $options);
        
        
        $user =[
            "Address" => $_POST['Address'],
            "dob"  => $_POST['dob'],
            "Fname"     => $_POST['Fname'],
            "Lname"       => $_POST['Lname'],
            "Minit"  => $_POST['Minit'],
            "SSN"  => $_POST['SSN']
        ];
        
        $sql = "UPDATE Employee
               SET Address = :Address,
                dob = :dob,
                Fname = :Fname,
                Lname = :Lname,
                Minit = :Minit,
                SSN = :SSN
                WHERE SSN = :SSN";
        
        $statement = $connection->prepare($sql);
        $statement->execute($user);
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}

if (isset($_GET['SSN'])) {
    try {
        $connection = new PDO($dsn, $username, $password, $options);
        $SSN = $_GET['SSN'];
        
        $sql = "SELECT * FROM Employee WHERE SSN = :SSN";
        $statement = $connection->prepare($sql);
        $statement->bindValue(':SSN', $SSN);
        $statement->execute();
        
        $user = $statement->fetch(PDO::FETCH_ASSOC);
    } catch(PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
} else {
    echo "Something went wrong!";
    exit;
}
?>

<?php require "../templates/header.php"; ?>

<h2>Edit a user</h2>

<form method="post">
    <input name="csrf" type="hidden" value="<?php echo escape($_SESSION['csrf']); ?>">
    <?php foreach ($user as $key => $value) : ?>
      <label for="<?php echo $key; ?>"><?php echo ucfirst($key); ?></label>
	    <input type="text" name="<?php echo $key; ?>" SSN="<?php echo $key; ?>" value="<?php echo escape($value); ?>" <?php echo ($key === 'SSN' ? 'readonly' : null); ?>>
    <?php endforeach; ?> 
    <input type="submit" name="submit" value="Submit">
</form>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>
