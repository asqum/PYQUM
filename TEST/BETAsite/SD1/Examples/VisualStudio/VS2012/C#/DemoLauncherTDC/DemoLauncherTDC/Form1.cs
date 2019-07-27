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
        private SD_TDC moduleTDC;
        private int nChannel, nChannel2;
        private int pause;

        public Form1()
        {
            InitializeComponent();

            // Create the AOU module object
            moduleTDC = new SD_TDC();

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

            if (moduleTDC.isOpen() == false) //Check if the module is not already opened
            {
                status = moduleTDC.open(textBoxName.Text, (int)numericUpDownChassis.Value, (int)numericUpDownSlot.Value);

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
            if (moduleTDC.isOpen() == true)
            {

                groupBoxTests.Enabled = false;

                int status = moduleTDC.close();

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

       

        private void buttonDAQwithoutBuffers_Click(object sender, EventArgs e)
        {
            ulong[] dataBuffer = new ulong[100];
            int pointsRead = 0;
            int i = 0;

            // Config DAQ with two cycles of 16 points
            moduleTDC.DAQconfig(nChannel, 16, 2, 1, SD_TriggerModes.VIHVITRIG);

            // Flush DAQ
            moduleTDC.DAQflush(nChannel);

            printToConsole("Module configuration successfull. Press any key to start the DAQ.");
            runPause();

            // Start DAQ
            moduleTDC.DAQstart(nChannel);

            printToConsole("DAQ started. Waiting for first cycle's trigger. Press any key to send a VI/HVI trigger.");
            runPause();

            // Send VI/HVI trigger
            moduleTDC.DAQtrigger(nChannel);

            // Waiting for 16 points
            while (moduleTDC.DAQcounterRead(nChannel) < 16) ;

            printToConsole("DAQ has acquired " + moduleTDC.DAQcounterRead(nChannel).ToString() + " points.");
            runPause();

            printToConsole("Press any key to send another trigger. Press any key to send a VI/HVI trigger.");
            runPause();

            // Send VI/HVI trigger
            moduleTDC.DAQtrigger(nChannel);

            // Waiting for 32 points
            while (moduleTDC.DAQcounterRead(nChannel) < 32) ;

            printToConsole("DAQ has acquired " + moduleTDC.DAQcounterRead(nChannel).ToString() + " points.");
            runPause();

            // Read data of frist cycle
            pointsRead = moduleTDC.DAQread(nChannel, dataBuffer, 1);
            printToConsole("Points read : " + pointsRead.ToString());
            runPause();

            printToConsole("Data of frist cycle\n");
            for (i = 0; i < 16; i++)
                printToConsole("Data[" + i.ToString() + "]: " + dataBuffer[i].ToString());
            runPause();

            printToConsole("Data of second cycle\n");
            for (i = 16; i < pointsRead; i++)
                printToConsole("Data[" + i.ToString() + "]: " + dataBuffer[i].ToString());
            runPause();

            // Stop DAQ
            moduleTDC.DAQstop(nChannel);

            printToConsole("Press any key to finish.");
            runPause();
        }

        private void ButtonHistogram_Click(object sender, EventArgs e)
        {
	        int[] bufferHistograma;
            bufferHistograma = new int[500];
	        int i, maxBin, maxValue;
	        ulong totalValue;
	        double noise;
        	
	        // Config Histogram with windown size of 160ns and offset 0
	        moduleTDC.histogramConfig(0, nChannel, nChannel2, 0, 500, 0); // BinSize = 320ps 

            printToConsole("Module configuration successfull. Press any key to start the Histogram.");
	        runPause();

	        moduleTDC.histogramStart(0);

            printToConsole("Press any key to pause.");
	        runPause();

	        moduleTDC.histogramPause(0);

            printToConsole("Press any key to resume.");
	        runPause();

	        moduleTDC.histogramResume(0);

            printToConsole("Press any key to stop.");
	        runPause();

	        moduleTDC.histogramStop( 0);

	        // Read Histogram data
	        moduleTDC.histogramRead(0, 0, bufferHistograma);

	        moduleTDC.histogramFlush(0);

            printToConsole("Histogram data acquired: \n\n");

	        maxBin = -1;
	        maxValue = -1;
	        totalValue = 0;
	        // Show Histogram data
	        for(i=0;i<500;i++)
	        {
                printToConsole(" Bin: " + i.ToString() + " Time: " + ((i * 320.0) / 1000.0).ToString() + " ns - Value of bin: " + bufferHistograma[i].ToString());
		        if((i % 100)==99)
		        {
                    printToConsole("\nPress any key to continue.");
			        runPause();
		            }
		        if(bufferHistograma[i] > maxValue)
		        {
			        maxValue = bufferHistograma[i];
			        maxBin = i;
		        }
		        totalValue += (ulong) bufferHistograma[i];
	        }

            printToConsole("Max Bin : " + maxBin.ToString() + " - Time : " + ((maxBin * 320.0) / 1000.0).ToString() + " ns");
	        printToConsole("Max Value : " + maxValue.ToString());
	        noise = (totalValue - (ulong)maxValue)/(500.0-1);
	        printToConsole("Noise : " + noise.ToString());
	        printToConsole("SNR : " + (maxValue / noise).ToString());
	        printToConsole("\nPress any key to finish.");
	        runPause();
        }

        private void BottonRateCounterRead_Click(object sender, EventArgs e)
        {
            int rateCount;

            // Config channel with 0V of threshold and rising edge
            moduleTDC.thresholdConfig(nChannel, 0);
            moduleTDC.edgeConfig(nChannel, 0); //TDC_RISING_EDGE); !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            // Set counter rate in 1s
            moduleTDC.rateCounterConfig(nChannel, 1000000);		// 1s
            rateCount = moduleTDC.rateCounterRead(nChannel);

            printToConsole(" Rate Couter is : " + rateCount.ToString() + " Counts");

            printToConsole("Press any key to finish.");
            runPause();
        }

        private void buttonDAQwithBuffers_Click(object sender, EventArgs e)
        {
	        ulong dataPrev=0;
	        ulong[] dataBuffer = new ulong[16];
	        int totalPointsRead = 0;
	        int nPointsRead = 0;
	        int error = 0;
	        int i = 0;

            // Config DAQ Buffers Pool with Callback
            moduleTDC.DAQbufferPoolConfig(nChannel, dataBuffer, 1000);

            // Add other buffer
            dataBuffer = new ulong[16];
            moduleTDC.DAQbufferAdd(nChannel, dataBuffer);  

	        // Stop DAQ
	        moduleTDC.DAQstop(nChannel);

	        // Flush DAQ
            moduleTDC.DAQflush(nChannel);

	        // Config DAQ with two cycles of 16 points
            moduleTDC.DAQconfig(nChannel, 16, 2, 1, SD_TriggerModes.VIHVITRIG);

            printToConsole("Module configuration successfull. Press any key to start the DAQ.");
            runPause();

	        // Start DAQ
            moduleTDC.DAQstart(nChannel);

            printToConsole("DAQ started. Waiting for trigger for first cycles. Press any key to send a VI/HVI trigger.");
            runPause();

	        // Send VI/HVI trigger
            moduleTDC.DAQtrigger(nChannel);

	        // Waiting for 16 points (first cycle)
            while (moduleTDC.DAQcounterRead(nChannel) < 16) ;

            printToConsole("DAQ has acquired " + (moduleTDC.DAQcounterRead(nChannel)).ToString() + " points.");
            runPause();

            printToConsole("Waiting for another trigger for second cycles. Press any key to send a VI/HVI trigger.");
            runPause();

	        // Send VI/HVI trigger
            moduleTDC.DAQtrigger(nChannel);

	        // Waiting for 16 points (second cycle)
            while (moduleTDC.DAQcounterRead(nChannel) < 32) ;

            printToConsole("DAQ has acquired " + (moduleTDC.DAQcounterRead(nChannel)).ToString() + " points.");
            runPause();

	        // Read data
	        while(totalPointsRead<32)
	        {
                dataBuffer = moduleTDC.DAQbufferGet(nChannel, out nPointsRead, out error);
                printToConsole("Points Read : " + nPointsRead.ToString());
                printToConsole("error : " + SD_Error.getErrorMessage(error));
                printToConsole("Data Buffer: ");
		        for(i = 0; i<nPointsRead; i++)
		        {
                    printToConsole("\tData[" + (i + totalPointsRead).ToString() + "] : " + dataBuffer[i].ToString() + " ps : difference = " + (dataBuffer[i] - dataPrev).ToString() + " ps\n");
			        dataPrev = dataBuffer[i];
		        }

		        totalPointsRead = totalPointsRead + nPointsRead;
                printToConsole("Total Points read : " + totalPointsRead.ToString());
	        }

            printToConsole("Press any key to finish.");
            runPause();

	        // Free all  buffers
            moduleTDC.DAQbufferPoolRelease(nChannel);
            while (moduleTDC.DAQbufferRemove(nChannel) != null) ;
        }
    }
}
