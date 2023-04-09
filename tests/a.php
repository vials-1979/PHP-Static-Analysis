<?php

// 定义一个简单的函数
function sayHello($name) {
    echo "Hello, $name!";
}

// 调用函数
sayHello("John");

// 定义一个简单的类
class Car {
    public $make;
    public $model;

    public function __construct($make, $model) {
        $this->make = $make;
        $this->model = $model;
    }

    public function getInfo() {
        return "This car is a {$this->make} {$this->model}.";
    }
}

// 实例化一个 Car 对象
$myCar = new Car("Honda", "Civic");

// 调用类的方法
echo $myCar->getInfo();



// 声明一个变量
$message = "Hello, World!";

$add=$message."asdada";

// 输出变量值
echo $message;

// 使用条件语句
if (strlen($message) > 10) {
    echo "The message is long.";
} else {
    echo "The message is short.";
}

// 循环语句
for ($i = 0; $i < 10; $i++) {
    echo $i . " ";
}


?>
