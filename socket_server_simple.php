<?php

$serv = stream_socket_server("tcp://127.0.0.1:8100",$errno,$errstr) or die("create failed");

var_dump($errno,$errstr);
$subprocess = [];


while (true){
    $conn = stream_socket_accept($serv);
    if($conn === false) continue;
    $request = fread($conn,1024);
    echo $request.PHP_EOL;
    $response = "hello world";
    fwrite($conn,$response);
    fclose($conn);
}
exit(0);
