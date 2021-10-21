class BacteriaSet {

    constructor() {
        this.time = 0;
        this.roundCounter = [];
        this.mySet = [];
        this.numCounter = [];
        this.initiateNumCounter(60); // 按requestAnimationFrame中1s/60次的频率这里的时滞是1s
    }

    initiateNumCounter(lag) {
        for (var i = 1; i < lag; i++) {
            this.numCounter.push(0);
        }
    }

    applyDivision(numberToChange) {
        for (var i = 0; i < numberToChange; i++) {
            this.mySet.push(this.mySet[randomNumInt(0, this.mySet.length - 1)].division());
            this.bacteriaNumber += 1;
        }
    }

    applyDeath(numberToChange) {
        for (var i = 0; i > numberToChange; i--) {
            this.mySet.splice(randomNumInt(0, this.mySet.length - 1), 1);
            this.bacteriaNumber -= 1;
        }
    }

    applyEmigration() {
        for (var i = this.mySet.length - 1; i >= 0; i--) {
            if (this.mySet[i].isAlived == false) {
                this.mySet.splice(i, 1);
                this.bacteriaNumber -= 1;
            }
        }
    }

    iterateByOneStep() {
        // 先计算当前时间下菌的数量如何改变
        var currentBacteriaNumber = this.mySet.length;
        var numberToChange = this.bacteriaNumber - currentBacteriaNumber;
        // console.log(numberToChange); // test
        if (numberToChange > 0) { this.applyDivision(numberToChange); } else if (numberToChange < 0) { this.applyDeath(numberToChange); }
        // 菌数量改变后对每个菌进行一步迭代
        for (var i = 0; i < this.mySet.length; i++) {
            this.mySet[i].moving();
            this.mySet[i].draw(ctx)
        }
        this.applyEmigration();
        // 时间推移
        this.numCounter.push(this.bacteriaNumber);
        this.time += timer;
        //this.calculateBacteriaNumber();
    }
}

class wtBacteriaSet extends BacteriaSet {

    constructor() {
        super();
        this.bacteriaNumber = 200; // 暂定初始菌量是200
        for (var i = 0; i < this.bacteriaNumber; i++) {
            this.mySet.push(new wtBacteria());
        }
        this.r = 0.000001; //V5修改
    }

    calculateBacteriaNumber(anotherSet) {
        var wtNum = this.numWithLag;
        var intestinalNum = anotherSet.numWithLag;
        var slope = this.r * this.mySet.length * (1 - (wtNum + intestinalNum) / 500);
        this.bacteriaNumber = this.mySet.length + slope;
    }

}

class intestinalBacteriaSet extends BacteriaSet {

    constructor() {
        super();
        this.bacteriaNumber = 0; // 暂定初始菌量是0
        //V5修改
        for (var i = 0; i < this.bacteriaNumber; i++) {
            this.mySet.push(new intestinalBacteria());
        }
        this.r = 0.000001; //V5修改
    }

    //计算当前工程菌中每一轮的数量
    calculateEachRoundBacteria() {
        this.roundCounter.length=0;
        for (var i = 0; i < count; i++) {
            this.roundCounter.push(0);
        }
        for (var i = 0; i < this.mySet.length; i++) {
            for (var j = 1; j <= count; j++) {
                if(this.mySet[i].round==j) {
                    this.roundCounter[j-1]+=1;
                }
            }
        }
    }

    calculateBacteriaNumber(anotherSet) {
        var wtNum = anotherSet.numWithLag;
        var intestinalNum = this.numWithLag;
        var slope = this.r * this.mySet.length * (1 - (wtNum + intestinalNum) / 500);
        this.bacteriaNumber = this.mySet.length + slope;
    }

    Eat_EngineeredBacterial() { //V5修改

        for (var i = 0; i < hua; i++) { //V6：集中释放
            let PillBacteria = new intestinalBacteria();
            PillBacteria.xPosit = randomNum(1, 10)
            PillBacteria.yPosit = randomNum(100, 150)
            intestinalSet.mySet.push(PillBacteria);
        }
        
        this.bacteriaNumber = this.bacteriaNumber + hua;
    }

}