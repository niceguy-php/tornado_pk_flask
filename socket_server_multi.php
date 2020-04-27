<?php
ini_set('error_reporting', E_ALL);
ini_set('display_errors', 'On');
$serv = stream_socket_server("tcp://127.0.0.1:8100",$errno,$errstr) or die("create failed");

var_dump($errno,$errstr);
$subprocess = [];
cli_set_process_title( 'yyx-master' );

//来一个请求就fork一个子进程进行处理处理完成子进程退出，会有c10k问题,并发上w之后需要fork上w个子进程
while (true){
    $conn = stream_socket_accept($serv);
    $pid = pcntl_fork();
    if($pid == 0){
        cli_set_process_title( 'yyx-worker' );
        if ($conn === false) continue;
        $request = fread($conn,1024);
        echo $request.PHP_EOL;
        $response = "hello world".PHP_EOL;
        fwrite($conn,$response);
        fclose($conn);
        exit(0);
    }

}
