# PiQUM 

**PiQuM** is a **P**latform **i**ndependent & **P**urpose **i**ntegrated **Q**uantum **U**niversal **M**achine

>Created by: ````David Lee, Teik-Hui````

>Contributed by: ````Jackie Hsiao, Li-Chieh, ````

>Acknowledgment: ````Academia Sinica````

## Structure of PiQUM:
### 1. Blog (LaBooK)
  * Crucial BDR runtimes.
  * Measurement status.

### 2. Machine
  * ALL list of Instruments based on DR affiliation.
  * Sample assignment to each available ````Queue````.
  * Wiring configuration specific for each ````Queue````.

### 3. Bridge
  * IQ Calibration

### 4. Benchmark
  * Quality factor Estimation
  * Population Estimation (Fidelity)
  * Common Fitting (Rabi, T1, T2)

### 5. Guide
  * Qubit Frequency Prediction

## The Flow of Measurement:
### 6. User
User need to register and will be granted certain level of access into the platform.

### 7. Sample
Sample will be logged for each run of measurement.

### 8. Queue
Enter the Queue after checking every details about the sample is correct & appropriate.
Each Queue can run in parallel to each others.
  * ````CHAR````: Frequency-domain measurement for basic **char**acterization of each cavities and physical qubits.
  * ````QPC````: Time-domain measurement for advanced **Q**uantum **P**rocessor **C**ontrol

### 9. Task
Each task has its own directive for respective measurement schemes.
  * ````FRESP````: Frequency Response
  * ````CWSWEEP````: Continuous Wave Sweeping
  * ````SINGLEQB````: Single-Qubit-ish pulse measurement
  * ````QUBITS````: Multiple Qubits Orchestration

### 10. Story
Automatically telling unique story for each sample based on the ````notes```` taken by user. (coming soon)

## Scripting:
### 1. Parameter & Perimeter:
  * Wiring


  * Waveform / Rhythm:
  ````
    <start> to <stop> * <steps> <' r ' or '^'> <repeat>
  ````
  > Examples:
  >> ````-3 to 3 \*600 r 300 ```` means -3, -2.999, ... 2.998, 2.999, 3 with each point repeating for 300 times.
  >>> ````-1 to  1*200 ^100 ```` means -1, -0.999, ... 0.998, 0.999, 1 with each point repeating for 100 times.

  
### 2. Pulse Sequencing:
#### 2.1 SCORE:
"Musical" score dedicated for each DAC channel to orchestrate the train of pulses.
````
ns=<period>,mhz=<'i' or 'q'>/<IF-rotation>/<mixer-module>; 
<shape-1>/<parameter-i>/.../<parameter-f>,<pulse-width>,<pulse-height>;
...
<shape-n>/<parameter-i>/.../<parameter-f>,<pulse-width>,<pulse-height>;
````
> Available Shapes: Flat, Gauss, Gaussup, Gaussdn, dGauss, dGaussup, dGaussdn

#### 2.2 R-JSON:
A JSON-format statement with the capability to Schedule, Relate and Entangle each ````SCORE```` to perform all sorts of measurements and benchmarkings.
````
{
"<parameter in SCORE>" : "<value or waveform assigned>",
"<comma-separated parameters> > <formula or function made from the comma-separated parameters>" : "0",
...
}
````