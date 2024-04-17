<?php
// Read data from file
$fileContents = file_get_contents('convert.txt');

// Split contents into lines
$lines = explode("\n", $fileContents);

// Initialize array to store parsed data
$data = [];

// Parse each line
foreach ($lines as $line) {
    // Split line into components
    $parts = explode(" - ", $line);

    // Extract relevant information
    $timestamp = substr($parts[0], 0, 19);
    $speed = (float)substr($parts[1], strpos($parts[1], ": ") + 2);
    $coordinates = explode(", ", $parts[2]);
    $latitude = (float)$coordinates[0];
    $longitude = (float)$coordinates[1];

    // Add to data array
    $data[] = [
        'timestamp' => $timestamp,
        'speed' => $speed,
        'latitude' => $latitude,
        'longitude' => $longitude
    ];
}

// Return data as JSON
header('Content-Type: application/json');
echo json_encode($data);
?>
