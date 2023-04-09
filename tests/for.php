<?php
for ($i = 0; $i < 10; $i++) {
    if ($i === 5) {
      break; // 当$i等于5时跳出循环
    }
    echo $i . " ";
  }

  
  $i = 0;
  while ($i < 10) {
    if ($i === 5) {
      break; // 当$i等于5时跳出循环
    }
    echo $i . " ";
    $i++;
  }
?>
  