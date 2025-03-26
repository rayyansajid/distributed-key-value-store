const net = require('net');
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

let clientID = null; // Store the authenticated client ID
const client = new net.Socket();

// Function to send a request to the server
function sendRequest(command) {
    if (!clientID && !command.startsWith("AUTH")) {
        console.log("You must authenticate first using 'AUTH <client_id>'");
        return;
    }

    client.write(command);
}

// Connect to the server
client.connect(65432, '127.0.0.1', () => {
    console.log('Connected to server');
});

// Handle data received from the server
client.on('data', (data) => {
    const response = data.toString();
    console.log(`Response: ${response}`);

    // Check if authentication was successful
    if (response.startsWith("Authenticated as")) {
        clientID = response.split(" ")[2]; // Extract the client ID
        console.log(`You are now authenticated as ${clientID}`);
    }
});

// Handle connection errors
client.on('error', (err) => {
    console.error('Connection error:', err.message);
});

// Handle connection close
client.on('close', () => {
    console.log('Connection closed');
});

// Main loop for user input
console.log("Enter command (e.g., 'AUTH <client_id>', 'PUT key value', or 'GET key'):");
readline.on('line', (input) => {
    const command = input.trim();
    if (command.toLowerCase() === 'exit') {
        console.log('Exiting...');
        client.destroy();
        readline.close();
        process.exit(0);
    }
    sendRequest(command);
});