<?php
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Methods: GET, OPTIONS, POST");
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
set_time_limit(20);


$link=$_POST"curl"];
$query='./phispy "'.$link.'"';
$cmd = escapeshellcmd($query);
$output = shell_exec($cmd);
echo $output;
?>
