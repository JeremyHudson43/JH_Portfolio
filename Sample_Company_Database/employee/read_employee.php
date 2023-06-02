<?php

require "../config.php";
require "../common.php";
        

if (isset($_POST['submit'])) {
    try  {
        
        $connection = new PDO($dsn, $username, $password, $options);
        
        $sql = "SELECT *
                        FROM Employee
                        WHERE SSN = :SSN";
        
        $location = $_POST['SSN'];
        
        $statement = $connection->prepare($sql);
        $statement->bindParam(':SSN', $location, PDO::PARAM_STR);
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
        <th>Address</th>
        <th>DOB</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Middle Initial</th>
        <th>SSN</th>

                </tr>
            </thead>
            <tbody>
        <?php foreach ($result as $row) { ?>
            <tr>
        <td><?php echo escape($row["Address"]); ?></td>
        <td><?php echo escape($row["dob"]); ?></td>
        <td><?php echo escape($row["Fname"]); ?></td>
        <td><?php echo escape($row["Lname"]); ?></td>
        <td><?php echo escape($row["Minit"]); ?></td>
        <td><?php echo escape($row["SSN"]); ?></td>
            </tr>
        <?php } ?>
        </tbody>
    </table>
    <?php } else { ?>
        <blockquote>No results found for <?php echo escape($_POST['SSN']); ?>.</blockquote>
    <?php } 
} ?> 

<h2>Find employee based on SSN</h2>

<form method="post">
    <label for="SSN">SSN</label>
    <input type="text"  maxlength='9' minlength='9' id="SSN" name="SSN">
    <input type="submit" name="submit" value="View Results">
</form>

<br>
<a href="index.php">Back to home</a>
</br>

<?php require "../templates/footer.php"; ?>
