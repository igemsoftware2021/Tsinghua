var timer = 1; //每一轮迭代的时间步长暂设为1
class Bacteria {
    constructor() {
        this.radius = randomNum(1.5, 2.0)
        this.xPosit = randomNum(1, 10)
        this.yPosit = randomNum(50, 200)
        do {
            this.xVel = randomNum(-1, 2)
        } while (Math.abs(this.xVel) <= 0.01) //V5修改
        do {
            this.yVel = randomNum(-0.5, 0.5)
        } while (Math.abs(this.yVel) <= 0.01) //V5修改

        this.isAdhered = this.getIsAdhered();
        this.isAlived = true; //一开始存活
        this.adheredCoefficiency = 0.02 //黏附系数，工程菌
        console.log(this.xVel+"===="+this.yVel);
    }

    getIsAdhered() {
        let a = (this.yPosit > 234); //顶上
        let b = (this.yPosit < 16); //底下
        if (a || b)
            return true;
        else
            return false;
    }

    getIsAlived() {
        let a = (this.xPosit > 800);
        if (a)
            return false;
        else
            return true;
    }

    isUnattached() {
        let a = Math.random()
        if (a < this.adheredCoefficiency) //如果<0.1，释放。10%概率释放
            return true;
        else
            return false;
    }

    isCollideLeftSide() { //V5+修改，防止卡墙
        var next_xPosit = this.xPosit + timer * this.xVel;
        if (next_xPosit <= 0) { //撞啦！
            this.xPosit = -next_xPosit; //坐标反过来
            this.xVel *= -1; //速度也反过来
        }
    }

    moving() { //迭代
        if (!this.isAdhered) { //没有黏附
            //Moving
            this.xPosit += timer * this.xVel;
            this.yPosit += timer * this.yVel;
            //isAdhering
            this.isAdhered = this.getIsAdhered();
            //isAlive
            this.isAlived = this.getIsAlived();

            this.isCollideLeftSide() //处理可能的撞左边卡墙情形，V5+修改


        } else { //黏附了！
            if (this.isUnattached()) { //解黏附了！
                //console.log("Unattached!")
                this.xVel = randomNum(-1, 2) //(-0.4, 0.8)?
                //this.yVel = randomNum(-0.5, 0.5) //速度重置
                if (this.yPosit > 234) { //黏在下面那一层
                    this.yVel = randomNum(-0.5, -0.1) //(-0.2, -0.04)?
                    //console.log(this.yVel)
                    this.yPosit = 232
                }
                if (this.yPosit < 16) { //黏在顶上了
                    this.yVel = randomNum(0.1, 0.5) //(0.04, 0.2)?
                    this.yPosit = 18
                }
                this.isAdhered = false;
            }
        }
    }

    draw(ctx) {
        ctx.beginPath()
        ctx.arc(this.xPosit, this.yPosit, this.radius, 0, 2 * Math.PI)
        ctx.closePath()
        ctx.fillStyle = "red";
        ctx.fill()
    }
}

class wtBacteria extends Bacteria {
    constructor() {
        super();
        //Bacteria.apply(this); //???
        this.adheredCoefficiency = 0.05; //V9修改
    }
    draw(ctx) {
        ctx.beginPath()
        ctx.arc(this.xPosit, this.yPosit, this.radius, 0, 2 * Math.PI)
        ctx.closePath()
        ctx.fillStyle = "green";
        ctx.fill()
    }

    division() {
        var newWTBacteria = new wtBacteria();
        newWTBacteria.xPosit = this.xPosit
        newWTBacteria.yPosit = this.yPosit
        return newWTBacteria;
    }
}

class intestinalBacteria extends Bacteria {
    constructor() {
        super();
        //Bacteria.call(this);
        this.round = count; //V10
        this.adheredCoefficiency =0.02; //V5修改
    }

    division() {
        let newIntestinalBacteria = new intestinalBacteria();
        newIntestinalBacteria.round = count;
        newIntestinalBacteria.xPosit = this.xPosit
        newIntestinalBacteria.yPosit = this.yPosit
        return newIntestinalBacteria;
    }
}