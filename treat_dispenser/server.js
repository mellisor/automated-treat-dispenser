const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;

const command = '{python_path} {path_to_motor_lib}/motor.py 256 -d 45';

app.get('/', (req, res) => {
	exec(command, (err, stdout, stderr) => {
		res.send();
	});
});

app.listen(port);
