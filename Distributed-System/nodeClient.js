const net = require('net');

// Function to send a request to the server
function sendRequest(command) {
    // Create a TCP socket connection to the server
    const client = new net.Socket();

    // Connect to the server (replace '127.0.0.1' and 65432 if needed)
    client.connect(65432, '127.0.0.1', () => {
        console.log('Connected to server');
        // Send the command to the server
        client.write(command);
    });

    // Handle data received from the server
    client.on('data', (data) => {
        console.log(`Response: ${data.toString()}`);
        // Close the connection after receiving the response
        client.destroy();
    });

    // Handle connection errors
    client.on('error', (err) => {
        console.error('Connection error:', err.message);
    });

    // Handle connection close
    client.on('close', () => {
        console.log('Connection closed');
    });
}

// Main loop for user input
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

console.log("Enter command (e.g., 'PUT key value' or 'GET key'):");
readline.on('line', (input) => {
    const command = input.trim();
    if (command.toLowerCase() === 'exit') {
        console.log('Exiting...');
        readline.close();
        process.exit(0);
    }
    sendRequest(command);
});