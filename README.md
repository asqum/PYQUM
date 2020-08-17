# PYQUM 

**PyQuM** is an instrumentation and abstraction platform for Quantum Universal Machine (QUM)

Created by:
David Lee, Teik-Hui

Acknowledgement:
Academia Sinica

## Added Features in this version:
* User-specific mission based on sample.
* Time-domain measurement using basic Square-pulse
* Compact parameters loading using library packing for C-orders

## Structure in this version:
* Blog (LaBooK)
  * DR Cooling Process
  * BDR Cooldown Start-Days
  * Best BDR condition
  * Mixture Return Procedure (MRP)
  * RF Switch Operation
  * Measurement Plan
  * SOP Updates
  * DR Wiring status
  * ENA 5071C status

* Machine
  * ALL: Status update for PSGV, AWG
  * DC: YOKOGAWA, KEITHLEY, AMPLIFIER (I-Vb)
  * BDR: HISTORY 
  * NA: E5071, PNA
  * SG: PSGV, PSGA, ESG, MXG
  * AWG (M933X)
  * VSA (M9392A)

* Mission
  * Frequency Response
  * Continuous Wave Sweeping
  * Square-Pulse in-out measurement

## Data Collection Protocol / Principle:
* Basic dimension size determined solely by measurement tuning parameter NOT including repeat#.
  * The "resume" of measurement only work when datasize is with the basiz dimension size.
  * The repeating measurement could only be performed once and should not be resumed.

  
