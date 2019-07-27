using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using KeysightSD1;


namespace AOU_Demo
{
    public partial class Form1 : Form
    {
        // Private variables declaration
        private SD_AOU module;
        private int WFinModuleCount;
        private int WFinQueueCount;


        public Form1()
        {
            InitializeComponent();

            // Create the AOU module object
            module = new SD_AOU();

            // Initialize private variables   
            WFinModuleCount = 0;
            WFinQueueCount = 0;

            // Disable controls which need an open module to work
            groupBoxAWG.Enabled = false;
            groupBoxChannel.Enabled = false;
            groupBoxModulation.Enabled = false;

        }

        private void buttonOpen_Click(object sender, EventArgs e)
        {
            int status;

            if (module.isOpen() == false) //Check if the module is not already opened
            {
                status = module.open(textBoxName.Text, (int)numericUpDownChassis.Value, (int)numericUpDownSlot.Value);

                if (status > 0) 
                {
                    // Module opened succesfully
                    textBoxStatus.Text = "Module Opened (" + status.ToString() + ")";
                    groupBoxChannel.Enabled = true;
                    groupBoxAWG.Enabled = true;
                    groupBoxModulation.Enabled = true;
                }
                else
                {
                    //Error open module (name or slot must be wrong)
                    textBoxStatus.Text = "Open Error: " + status.ToString();
                    groupBoxAWG.Enabled = false;
                    groupBoxChannel.Enabled = false;
                    groupBoxModulation.Enabled = false;
                }

                // Initialize some channel controls
                comboBoxChannel.SelectedItem = 0;
                comboBoxWaveShape.SelectedItem = 0;
                numericUpDownAmplitude.Value = 0M;
                numericUpDownOffset.Value = 0M;
                numericUpDownFrequency.Value = 0M;
            }
            else
                textBoxStatus.Text = "Module already opened";
        }

        private void buttonClose_Click(object sender, EventArgs e)
        {
            //Check if the module is opened before trying to close it
            if (module.isOpen() == true) 
            {

                comboBoxChannel.SelectedItem = 0;
                comboBoxWaveShape.SelectedItem = 0;
                numericUpDownAmplitude.Value = 0M;
                numericUpDownOffset.Value = 0M;
                numericUpDownFrequency.Value = 0M;

                groupBoxAWG.Enabled = false;
                groupBoxChannel.Enabled = false;
                groupBoxModulation.Enabled = false;

                int status = module.close();

                textBoxStatus.Text = "Module Closed (" + status.ToString() + ")";
            }
            else
            {
                textBoxStatus.Text = "Close Error: No module opened";            
            }
        }

        private void comboBoxWaveShape_SelectedIndexChanged(object sender, EventArgs e)
        {
            string waveshapeStr = comboBoxWaveShape.SelectedItem.ToString();
            int nChannel = comboBoxChannel.SelectedIndex;

            if (waveshapeStr == "AWG")
            {
                // Set channel waveshape to Arbitrary waveform
                module.channelWaveShape(nChannel, SD_Waveshapes.AOU_AWG);
            }
            else
            {
                if (waveshapeStr == "Off")
                    module.channelWaveShape(nChannel, SD_Waveshapes.AOU_OFF); //Turn off channel
                else if (waveshapeStr == "Sinusoidal")
                    module.channelWaveShape(nChannel, SD_Waveshapes.AOU_SINUSOIDAL); // Set channel to sinusoidal
                else if (waveshapeStr == "Triangular")
                    module.channelWaveShape(nChannel, SD_Waveshapes.AOU_TRIANGULAR); // Set channel to Truangular
                else if (waveshapeStr == "Square")
                    module.channelWaveShape(nChannel, SD_Waveshapes.AOU_SQUARE); // Set channel to Square
                else if (waveshapeStr == "DC")
                    module.channelWaveShape(nChannel, SD_Waveshapes.AOU_DC); // Set channel to DC
            }

        }

        private void numericUpDownAmplitude_ValueChanged(object sender, EventArgs e)
        {
            // Change the selected channel amplitud (in volts)
            module.channelAmplitude(comboBoxChannel.SelectedIndex, (double)numericUpDownAmplitude.Value);
        }

        private void numericUpDownFrequency_ValueChanged(object sender, EventArgs e)
        {
            // Change the selected channel frequency (in Hz)
            module.channelFrequency(comboBoxChannel.SelectedIndex, (double)numericUpDownFrequency.Value * 1E6);
        }

        private void numericUpDownOffset_ValueChanged(object sender, EventArgs e)
        {
            // Change the selected channel offset (in volts)
            module.channelOffset(comboBoxChannel.SelectedIndex, (double)numericUpDownOffset.Value);
        }

        private void numericUpDownPhase_ValueChanged(object sender, EventArgs e)
        {
            // Change the selected channel Phase (in degrees) 
            module.channelPhase(comboBoxChannel.SelectedIndex, (double)numericUpDownPhase.Value);
        }

        private void buttonResetPhases_Click(object sender, EventArgs e)
        {

            int resetMask = 0;

            // Build the reset mask from the check box values
            if (checkBoxRstCh0.Checked)
                resetMask |= 1 << 0;
            if (checkBoxRstCh1.Checked)
                resetMask |= 1 << 1;
            if (checkBoxRstCh2.Checked)
                resetMask |= 1 << 2;
            if (checkBoxRstCh3.Checked)
                resetMask |= 1 << 3;
            // Reset the accumulated phase of all channels simultaneously with a bit mask
            // Resetting the accumulated phase is usefull to achieve phase coherent waveforms in multiple channels
            module.channelPhaseResetMultiple(resetMask);
        }

        private void buttonResetPhase_Click(object sender, EventArgs e)
        {
            // Reset the accumulated phase of the selected channel only
            module.channelPhaseReset((int)comboBoxChannel.SelectedIndex);
        }

        private void buttonBrowse_Click(object sender, EventArgs e)
        {
            // Show file selection dialog to select a waveform file
            openFileDialog1.ShowDialog();

            string filename = openFileDialog1.FileName;

            textBoxFileName.Text = filename;
        }

        private void buttonLoadWaveform_Click(object sender, EventArgs e)
        {
            string filename = textBoxFileName.Text;

            // Create a waveform object from a waveform file to load it later to the module memory
            SD_Wave tmpWaveform = new SD_Wave(filename);

            // Load the waveform in the waveform object to the module memory
            int status = module.waveformLoad(tmpWaveform, WFinModuleCount);

            // Update the loaded waveform visualization textbox and counter
            if (status >= 0)
            {
                textBoxWFModuleList.Text = textBoxWFModuleList.Text + "WF#:" + WFinModuleCount.ToString() + " => " + filename + "\r\n";
                WFinModuleCount++;
            }
            labelWaveformsInModule.Text = "Waveforms in Module: " + WFinModuleCount.ToString();

        }

        private void buttonLoadInternal_Click(object sender, EventArgs e)
        {
            string filename = textBoxFileName.Text;

            //Define a double array with half a gaussian to create a waveform object
            double[] dataTmp = {    0.000003726653172, 0.000006113567966, 0.000009929504306, 0.000015966783898, 0.000025419346516, 
                                    0.000040065297393, 0.000062521503775, 0.000096593413722, 0.000147748360232, 0.000223745793721,
                                    0.000335462627903, 0.000497955421503, 0.000731802418880, 0.001064766236668, 0.001533810679324,
                                    0.002187491118183, 0.003088715408237, 0.004317840007633, 0.005976022895006, 0.008188701014374,
                                    0.011108996538242, 0.014920786069068, 0.019841094744370, 0.026121409853918, 0.034047454734599,
                                    0.043936933623407, 0.056134762834134, 0.071005353739637, 0.088921617459386, 0.110250525304485,
                                    0.135335283236613, 0.164474456577155, 0.197898699083615, 0.235746076555864, 0.278037300453194,
                                    0.324652467358350, 0.375311098851400, 0.429557358210739, 0.486752255959972, 0.546074426639710,
                                    0.606530659712633, 0.666976810858475, 0.726149037073691, 0.782704538241868, 0.835270211411272,
                                    0.882496902584595, 0.923116346386636, 0.955997481833100, 0.980198673306755, 0.995012479192682};
            
            // Create a waveform object from a data vector
            SD_Wave tmpWaveform = new SD_Wave(SD_WaveformTypes.WAVE_ANALOG, 50, dataTmp);

            // Load the waveform object on the module memory
            int status = module.waveformLoad(tmpWaveform, WFinModuleCount);

            // Update the loaded waveform visualization textbox and counter
            if (status >= 0)
            {
                textBoxWFModuleList.Text = textBoxWFModuleList.Text + "WF#:" + WFinModuleCount.ToString() + " => Inertnal (Half-Gaussian)" + "\r\n";
                WFinModuleCount++;
            }
            labelWaveformsInModule.Text = "Waveforms in Module: " + WFinModuleCount.ToString();
        }

        private void buttonFlushModule_Click(object sender, EventArgs e)
        {
            // Flush all waveforms from the module memory
            module.waveformFlush();

            // Update the loaded waveform visualization textbox and counter
            textBoxWFModuleList.Text = "";
            WFinModuleCount = 0;
            labelWaveformsInModule.Text = "Waveforms in Module: " + WFinModuleCount.ToString();
        }

        private void buttonQueue_Click(object sender, EventArgs e)
        {
            // Check if the waveform number to queue is already loaded into the module if not the waveform cannot be queued
            if (numericUpDownWFnumber.Value >= WFinModuleCount)
            {
                labelWaveformsInQueue.Text = "Waveforms in Queue: " + WFinQueueCount.ToString() + " - ERROR: Invalid Waveform #";
                return;
            }

            // Queue the waveform into the selected channel queue
            int status = module.AWGqueueWaveform((int)comboBoxChannel.SelectedIndex, (int)numericUpDownWFnumber.Value, 0, 0, (int)numericUpDownCycles.Value, (int)numericUpDownPrescaler.Value);

            // Update the queued waveform visualization textbox and counter
            if (status >= 0)
            {
                textBoxWFQueueList.Text = textBoxWFQueueList.Text + WFinQueueCount.ToString() + ": => WF#:" + numericUpDownWFnumber.Value.ToString() + ", Cycles:" + numericUpDownCycles.Value.ToString() + ", Prescaler:" + numericUpDownPrescaler.Value.ToString() + "\r\n";
                WFinQueueCount++;
            }
            labelWaveformsInQueue.Text = "Waveforms in Queue: " + WFinQueueCount.ToString();
        }

        private void buttonFlushQueue_Click(object sender, EventArgs e)
        {
            // Remove all waveform from the queue
            module.AWGflush((int)comboBoxChannel.SelectedIndex);

            // Update the queued waveform visualization textbox and counter
            textBoxWFQueueList.Text = "";
            WFinQueueCount = 0;
            labelWaveformsInQueue.Text = "Waveforms in Queue: " + WFinQueueCount.ToString();
        }

        private void buttonPlay_Click(object sender, EventArgs e)
        {
            // Start the AWG to reproduce the waveforms in the queue
            module.AWGstart((int)comboBoxChannel.SelectedIndex);
        }

        private void buttonStop_Click(object sender, EventArgs e)
        {
            // Stop the AWG
            module.AWGstop((int)comboBoxChannel.SelectedIndex);
        }

        private void comboBoxModulation_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBoxModulation.SelectedItem.ToString() == "IQ")
            {
                // IQ modulation don't have deviation gain => disable de control
                numericUpDownDevGain.Enabled = false;
            }
            else
            {
                numericUpDownDevGain.Enabled = true;
                if (comboBoxModulation.SelectedItem.ToString() == "Amplitude")
                {
                    // Set the deviation gain control to the amplitud modulation range: -1.5V<->1.5V
                    numericUpDownDevGain.Minimum = -1.5M;
                    numericUpDownDevGain.Maximum = 1.5M;
                    numericUpDownDevGain.Increment = 0.1M;
                    labelDevGain.Text = "Deviation Gain (V)";
                }
                else if (comboBoxModulation.SelectedItem.ToString() == "Frequency")
                {
                    // Set the deviation gain control to the frequency modulation range: -200MHz<->200MHzV
                    numericUpDownDevGain.Minimum = -200M;
                    numericUpDownDevGain.Maximum = 200M;
                    numericUpDownDevGain.Increment = 10M;
                    labelDevGain.Text = "Deviation Gain (MHz)";
                }
                else if (comboBoxModulation.SelectedItem.ToString() == "Phase")
                {
                    // Set the deviation gain control to the frequency modulation range: --180deg<->180deg
                    numericUpDownDevGain.Minimum = -180M;
                    numericUpDownDevGain.Maximum = 180M;
                    numericUpDownDevGain.Increment = 10M;
                    labelDevGain.Text = "Deviation Gain (Deg)";
                }
            
            }

            // Configure de modulation 
            setModulation();
        }

        private void numericUpDownDevGain_ValueChanged(object sender, EventArgs e)
        {
            setModulation();
        }

        private void setModulation()
        {
            double devGain = (double)numericUpDownDevGain.Value;

            if (comboBoxModulation.SelectedItem.ToString() == "Amplitude")
            {
                // Turn on the amplitude modulation and off the frequency modulation (both could be on simultaneously)
                module.modulationAmplitudeConfig((int)comboBoxChannel.SelectedIndex, SD_ModulationTypes.AOU_MOD_AM, devGain);
                module.modulationAngleConfig((int)comboBoxChannel.SelectedIndex, SD_ModulationTypes.AOU_MOD_OFF, 0.0);
            }
            else if (comboBoxModulation.SelectedItem.ToString() == "Frequency")
            {
                // Turn on the frequency modulation and off the amplitude modulation (both could be on simultaneously)
                module.modulationAmplitudeConfig((int)comboBoxChannel.SelectedIndex, SD_ModulationTypes.AOU_MOD_OFF, 0.0);
                module.modulationAngleConfig((int)comboBoxChannel.SelectedIndex, SD_ModulationTypes.AOU_MOD_FM, devGain * 1E6);
            }
            else if (comboBoxModulation.SelectedItem.ToString() == "Phase")
            {
                // Turn on the phase modulation and off the amplitude modulation (both could be on simultaneously)
                module.modulationAmplitudeConfig((int)comboBoxChannel.SelectedIndex, SD_ModulationTypes.AOU_MOD_OFF, 0.0);
                module.modulationAngleConfig((int)comboBoxChannel.SelectedIndex, SD_ModulationTypes.AOU_MOD_PHASE, devGain);
            }
            else if (comboBoxModulation.SelectedItem.ToString() == "IQ")
            {
                // Turn on the IQ modulation, both Amplitude and Frequency/Phase modulations are automatically dissabled
                module.modulationIQconfig((int)comboBoxChannel.SelectedIndex, 1);
            }
            else
            {
                // Disable all modulations
                module.modulationIQconfig((int)comboBoxChannel.SelectedIndex, 0);
                module.modulationAmplitudeConfig((int)comboBoxChannel.SelectedIndex, SD_ModulationTypes.AOU_MOD_OFF, 0.0);
                module.modulationAngleConfig((int)comboBoxChannel.SelectedIndex, SD_ModulationTypes.AOU_MOD_OFF, 0.0);
            }
        }

    }
}
