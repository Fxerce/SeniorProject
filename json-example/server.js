const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static('public'));  // Serve static files from the "public" folder

// Endpoint to handle form submission
app.post('/submit', (req, res) => {
    const newData = req.body;

    // Read the existing data from the JSON file
    fs.readFile(path.join(__dirname, 'data.json'), 'utf-8', (err, data) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Error reading file' });
        }

        const jsonData = data.length ? JSON.parse(data) : [];
        jsonData.push(newData);

        // Write the updated data back to the JSON file
        fs.writeFile(path.join(__dirname, 'data.json'), JSON.stringify(jsonData, null, 2), (err) => {
            if (err) {
                console.error(err);
                return res.status(500).json({ message: 'Error writing file' });
            }
            res.json({ message: 'Data saved successfully' });
        });
    });
});

// Endpoint to display data
app.get('/display', (req, res) => {
    fs.readFile(path.join(__dirname, 'data.json'), 'utf-8', (err, data) => {
        if (err) {
            console.error(err);
            return res.status(500).send('Error reading file');
        }

        const jsonData = data.length ? JSON.parse(data) : [];
        res.json(jsonData);  // Send the data as JSON
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
