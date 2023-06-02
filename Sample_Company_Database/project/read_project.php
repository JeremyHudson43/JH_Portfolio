<?php

if (isset($_POST['submit'])) {
    try  {
        
        require "../config.php";
        require "../common.php";
        
        $connection = new PDO($dsn, $username, $password, $options);
        
        $sql = "SELECT *
                        FROM Project
                        WHERE ProjNum = :ProjNum";
        
        $location = $_POST['ProjNum'];
        
        $statement = $connection->prepare($sql);
        $statement->bindParam(':ProjNum', $location, PDO::PARAM_STR);
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
        <th>ProjName</th>
        <th>ProjNum</th>
        <th>ProjDesc</th>
                </tr>
            </thead>
            <tbody>
        <?php foreach ($result as $row) { ?>
            <tr>
      <td><?php echo escape($row["ProjName"]); ?></td>
        <td><?php echo escape($row["ProjNum"]); ?></td>
        <td><?php echo escape($row["ProjDesc"]); ?></td>
            </tr>
        <?php } ?>
        </tbody>
    </table>
    <?php } else { ?>
        <blockquote>No results found for <?php echo escape($_POST['ProjNum']); ?>.</blockquote>
    <?php } 
} ?> 

<h2>Find Project based on ProjNumber</h2>

<form method="post">
    <label for="ProjNum">ProjNumber</label>
    <input type="text" id="ProjNum" name="ProjNum">
    <input type="submit" name="submit" value="View Results">
</form>

<br>
<a href="index.php">Back to home</a>
</br>
<?php require "../templates/footer.php"; ?>
