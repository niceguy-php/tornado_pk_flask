<?php

$client = stream_socket_client("tcp://127.0.0.1:8100",$errno,$errstr) or die("create failed");

if(!$client){
    var_dump($errstr,$errno);
}else{

    fwrite($client,"nice");

    while (!feof($client)){
        echo fgets($client,1024);
    }

    fclose($client);
}