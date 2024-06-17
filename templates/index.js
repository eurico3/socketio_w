const sio = io();

sio.on('connect', () => {
    console.log('connected');
    sio.emit('sum', {number : [1,2]}, (result) => {
        console.log('Callback result:',result)
    })
});

sio.on('disconnect', () => {
    console.log('disconnected');
});

sio.on('mult', (data) => {
    console.log('1526 mult',data);
    document.getElementById('content3').innerHTML = data.value;
});

sio.on('mult2', (data) => {
    console.log('mult2',data);
    document.getElementById('content').innerHTML = data.value;
    document.getElementById('content2').innerHTML = data.value+8;
});


sio.on('updateData', (data) => {
    console.log('updateData',data);
    document.getElementById('content4').innerHTML = data;
    //document.getElementById('content2').innerHTML = data.value+8;
});

// The sum result event, using callbacks is no longer needed
//sio.on('sum_result', (data) => {
//    console.log(data)
//})
