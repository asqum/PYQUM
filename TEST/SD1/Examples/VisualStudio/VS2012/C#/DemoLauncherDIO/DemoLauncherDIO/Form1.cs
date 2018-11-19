using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using KeysightSD1;

namespace TestLauncher
{
    public partial class Form1 : Form
    {
        // Declare private variables
        private SD_DIO moduleDIO;
        private int nChannel, nChannel2;
        private int pause;

        public Form1()
        {
            InitializeComponent();

            // Create the AOU module object
            moduleDIO = new SD_DIO();

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

            if (moduleDIO.isOpen() == false) //Check if the module is not already opened
            {
                status = moduleDIO.open(textBoxName.Text, (int)numericUpDownChassis.Value, (int)numericUpDownSlot.Value);

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
            if (moduleDIO.isOpen() == true)
            {
                groupBoxTests.Enabled = false;

                int status = moduleDIO.close();

                textBoxStatus.Text = "Module Closed (" + status.ToString() + ")";
            }
            else
                textBoxStatus.Text = "Close Error: No module opened";
        }

        private void numericUpDownChannel_ValueChanged(object sender, EventArgs e)
        {
            // Initialize the channel variables used by the demo scripts
            nChannel = (int)numericUpDownChannel.Value;
            nChannel2 = (int)numericUpDownChannel2.Value;
        }

        private void buttonDAQwithoutBuffers_Click(object sender, EventArgs e)
        {
            short[] dataBuffer = new short[100];
            int pointsRead = 0;
            int i = 0;

            // Config the Input Bus 0 pins 0 to 15 of Port 0 
            moduleDIO.busConfig(SD_DIO_Bus.DIO_INPUT_BUS0 + nChannel, 0, 0, 15);

            // Config DAQ with two cycles of 16 points
            moduleDIO.DAQconfig(nChannel, 40, 2, 1, SD_TriggerModes.VIHVITRIG);

            // Flush DAQ
            moduleDIO.DAQflush(nChannel);

            printToConsole("Module configuration successfull. Press any key to start the DAQ.");
            runPause();

            // Start DAQ
            moduleDIO.DAQstart(nChannel);

            printToConsole("DAQ started. Waiting for first cycle's trigger. Press any key to send a VI/HVI trigger.");
            runPause();

            // Send VI/HVI trigger
            moduleDIO.DAQtrigger(nChannel);

            // Waiting for 40 points
            while (moduleDIO.DAQcounterRead(nChannel) < 40) ;

            printToConsole("DAQ has acquired " + moduleDIO.DAQcounterRead(nChannel).ToString() + " points.");
            runPause();

            printToConsole("Press any key to send another trigger. Press any key to send a VI/HVI trigger.");
            runPause();

            // Send VI/HVI trigger
            moduleDIO.DAQtrigger(nChannel);

            // Waiting for 80 points
            while (moduleDIO.DAQcounterRead(nChannel) < 80) ;

            printToConsole("DAQ has acquired " + moduleDIO.DAQcounterRead(nChannel).ToString() + " points.");
            runPause();

            // Read data of frist cycle
            pointsRead = moduleDIO.DAQread(nChannel, dataBuffer, 1);
            printToConsole("Points read : " + pointsRead.ToString());
            runPause();

            printToConsole("Data of frist cycle\n");
            for (i = 0; i < 40; i++)
                printToConsole("Data[" + i.ToString() + "]: " + dataBuffer[i].ToString());
            runPause();

            printToConsole("Data of second cycle\n");
            for (i = 40; i < pointsRead; i++)
                printToConsole("Data[" + i.ToString() + "]: " + dataBuffer[i].ToString());
            runPause();

            // Stop DAQ
            moduleDIO.DAQstop(nChannel);

            printToConsole("Press any key to finish.");
            runPause();
        }
       
        private void buttonBuses_Click(object sender, EventArgs e)
        {
            int error, dataAux;

            // Config the Output Bus selected in pins 0 to 15 of Port selected  
            moduleDIO.busConfig(SD_DIO_Bus.DIO_OUTPUT_BUS0 + nChannel, nChannel, 0, 15);

            // Config the Input Bus selected in pins 0 to 15 of Port selected 
            moduleDIO.busConfig(SD_DIO_Bus.DIO_INPUT_BUS0 + nChannel, nChannel, 1, 15);

            //Config all pins as output
            moduleDIO.IOdirectionConfig(-1/*0xFFFFFFFFFFFFFFFF*/, SD_PinDirections.DIR_OUT);

            printToConsole("Module configuration successfull. Press any key to set the trigger.");
            runPause();

            dataAux = 32768;

            while (dataAux > 0)
            {
                error = moduleDIO.busWrite(SD_DIO_Bus.DIO_OUTPUT_BUS0 + nChannel, dataAux);
                if (error < 0)
                    return;

                printToConsole("Write data in OutputBus 0\n");

                dataAux = moduleDIO.busRead(SD_DIO_Bus.DIO_INPUT_BUS0 + nChannel, out error);
                if (error < 0)
                {
                    printToConsole(SD_Error.getErrorMessage(error));
                    return;
                }

                printToConsole("Read data in InputBus : " + dataAux.ToString());
                runPause();
            }
        }

        private void buttonDAQwithBuffers_Click(object sender, EventArgs e)
        {
            short dataPrev = 0;
            short[] dataBuffer = new short[40];
            int totalPointsRead = 0;
            int nPointsRead = 0;
            int error = 0;
            int i = 0;

            // Config the Input Bus 0 pins 0 to 15 of Port 0 
            moduleDIO.busConfig(SD_DIO_Bus.DIO_INPUT_BUS0 + nChannel, 0, 0, 15);

            // Stop DAQ
            moduleDIO.DAQstop(nChannel);

            // Flush DAQ
            moduleDIO.DAQflush(nChannel);

            // Config DAQ with two cycles of 40 points
            moduleDIO.DAQconfig(nChannel, 40, 2, 1, SD_TriggerModes.VIHVITRIG);

            // Config DAQ Buffers Pool with Callback
            moduleDIO.DAQbufferPoolConfig(nChannel, dataBuffer, 5000);

            // Add other buffer
            dataBuffer = new short[40];
            moduleDIO.DAQbufferAdd(nChannel, dataBuffer);

            printToConsole("Module configuration successfull. Press any key to start the DAQ.");
            runPause();

            // Start DAQ
            moduleDIO.DAQstart(nChannel);

            printToConsole("DAQ started. Waiting for trigger for first cycles. Press any key to send a VI/HVI trigger.");
            runPause();

            // Send VI/HVI trigger
            moduleDIO.DAQtrigger(nChannel);

            // Waiting for 16 points (first cycle)
            while (moduleDIO.DAQcounterRead(nChannel) < 40) ;

            printToConsole("DAQ has acquired " + (moduleDIO.DAQcounterRead(nChannel)).ToString() + " points.");
            runPause();

            printToConsole("Waiting for another trigger for second cycles. Press any key to send a VI/HVI trigger.");
            runPause();

            // Send VI/HVI trigger
            moduleDIO.DAQtrigger(nChannel);

            // Waiting for 16 points (second cycle)
            while (moduleDIO.DAQcounterRead(nChannel) < 80) ;

            printToConsole("DAQ has acquired " + (moduleDIO.DAQcounterRead(nChannel)).ToString() + " points.");
            runPause();

            // Read data
            while (totalPointsRead < 80)
            {
                dataBuffer = moduleDIO.DAQbufferGet(nChannel, out nPointsRead, out error);
                printToConsole("Points Read : " + nPointsRead.ToString());
                printToConsole("error : " + error.ToString());
                printToConsole("Data Buffer: ");
                for (i = 0; i < nPointsRead; i++)
                {
                    printToConsole("\tData[" + (i + totalPointsRead).ToString() + "] : " + dataBuffer[i].ToString());
                    dataPrev = dataBuffer[i];
                }

                totalPointsRead = totalPointsRead + nPointsRead;
                printToConsole("Total Points read : " + totalPointsRead.ToString());
            }

            printToConsole("Press any key to finish.");
            runPause();

            // Free all  buffers
            moduleDIO.DAQbufferPoolRelease(nChannel);
            while (moduleDIO.DAQbufferRemove(nChannel) != null) ;
        }

        private void buttonDWGfromArray_Click(object sender, EventArgs e)
        {
	        int error = 0;

	        // Config the Output Bus selected in pins 0 to 15 of Port selected 
	        moduleDIO.busConfig(SD_DIO_Bus.DIO_OUTPUT_BUS0 + nChannel, nChannel, 0, 15);

	        //Config all pins of both ports as output
	        moduleDIO.IOdirectionConfig(-1/*0XFFFFFFFFFFFFFFFF*/, SD_PinDirections.DIR_OUT);
 
	        // Erase all waveforms from module memory
            moduleDIO.waveformFlush();

	        printToConsole("Module configuration successfull. Press any key to start the DWG.");
	        runPause();

	        //Load waveforms from Array with prestaler 1 (100MSPS) and infinite cycles
	        int[] points = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32};
            error = moduleDIO.DWG(nChannel, SD_TriggerModes.AUTOTRIG, 0, 0, 1, SD_WaveformTypes.WAVE_DIGITAL, points);
	        if (error < 0)
	        {
		        printToConsole(SD_Error.getErrorMessage(error));
		        return;
	        }

	        printToConsole("Press any key to stop the DWG.");
	        runPause();

            moduleDIO.DWGstop(nChannel);

	        printToConsole("Press any key to finish.");
	        runPause();
        }

        private void buttonDWGstrobeOutWithTrigger_Click(object sender, EventArgs e)
        {
            // Config the Output Bus 0 in pins 0 to 15 of Port 0 
            moduleDIO.busConfig(SD_DIO_Bus.DIO_OUTPUT_BUS0, 0, 0, 15);

            // Config the Strobe 0 
            moduleDIO.busSamplingConfig(SD_DIO_Bus.DIO_OUTPUT_BUS0, 0, SD_Strobe.STROBE_ON, SD_Strobe.STROBE_EDGERISE, 0, 0, SD_DebouncingTypes.DEBOUNCING_NONE);

            //Config pins 0 to 15 of Port 0 as output
            moduleDIO.IOdirectionConfig( 0x000000000000FFFF, SD_PinDirections.DIR_OUT);

            // Create waveforms objects in PC RAM from waveforms files
            SD_Wave waveId1 = new SD_Wave("W:\\Waveforms_Demo\\Alberto\\DigitalTest_32samples.txt");
            SD_Wave waveId2 = new SD_Wave("W:\\Waveforms_Demo\\Alberto\\DigitalTest_48samples.txt");

            if (waveId1.getStatus() < 0 || waveId1.getStatus() < 0)
            {
                printToConsole("Error opening waveform File\n");
                runPause();
                // Waves will be freed by garbage colletor   
                return;
            }

            // Erase all waveforms from module memory and load waveforms waveId1 and waveId2 in position nWave1 and nWave2
            moduleDIO.waveformFlush();
            moduleDIO.waveformLoad(waveId1, 0);
            moduleDIO.waveformLoad(waveId2, 1);

            // Flush channel waveform queue
            moduleDIO.DWGflush(nChannel);

            // Queue waveforms nWave1 and nWave2 in nChannel
            moduleDIO.DWGqueueWaveform(nChannel, 0, SD_TriggerModes.AUTOTRIG, 0, 1, 1);
            moduleDIO.DWGqueueWaveform(nChannel, 1, SD_TriggerModes.VIHVITRIG, 0, 1, 1);

            printToConsole("Module configuration successfull. Press any key to start the DWG.");
            runPause();

            moduleDIO.DWGstart( nChannel);

            printToConsole("DWG started. Press any key to send a VI/HVI trigger.");
            runPause();

            moduleDIO.DWGtrigger( nChannel);

            printToConsole("Press any key to stop the DWG.");
            runPause();

            moduleDIO.DWGstop( nChannel);

            printToConsole("DWG Stopped. Press any key to finish.");
            runPause();
        }
    }
}
