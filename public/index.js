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
    console.log('mult',data);
});

sio.on('mult2', (data) => {
    console.log('mult2',data);
});

// The sum result event, using callbacks is no longer needed
//sio.on('sum_result', (data) => {
//    console.log(data)
//})

