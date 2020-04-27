<?php

$serv = stream_socket_server("tcp://127.0.0.1:8100",$errno,$errstr) or die("create failed");

var_dump($errno,$errstr);
$subprocess = [];
cli_set_process_title( 'yyx-master' );
//启动固定数量的多个进程常驻内存处理来的请求
for($i=0;$i<5;$i++){
    $pid = pcntl_fork();
    echo $pid.PHP_EOL;
    if($pid == 0){
        cli_set_process_title( 'yyx-worker' );
        while (true){
            $conn = stream_socket_accept($serv);
            if($conn === false) continue;
            $request = fread($conn,1024);
            echo $request.PHP_EOL;
            $response = "hello world".PHP_EOL;
            fwrite($conn,$response);
            fclose($conn);
        }
        exit(0);
    }else{
        $subprocess[] = $pid;//管理子进程的状态
    }
}
var_dump($subprocess);
while (true){//如果没有这里，就没有master，但是tcp监听的worker依然可以正常处理,只是worker没有master来管理
    sleep(1);
}
