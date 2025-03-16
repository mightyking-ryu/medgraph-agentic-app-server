<?php

function generate_uuid() {
    return bin2hex(random_bytes(16));
}

?>