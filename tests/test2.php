<?php

$aa=$bb+$cc*2;//1
$dd=$_GET['dd'];//2
echo $dd;//3

$ee=1;//4

//-------b0

while($ee<-3){// 
    $ee=fun($ee);//
}

//------- b1

if($ee==4){//---b2
    $xy="xux";


eval('echo $aa;');
//---b3
}

else{
    $xy="xu1";
    print_r($xy);
}

$xy="xu00001";//---b4


function fun($ff){
    return ++$ff;
}
//b5

/**
 * start->b0->b1->b2->b3-b4------|
 *                |              |--->end
 *                ->b4-----------|
 * 
 * 
 * 
 * 
 */

// BasicBlock: BB0
// Predecessors: []
// Successors: ['BB1']       
// BasicBlock: BB1
// Predecessors: ['BB0']     
// Successors: ['BB2']       
// BasicBlock: BB2
// Predecessors: ['BB1']     
// Successors: ['BB3', 'BB5']
// BasicBlock: BB3
// Predecessors: ['BB2']     
// Successors: []
// BasicBlock: BB5
// Predecessors: ['BB2']     
// Successors: ['BB6']       
// BasicBlock: BB6
// Predecessors: ['BB5']     
// Successors: []