using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using KeysightSD1;
//using System.Threading;

namespace TestLauncher
{
    public partial class Form1 : Form
    {
        // Declare private variables
        private SD_AOU moduleAOU;
        private int nChannel, nChannel2;
        private int pause;

        public Form1()
        {
            InitializeComponent();

            // Create the AOU module object
            moduleAOU = new SD_AOU();

            // Initialize private variables 
            nChannel = 0;
            nChannel2 = 2;

            // Disable controls which need an open module to work
            groupBoxTests.Enabled = false;
        }

        // Function to encapsulate output operations "console" like
        private void printToConsole(string txt)
        {
            textBoxOutput.Text += txt + "\r\n";
        }

        // Function to clear the "console"
        private void clearConsole()
        {
            textBoxOutput.Text = "";
        }


        // Execute a pause - allow to run scripts and pauses while refreshing the UI (not the most appropiate/elegant)
        // the paused is executed while the variable pause is zero
        private void runPause()
        {
            pause = 0;

            while (pause == 0)
                Application.DoEvents();
        }

        // This button release the pause
        private void buttonContinue_Click(object sender, EventArgs e)
        {
            pause = 1;
        }

        // Also release the pause before closing the program
        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            pause = 1;
        }


        private void buttonOpen_Click(object sender, EventArgs e)
        {
            int status;

            if (moduleAOU.isOpen() == false) //Check if the module is not already opened
            {
                status = moduleAOU.open(textBoxName.Text, (int)numericUpDownChassis.Value, (int)numericUpDownSlot.Value);

                if (status > 0)
                {
                    // Module opened succesfully
                    textBoxStatus.Text = "Module Opened (" + status.ToString() + ")";
                    groupBoxTests.Enabled = true;
                }
                else
                {
                    //Error open module (name or slot must be wrong)
                    textBoxStatus.Text = "Open Error: " + status.ToString();
                    groupBoxTests.Enabled = false;
                }
            }
            else
                textBoxStatus.Text = "Module already opened";
        }

        private void buttonClose_Click(object sender, EventArgs e)
        {
            //Check if the module is opened before trying to close it
            if (moduleAOU.isOpen() == true)
            {

                groupBoxTests.Enabled = false;

                int status = moduleAOU.close();

                textBoxStatus.Text = "Module Closed (" + status.ToString() + ")";
            }
            else
            {
                textBoxStatus.Text = "Close Error: No module opened";
            }
        }

        private void numericUpDownChannel_ValueChanged(object sender, EventArgs e)
        {
            // Initialize the channel variables used by the demo scripts
            nChannel = (int)numericUpDownChannel.Value;
            nChannel2 = (int)numericUpDownChannel2.Value;
        }

        private void buttonTestWaveformTrigger_Click(object sender, EventArgs e)
        {

            clearConsole();

            // Create a waveform object in PC RAM from waveform file
            SD_Wave wave1 = new SD_Wave("..\\..\\..\\..\\..\\..\\..\\Waveforms\\Triangular.csv");
            SD_Wave wave2 = new SD_Wave("..\\..\\..\\..\\..\\..\\..\\Waveforms\\Gaussian.csv");
            if(wave1.getStatus()<0 || wave2.getStatus()<0)
            {
                printToConsole("Error opening waveform File");
                return;
            }

            int nWave1 = 0;
            int nWave2 = 1;

            // Erase all waveforms from module memory and load waveforms waveId1 and waveId2 in position nWave1 and nWave2
            moduleAOU.waveformFlush();
            moduleAOU.waveformLoad(wave1,nWave1);
            moduleAOU.waveformLoad(wave2,nWave2);

            // Turn off nChannel
            moduleAOU.channelWaveShape(nChannel,SD_Waveshapes.AOU_OFF);

            // Switch off angle modulation and Amplitude modulation
            moduleAOU.modulationAngleConfig(nChannel,SD_ModulationTypes.AOU_MOD_OFF,0);
            moduleAOU.modulationAmplitudeConfig(nChannel,SD_ModulationTypes.AOU_MOD_OFF,0);

            // Config amplitude and setup AWG in nChannel
            moduleAOU.channelAmplitude(nChannel,1.2);				// 1.2 Volts Peak
            moduleAOU.channelWaveShape(nChannel,SD_Waveshapes.AOU_AWG);

            // Set external trigger as input
            moduleAOU.triggerIOdirection(SD_TriggerDirections.AOU_TRG_IN);

            // Config trigger as external trigger and rising edge
            moduleAOU.AWGtriggerExternalConfig(nChannel,SD_TriggerExternalSources.TRIGGER_EXTERN, SD_TriggerBehaviors.TRIGGER_RISE);

            // Flush channel waveform queue
            moduleAOU.AWGflush(nChannel);

            // Queue waveform nWave1 with VI/HVI trigger and delay of 50ns from the trigger
            moduleAOU.AWGqueueWaveform(nChannel,nWave1,SD_TriggerModes.VIHVITRIG,50,1,0);

            // Queue waveform nWave1 with external trigger and delay of 100ns from the trigger
            moduleAOU.AWGqueueWaveform(nChannel,nWave1,SD_TriggerModes.EXTTRIG,100,1,0);

            // Queue waveforms nWave1 and nWave2 with differents trigger and delay of 200ns from the trigger and between them
            moduleAOU.AWGqueueWaveform(nChannel,nWave2,SD_TriggerModes.EXTTRIG,200,1,0);
            moduleAOU.AWGqueueWaveform(nChannel,nWave1,SD_TriggerModes.AUTOTRIG,280,1,0);

            printToConsole("External trigger configurated.\nModule configuration successfull, Press CONTINUE to start the AWG");
            runPause();

            moduleAOU.AWGstart(nChannel);

            printToConsole("AWG started. Waiting for the triggers. Press CONTINUE to send a VI/HVI trigger." );
            runPause();

            moduleAOU.AWGtrigger(nChannel);

            printToConsole("Waiting for two external triggers. Press CONTINUE to stop the AWG.");
            runPause();

            moduleAOU.AWGstop(nChannel);

            printToConsole("AWG Stopped. Test Finished.");

        }

        private void buttonTestMultipleWaveforms_Click(object sender, EventArgs e)
        {
            clearConsole();

            int nWave1 = 0;
            int nWave2 = 1;

            // Create a waveform object in PC RAM from waveform file
            SD_Wave wave1 = new SD_Wave("..\\..\\..\\..\\..\\..\\..\\Waveforms\\Triangular.csv");
            SD_Wave wave2 = new SD_Wave("..\\..\\..\\..\\..\\..\\..\\Waveforms\\Gaussian.csv");
            if (wave1.getStatus() < 0 || wave2.getStatus() < 0)
            {
                printToConsole("Error opening waveform File");
                return;
            }

            // Erase all waveforms from module memory and load waveforms waveId1 and waveId2 in positions nWave1 and nWave2
            moduleAOU.waveformFlush();
            moduleAOU.waveformLoad(wave1, nWave1);
            moduleAOU.waveformLoad(wave2, nWave2);

            // Turn off nChannel
            moduleAOU.channelWaveShape(nChannel, SD_Waveshapes.AOU_OFF);

            // Switch off angle modulation and Amplitude modulation
            moduleAOU.modulationAngleConfig(nChannel, SD_ModulationTypes.AOU_MOD_OFF, 0);
            moduleAOU.modulationAmplitudeConfig(nChannel, SD_ModulationTypes.AOU_MOD_OFF, 0);

            // Config amplitude and setup AWG in nChannel
            moduleAOU.channelAmplitude(nChannel, 1.2);			// 1.2 Volts Peak
            moduleAOU.channelWaveShape(nChannel, SD_Waveshapes.AOU_AWG);

            // Flush channel waveform queue
            moduleAOU.AWGflush(nChannel);

            // Queue waveforms nWave1 and nWave2 in nChannel
            moduleAOU.AWGqueueWaveform(nChannel, nWave1, SD_TriggerModes.AUTOTRIG, 0, 1, 0);
            moduleAOU.AWGqueueWaveform(nChannel, nWave2, SD_TriggerModes.AUTOTRIG, 0, 2, 0);

            printToConsole("Module configuration successfull. Press CONTINUE to start the AWG");
            runPause();

            moduleAOU.AWGstart(nChannel);

            printToConsole("AWG started. Press CONTINUE to stop the AWG.");
            runPause();

            moduleAOU.AWGstop(nChannel);

            printToConsole("AWG Stopped. Press CONTINUE to start the AWG.");
            runPause();

            moduleAOU.AWGstart(nChannel);

            printToConsole("AWG started. Press CONTINUE to restart the AWG.");
            runPause();

            moduleAOU.AWGstart(nChannel);

            printToConsole("AWG started. Press CONTINUE to stop the AWG.");
            runPause();

            moduleAOU.AWGstop(nChannel);

            printToConsole("AWG Stopped. Press CONTINUE to finish.");
            runPause();
        }

        private void buttonTestAMmodulation_Click(object sender, EventArgs e)
        {

            // Create a waveform object in PC RAM from waveform file
            SD_Wave wave = new SD_Wave("W:\\Waveforms_Demo\\Gaussian.csv");

            if(wave.getStatus() < 0)
            {
                printToConsole("Error opening waveform File");
                return;
            }
            int nWave = 0;

            // Erase all waveforms from module memory and load the waveform waveID in position nWave
            moduleAOU.waveformFlush();
            moduleAOU.waveformLoad(wave,nWave);

            // Turn off nChannel
            moduleAOU.channelWaveShape(nChannel,SD_Waveshapes.AOU_OFF);

            // Switch off angle modulation and setup AM modulation
            moduleAOU.modulationAngleConfig( nChannel,SD_ModulationTypes.AOU_MOD_OFF,0);
            moduleAOU.modulationAmplitudeConfig( nChannel,SD_ModulationTypes.AOU_MOD_AM,1);		// Deviation Gain = 1

            // Config carrier amplitude, frequency and shape
            moduleAOU.channelAmplitude(nChannel,0);								// 0 Volts Peak
            moduleAOU.channelFrequency(nChannel,10E6);	 						// 10 MHz
            moduleAOU.channelWaveShape(nChannel,SD_Waveshapes.AOU_SINUSOIDAL);

            // Flush channel waveform queue
            moduleAOU.AWGflush(nChannel);

            // Queue waveform nWave in nChannel
            moduleAOU.AWGqueueWaveform(nChannel,nWave,SD_TriggerModes.AUTOTRIG,0,0,1);

            printToConsole("Module configuration successfull. Press CONTINUE to start the AWG");
            runPause();

            moduleAOU.AWGstart(nChannel);

            printToConsole("AWG started. Press CONTINUE to stop the AWG.");
            runPause();

            moduleAOU.AWGstop(nChannel);

            printToConsole("AWG Stopped. Press CONTINUE to finish.");
            runPause();


        }

        private void buttonTestWaveformContinuous_Click(object sender, EventArgs e)
        {

            // Create a waveform object in PC RAM from waveform file
            SD_Wave wave = new SD_Wave("..\\..\\..\\..\\..\\..\\..\\Waveforms\\Triangular.csv");
            if(wave.getStatus() < 0)
            {
                printToConsole("Error opening waveform File");
                return;
            }
            int nWave = 0;

            // Switch off angle modulation and Amplitude modulation
            moduleAOU.modulationAngleConfig(nChannel,SD_ModulationTypes.AOU_MOD_OFF,0);
            moduleAOU.modulationAmplitudeConfig(nChannel,SD_ModulationTypes.AOU_MOD_OFF,0);

            // Erase all waveforms from module memory and load the waveform waveID in position nWave
            moduleAOU.waveformFlush();
            moduleAOU.waveformLoad(wave,nWave);

            // Config amplitude and setup AWG in nChannel
            moduleAOU.channelAmplitude(nChannel,1.2);					// 1.2 Volts Peak
            moduleAOU.channelWaveShape(nChannel,SD_Waveshapes.AOU_AWG);

            // Flush channel waveform queue
            moduleAOU.AWGflush(nChannel);

            // Queue waveform nWave in nChannel
            moduleAOU.AWGqueueWaveform(nChannel,nWave,SD_TriggerModes.AUTOTRIG,0,0,0);	// Cycles = 0

            printToConsole("Module configuration successfull. Press CONTINUE to start the AWG");
            runPause();

            moduleAOU.AWGstart(nChannel);

            printToConsole("AWG started. Press CONTINUE to pause the AWG.");
            runPause();

            moduleAOU.AWGpause(nChannel);

            printToConsole("AWG paused. Press CONTINUE to resume the AWG.");
            runPause();

            moduleAOU.AWGresume(nChannel);

            printToConsole("AWG resumed. Press CONTINUE to stop the AWG.");
            runPause();

            moduleAOU.AWGstop(nChannel);

            printToConsole("AWG stopped. Press CONTINUE to start the AWG.");
            runPause();

            moduleAOU.AWGstart(nChannel);

            printToConsole("AWG started. Press CONTINUE to stop the AWG.");
            runPause();

            moduleAOU.AWGstop(nChannel);

            printToConsole("AWG Stopped. Press CONTINUE to finish.");
            runPause();

        }

        private void buttonTestFrequencyModulation_Click(object sender, EventArgs e)
        {

            // Create a waveform object in PC RAM from waveform file
            SD_Wave wave = new SD_Wave("..\\..\\..\\..\\..\\..\\..\\Waveforms\\Gaussian.csv");
            if(wave.getStatus()<0)
            {
                printToConsole("Error opening waveform File");
                runPause();
                return;
            }
            int nWave = 0;

            // Erase all waveforms from module memory and load the waveform waveID in position nWave
            moduleAOU.waveformFlush();
            moduleAOU.waveformLoad(wave,nWave);

            // Turn off nChannel
            moduleAOU.channelWaveShape(nChannel,SD_Waveshapes.AOU_OFF);

            // Switch off amplitude modulation and setup FM modulation
            moduleAOU.modulationAmplitudeConfig(nChannel,SD_ModulationTypes.AOU_MOD_OFF,0);
            moduleAOU.modulationAngleConfig(nChannel, SD_ModulationTypes.AOU_MOD_FM, 10 * 1E6);			// Deviation Gain = 10 * 1E6 (in Hz)

            // Config amplitude, frequency and shape
            moduleAOU.channelAmplitude(nChannel,1.0);							// 1 Volts Peak
            moduleAOU.channelFrequency(nChannel,10E6);	 						// 10 MHz
            moduleAOU.channelWaveShape(nChannel,SD_Waveshapes.AOU_SINUSOIDAL);

            // Flush channel waveform queue
            moduleAOU.AWGflush(nChannel);

            // Queue waveform nWave in nChannel
            moduleAOU.AWGqueueWaveform(nChannel,nWave,SD_TriggerModes.AUTOTRIG,0,0,1);

            printToConsole("Module configuration successfull. Press CONTINUE to start the AWG");
            runPause();

            moduleAOU.AWGstart(nChannel);

            printToConsole("AWG started. Press CONTINUE to stop the AWG.");
            runPause();

            moduleAOU.AWGstop(nChannel);

            printToConsole("AWG Stopped. Press CONTINUE to finish.");
            runPause();

        }

        private void buttonTestTriggerOutClockOut_Click(object sender, EventArgs e)
        {
            printToConsole("Trigger set as OUT");
            printToConsole("Clock Out set 0 Hz. Trigger Out set Hight");
            moduleAOU.clockIOconfig(0);
            moduleAOU.triggerIOdirection(SD_TriggerDirections.AOU_TRG_OUT);
            moduleAOU.triggerIOwrite(1);
            runPause();

            printToConsole("Clock Out set 10 Hz. Trigger Out set Low");
            moduleAOU.clockIOconfig(10);
            moduleAOU.triggerIOdirection(SD_TriggerDirections.AOU_TRG_OUT);
            moduleAOU.triggerIOwrite(0);
            runPause();

            printToConsole("Clock Out set 50 Hz. Trigger Out set Hight");
            moduleAOU.clockIOconfig(50);
            moduleAOU.triggerIOdirection(SD_TriggerDirections.AOU_TRG_OUT);
            moduleAOU.triggerIOwrite(1);
            runPause();

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }


    }
}
