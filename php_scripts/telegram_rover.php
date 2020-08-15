<?php
echo file_get_contents('http://172.27.220.5:8823/move?track_left='.$_GET['track_left'].'&track_right='.$_GET['track_right'].'&delay='.$_GET['delay'].'&speed='.$_GET['speed']);
?>
