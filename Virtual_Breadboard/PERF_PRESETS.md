# Perfboard layout presets (apply if missing)

`index.html` already lists `1perf` / `1perf-small`. Wire them in JS:

## simulate.js
```diff
--- a/Virtual_Breadboard/simulate.js
+++ b/Virtual_Breadboard/simulate.js
@@ -59,6 +59,8 @@
   '4small': [{ size: 'small' }, { size: 'small' }, { size: 'small' }, { size: 'small' }],
   '1large1small': [{ size: 'large' }, { size: 'small' }],
   '1large2small': [{ size: 'large' }, { size: 'small' }, { size: 'small' }],
+  '1perf': [{ size: 'large', kind: 'perf' }],
+  '1perf-small': [{ size: 'small', kind: 'perf' }],
 };
 
 function readInput() {
```

## js/app.js
```diff
--- a/Virtual_Breadboard/js/app.js
+++ b/Virtual_Breadboard/js/app.js
@@ -9,6 +9,9 @@
     '4small': [{ size: 'small' }, { size: 'small' }, { size: 'small' }, { size: 'small' }],
     '1large1small': [{ size: 'large' }, { size: 'small' }],
     '1large2small': [{ size: 'large' }, { size: 'small' }, { size: 'small' }],
+    // Perfboard: same hole geometry; every pad is its own cellId.
+    '1perf': [{ size: 'large', kind: 'perf' }],
+    '1perf-small': [{ size: 'small', kind: 'perf' }],
   };
   let board = Board.build(LAYOUT_PRESETS['1large']);
   const circuit = new CircuitEngine.Circuit();
```

Without these two-line preset adds, choosing Perfboard in the UI throws Unknown layout.
API works regardless: `Board.build([{ size: 'large', kind: 'perf' }])`.
