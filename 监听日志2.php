<?php
// 设置默认时区为上海
date_default_timezone_set('Asia/Shanghai');

// 获取访问者的IP地址
$ip = $_SERVER["REMOTE_ADDR"];

// 获取访问者要访问的文件名
$filename = $_SERVER['PHP_SELF'];

// 获取访问者请求的参数
$parameter = $_SERVER["QUERY_STRING"];

// 获取请求方法（GET、POST等）
$method = $_SERVER['REQUEST_METHOD'];

// 获取请求的URI
$uri = $_SERVER['REQUEST_URI'];

// 获取当前时间并格式化
$time = date('Y-m-d H:i:s', time());

// 获取POST请求的原始数据
$post = file_get_contents("php://input", 'r');

// 其他你想记录的信息
$others = '...其他你想得到的信息...';

// 构建日志记录信息
$logadd = 'Visit Time：' . $time . ' ' .
          'Visit IP：' . $ip . "\r\n" .
          'RequestURI：' . $uri . ' ' . $parameter . ' ' .
          'RequestMethod：' . $method . "\r\n";

// 日志文件路径（建议使用绝对路径）
$logfile = 'log.txt';

// 打开日志文件（追加模式）
$fh = fopen($logfile, "a+");

if ($fh) {
    // 写入日志内容
    fwrite($fh, $logadd);

    // 写入COOKIE信息
    fwrite($fh, print_r($_COOKIE, true) . "\r\n");

    // 写入POST数据
    fwrite($fh, $post . "\r\n");

    // 写入其他信息
    fwrite($fh, $others . "\r\n");

    // 关闭文件句柄
    fclose($fh);
} else {
    // 日志文件打开失败，记录错误信息
    error_log("Failed to open log file: $logfile");
}
?>
