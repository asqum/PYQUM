let xmax = 1250;
let numTraces = 1;
let traces = [];
let x = [];

for (let i = 0; i < numTraces; i++) {
  x[i] = [];
  for(let j = 0; j < xmax; j++) {
    x[i].push(j);
  }
  traces.push({
    x: x[i],
    type: "scattergl",
    mode: "markers"
  });
}

var fps_display = document.querySelector("#fps");
setInterval(function() { 
  let amp = 10*Math.random() + 1;
  for (let i = 0; i < numTraces; i++) {
    let y = [];
    for (let j = 0; j < traces[i].x.length - 1; j++) {
      y[j] = amp*Math.random();
    }
    traces[i].y = y;
    traces[i].name = (1000000*Math.random()).toString();
  }
  let layout = {
    xaxis: { range: [0, xmax] },
    yaxis: { range: [0, 11] }
  }
  Plotly.react('plot', traces, layout);
  // fps_display.update(numTraces * xmax);
}, 1);