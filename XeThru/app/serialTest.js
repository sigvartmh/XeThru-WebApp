var SerialPort = require("serialport").SerialPort
var serialPort = new SerialPort("COM10", {
  baudrate: 115200
});

serialPort.on("open", function () {
  console.log('open');
  serialPort.on('data', function(data) {
    console.log('data received: ' + data);
    
    str = String(data)
    console.log("1st part of data string: "+ str[0])
    if(str[0] === 'i'){
    	var v = parseInt(str.match(/\d+/)[0]);
    	console.log('Recived i data: ' + v);
    }
    console.log('data type:' + typeof data);
  });
});