function randomNum(minNum, maxNum) { //生成[minNum,maxNum]随机数
    switch (arguments.length) {
        case 1:
            return parseFloat(Math.random() * minNum, 10);
            break;
        case 2:
            return parseFloat(Math.random() * (maxNum - minNum) + minNum, 10);
            break;
        default:
            return 0;
            break;
    }
}

function randomNumInt(minNum, maxNum) { //生成[minNum,maxNum]随机整数
    switch (arguments.length) {
        case 1:
            return parseInt(Math.random() * minNum + 1, 10);
            break;
        case 2:
            return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
            break;
        default:
            return 0;
            break;
    }
}

function reStart() {
    window.requestAnimationFrame(drawFrame, canvas)
    canvas.height = canvas.height // 清空画布
}