<?php
function foo($x, $y) {
    return $x * $y;
}

$a = 1;
$b = 2;
$c = 0;

$c=$a+$b;
while ($a < 10) {
    $c = $a + $b;
    if ($c > 5) {
        $d = foo($a, $b);
        echo "Result: $d\n";
    }
    $a += 1;
}

$a=$a+1;
?>


<!-- #如果一开始没有label就创建一个虚拟label,将内容放入
#两个bb之间是有前后继关系的
#遇到if，要将jump_label的标签当作后继
#以label名当作bb的名字，以方便前后继的维护
#如果label为GOTO，那么这个bb的后继应该为它的jump_label,并且取消它和下一个bb的前后继关系 -->