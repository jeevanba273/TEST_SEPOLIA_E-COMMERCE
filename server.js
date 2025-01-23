const express = require('express');
const { exec, spawn } = require('child_process');
const path = require('path');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Create HTTP server
const server = http.createServer(app);

// WebSocket server
const wss = new WebSocket.Server({ server, path: '/ws' });

wss.on('connection', ws => {
    console.log('WebSocket connection established.');
    let scriptProcess = null;

    ws.on('message', message => {
        try {
            if (message === 'STOP_SCRIPT') {
                console.log('Received stop request');
                if (scriptProcess) {
                    scriptProcess.kill();
                    console.log('Script process killed');
                    ws.send("Script stopped by user");
                    ws.send("SCRIPT_FINISHED");
                } else {
                    console.log('No script process to stop');
                    ws.send("No active script to stop");
                }
                return;
            }

            const data = JSON.parse(message);
            const { scriptId, params } = data;

            let scriptPath;
            let command;

            switch (scriptId) {
                case 1:
                    if (!params[0]) {
                        ws.send("Error: Infura Project ID is required for Script 1");
                        ws.send("SCRIPT_FINISHED");
                        return;
                    }
                    console.log(`Running script ${scriptId} with Infura Project ID: ${params[0]}`);
                    scriptPath = path.join(__dirname, 'script1.py');
                    command = `python "${scriptPath}" "${params[0]}"`;
                    break;
                case 2:
                    console.log(`Running script ${scriptId}`);
                    scriptPath = path.join(__dirname, 'script2.py');
                    command = `python "${scriptPath}"`;
                    break;
                case 3:
                case 5:
                case 6:
                    if (params.length < 2) {
                        ws.send(`Error: Both Infura Project ID and Wallet Address are required for Script ${scriptId}`);
                        ws.send("SCRIPT_FINISHED");
                        return;
                    }
                    console.log(`Running script ${scriptId} with Infura Project ID: ${params[0]} and Wallet Address: ${params[1]}`);
                    scriptPath = path.join(__dirname, `script${scriptId}.py`);
                    command = `python "${scriptPath}" "${params[0]}" "${params[1]}"`;
                    break;
                case 4:
                    if (params.length < 4) {
                        ws.send("Error: Infura Project ID, Sender Address, Private Key, and Receiver Address are required for Script 4");
                        ws.send("SCRIPT_FINISHED");
                        return;
                    }
                    console.log(`Running script 4 with Infura Project ID: ${params[0]}, Sender Address: ${params[1]}, Private Key: ${params[2]}, Receiver Address: ${params[3]}`);
                    scriptPath = path.join(__dirname, 'script4.py');
                    command = `python "${scriptPath}" "${params[0]}" "${params[1]}" "${params[2]}" "${params[3]}"`;
                    break;
                case 7:
                    if (params.length < 2) {
                        ws.send(`Error: Both Infura Project ID and Wallet Address are required for Script ${scriptId}`);
                        ws.send("SCRIPT_FINISHED");
                        return;
                    }
                    console.log(`Running script ${scriptId} with Infura Project ID: ${params[0]} and Wallet Address: ${params[1]}`);
                    scriptPath = path.join(__dirname, `script${scriptId}.py`);
                    scriptProcess = spawn('python', [scriptPath, params[0], params[1]]);

                    scriptProcess.stdout.on('data', (data) => {
                        ws.send(data.toString());
                    });

                    scriptProcess.stderr.on('data', (data) => {
                        ws.send(`Error: ${data.toString()}`);
                    });

                    scriptProcess.on('close', (code) => {
                        if (code !== 0) {
                            ws.send(`Script finished with code ${code}`);
                        }
                        ws.send("SCRIPT_FINISHED");
                        scriptProcess = null;
                    });

                    return;
                case 8:
                    if (params.length < 3) {
                        ws.send("Error: Infura Project ID, Private Key, and Receiver Address are required for Script 8");
                        ws.send("SCRIPT_FINISHED");
                        return;
                    }
                    console.log(`Running script 8 with Infura Project ID: ${params[0]}, Private Key: ${params[1]}, Receiver Address: ${params[2]}`);
                    scriptPath = path.join(__dirname, 'script8.py');
                    command = `python "${scriptPath}" "${params[0]}" "${params[1]}" "${params[2]}"`;
                    break;
                default:
                    ws.send("Error: Unknown script ID");
                    ws.send("SCRIPT_FINISHED");
                    return;
            }

            if (scriptId !== 7) {
                scriptProcess = exec(command);

                scriptProcess.stdout.on('data', data => {
                    ws.send(data.toString());
                });

                scriptProcess.stderr.on('data', data => {
                    ws.send(`Error: ${data.toString()}`);
                });

                scriptProcess.on('close', code => {
                    if (code !== 0) {
                        ws.send(`Script finished with code ${code}`);
                    }
                    ws.send("SCRIPT_FINISHED");
                    scriptProcess = null;
                });

                scriptProcess.on('error', err => {
                    ws.send(`Error: ${err.message}`);
                    ws.send("SCRIPT_FINISHED");
                    scriptProcess = null;
                });
            }
        } catch (e) {
            ws.send(`Error: ${e.message}`);
            ws.send("SCRIPT_FINISHED");
        }
    });

    ws.on('close', () => {
        console.log('WebSocket connection closed.');
        if (scriptProcess) {
            scriptProcess.kill();
            console.log('Script process killed due to WebSocket closure');
        }
    });

    ws.on('error', error => {
        console.error('WebSocket error:', error);
    });
});

// Start the server
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});