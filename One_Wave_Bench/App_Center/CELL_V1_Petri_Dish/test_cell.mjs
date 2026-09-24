import {CellV1} from "./cell.js";
function assert(x,msg){if(!x)throw new Error(msg)}
const c=new CellV1();
for(let i=0;i<20;i++)c.update({a:1,b:1,c:1});
assert(c.state==="UP","positive differential should reach UP");
for(let i=0;i<60;i++)c.update({a:0,b:0,c:0});
assert(["UP","STAY"].includes(c.state),"hysteresis should retain then relax");
for(let i=0;i<40;i++)c.update({a:-1,b:-1,c:-1});
assert(c.state==="DOWN","negative differential should reach DOWN");
console.log("CELL_PETRI_DISH_TEST_OK");