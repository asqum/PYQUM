# PiQUM 

**PiQuM** is a Platform independent & Purpose integrated Quantum Universal Machine (QUM)

Created by:
David Lee, Teik-Hui

Contributed by:
Jackie Hsiao, Li-Chieh

Acknowledgment:
Academia Sinica

## Structure of PiQUM:
* Blog (LaBooK)
  * Crucial BDR runtimes.
  * Measurement status.

* Machine
  * List of Instruments based on DR affiliation.

* Mission
  * Frequency Response
  * Continuous Wave Sweeping
  * Single Qubit Pulsing
  * Qubits Orchestra

## Data Collection Protocol / Principle:
* Basic dimension size determined solely by measurement tuning parameter NOT including repeat#.
  * The "resume" of measurement only works when data size is with the basis dimension size.
  * The repeating measurement could only be performed once and should not be resumed. (Scrapped to accomodate Job queueing)

## Scripting:
* 1. Parameter & Perimeter:
  * Wiring


  * Waveform / Rhythm:
  <start> to <stop> * <steps> <' r ' or '^'> <repeat>

  
* 2. Pulse Sequencing:
  * SCORE & R-JSON
  ns=<period>,mhz=<'i' or 'q'>/<IF-rotation>/<mixer-module>; 
  <shape-1>/<parameter-i>/.../<parameter-f>,<pulse-width>,<pulse-height>;
  ...
  <shape-n>/<parameter-i>/.../<parameter-f>,<pulse-width>,<pulse-height>;
