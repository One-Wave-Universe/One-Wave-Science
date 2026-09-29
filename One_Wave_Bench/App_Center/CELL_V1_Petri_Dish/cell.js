export class CellV1 {
  constructor() {
    this.field = 0;
    this.void = 0;
    this.lean = 0;
    this.state = "STAY";
    this.memory = 0;
    this.reinjection = 0;
    this.enter = 0.55;
    this.leave = 0.25;
    this.hold = false;
    this.history = [];
  }

  clamp(x,a=-1,b=1){ return Math.max(a,Math.min(b,x)); }

  update(input) {
    const a = Number(input.a || 0);
    const b = Number(input.b || 0);
    const c = Number(input.c || 0);
    const fieldDrive = this.clamp((Math.max(a,0)+Math.max(b,0)+Math.max(c,0))/3,0,1);
    const voidDrive  = this.clamp((Math.max(-a,0)+Math.max(-b,0)+Math.max(-c,0))/3,0,1);

    this.field = 0.72*this.field + 0.28*fieldDrive;
    this.void  = 0.72*this.void  + 0.28*voidDrive;

    const differential = this.field - this.void + 0.18*this.memory + 0.12*this.reinjection;
    this.lean = this.clamp(0.68*this.lean + 0.32*differential);

    if (this.hold) {
      if (Math.abs(this.lean) <= this.leave) this.hold = false;
    } else if (Math.abs(this.lean) >= this.enter) {
      this.hold = true;
    }

    if (this.hold) this.state = this.lean > 0 ? "UP" : "DOWN";
    else this.state = "STAY";

    const target = this.state === "UP" ? 1 : this.state === "DOWN" ? -1 : 0;
    this.reinjection = this.clamp(0.65*this.reinjection + 0.35*target);
    this.memory = this.clamp(0.92*this.memory + 0.08*target);

    const snap = {
      a,b,c,field:this.field,void:this.void,lean:this.lean,
      state:this.state,memory:this.memory,reinjection:this.reinjection,
      hold:this.hold
    };
    this.history.push(snap);
    if (this.history.length > 240) this.history.shift();
    return snap;
  }
}
