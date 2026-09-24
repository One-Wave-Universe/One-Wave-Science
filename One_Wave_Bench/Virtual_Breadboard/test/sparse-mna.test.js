'use strict';
const assert = require('assert');
const CE = require('../js/circuit.js');
const { Circuit, solveLinear, solveSparseLinear, makeSparseMatrix, sparseNnz, sparseToDense } = CE;
let n=0;
function ok(name,v,msg=''){ n++; assert(v, `${name}${msg?': '+msg:''}`); console.log(`PASS [${name}]${msg?' -- '+msg:''}`); }
function near(name,a,b,tol=1e-10){ n++; assert(Math.abs(a-b)<=tol, `${name}: ${a} vs ${b}`); console.log(`PASS [${name}]`); }
console.log('=== Virtual Breadboard sparse MNA qualification ===');

// Independent linear algebra check: a 200x200 diagonally-dominant tridiagonal
// system is genuinely sparse and must match the preserved dense reference solver.
const size=200;
const A=makeSparseMatrix(size);
const b=new Array(size).fill(0).map((_,i)=>1 + (i%7)*0.1);
for(let i=0;i<size;i++){
  A[i][i]=4;
  if(i>0) A[i][i-1]=-1;
  if(i<size-1) A[i][i+1]=-1;
}
const nnz=sparseNnz(A);
ok('sparse-storage-is-subquadratic', nnz < size*4, `nnz=${nnz} dense=${size*size}`);
const denseX=solveLinear(sparseToDense(A,size),b);
const sparseSolved=solveSparseLinear(A,b);
for(let i=0;i<size;i++) near(`dense-sparse-x-${i}`,sparseSolved.x[i],denseX[i],1e-10);
ok('sparse-factorization-reports-nnz', sparseSolved.stats.initialNnz===nnz, JSON.stringify(sparseSolved.stats));
ok('sparse-factorization-bounded-fill', sparseSolved.stats.peakNnz < size*8, JSON.stringify(sparseSolved.stats));

// Real MNA check: a large resistor ladder crosses the auto threshold and must
// give the same electrical answer as the dense reference path.
const components=[{id:'V1',type:'battery',a:'n0',b:'gnd',value:10}];
for(let i=0;i<100;i++) components.push({id:`R${i}`,type:'resistor',a:`n${i}`,b:`n${i+1}`,value:1000});
components.push({id:'Rload',type:'resistor',a:'n100',b:'gnd',value:1000});
const elements={wires:[],components};
const denseCircuit=new Circuit();
const sparseCircuit=new Circuit();
const autoCircuit=new Circuit();
const dense=denseCircuit.solve(elements,1e-3,25,{linearSolver:'dense'});
const sparse=sparseCircuit.solve(elements,1e-3,25,{linearSolver:'sparse'});
const auto=autoCircuit.solve(elements,1e-3,25,{linearSolver:'auto'});
ok('dense-large-ladder-converges',dense.solver.converged,JSON.stringify(dense.solver));
ok('sparse-large-ladder-converges',sparse.solver.converged,JSON.stringify(sparse.solver));
ok('auto-large-ladder-converges',auto.solver.converged,JSON.stringify(auto.solver));
ok('dense-path-reported',dense.solver.linearSolver==='dense',JSON.stringify(dense.solver));
ok('sparse-path-reported',sparse.solver.linearSolver==='sparse',JSON.stringify(sparse.solver));
ok('auto-selects-sparse-for-large-matrix',auto.solver.linearSolver==='sparse',JSON.stringify(auto.solver));
ok('matrix-is-actually-sparse',sparse.solver.matrixDensity < 0.05, `density=${sparse.solver.matrixDensity}`);
for(const node of ['n0','n1','n25','n50','n75','n100']){
  const vd=dense.voltages.get(dense.uf.find(node));
  const vs=sparse.voltages.get(sparse.uf.find(node));
  near(`ladder-dense-sparse-${node}`,vs,vd,1e-9);
}
near('auto-matches-explicit-sparse',auto.voltages.get(auto.uf.find('n50')),sparse.voltages.get(sparse.uf.find('n50')),1e-10);
let threw=false;
try { new Circuit().solve(elements,1e-3,25,{linearSolver:'bogus'}); } catch(e){ threw=/unknown linearSolver/.test(String(e)); }
ok('invalid-linear-solver-rejected',threw);
console.log(`=== ALL ${n} SPARSE-MNA CHECKS PASSED ===`);
