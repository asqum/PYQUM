using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using KeysightSD1;

namespace AWGtest
{
    class Program
    {
        static void Main(string[] args)
        {
            int status;

            //Create an instance of the AOU module
            SD_AOU moduleAOU = new SD_AOU();

            //Open a physical AOU-H0002 module on Slot 4
            if ((status = moduleAOU.open("", 0, 6)) < 0)
            {
                Console.WriteLine("Error openning the Module 'SD-PXE-AOU-H0002', make sure the slot and chassis are correct. Aborting the Demo...");
                Console.ReadKey();

                return;
            }

            // Config amplitude and setup AWG in channels 0 and 1
            moduleAOU.channelAmplitude(0, 1.2);				// 1.2 Volts Peak
            moduleAOU.channelWaveShape(0, SD_Waveshapes.AOU_AWG);
            moduleAOU.channelAmplitude(1, 1.2);				// 1.2 Volts Peak
            moduleAOU.channelWaveShape(1, SD_Waveshapes.AOU_AWG);

            Console.WriteLine("Press any key to run the AWG on channel 0 (infinite cycles of a Triangular with prescaler 2)...");
            Console.ReadKey();
            // Load, queue and run the Triangular.csv waveform on channel 0
            if (moduleAOU.AWG(0, "Triangular.csv", SD_TriggerModes.AUTOTRIG, 0, 0, 2) < 0)
            {
                Console.WriteLine("Error loading the waveform file 'Triangular.csv', make sure the path is correct. Aborting the Demo...");
                Console.ReadKey();

                moduleAOU.close();
                return;
            }

            Console.WriteLine("Press any key to run the AWG on channel 1 (2 cycles of a Triangular with prescaler 5)...");
            Console.ReadKey();
            // Load, queue and run the Triangular.csv waveform on channel 1
            if (moduleAOU.AWG(1, "Triangular.csv", SD_TriggerModes.AUTOTRIG, 0, 2, 5) < 0)
            {
                Console.WriteLine("Error loading the waveform file 'Triangular.csv', make sure the path is correct. Aborting the Demo...");
                Console.ReadKey();

                moduleAOU.close();
                return;
            }

            Console.WriteLine("Press any key to stop the AWGs 0 and 1...");
            Console.ReadKey();
            //Stop simultaneously the AWGs of channels 0 and 1.
            moduleAOU.AWGstopMultiple(3);


            Console.WriteLine("Press any key to run the AWG on channel 0 and 1...");
            Console.WriteLine("(Channel 0: 1 cycle Triangular with prescaler 4 -- Channel 1: 3 cycles Triangular with prescaler 3)");
            Console.ReadKey();
            // Load, queue and run the triangular.csv waveform on channel 0
            if (moduleAOU.AWG(0, "Triangular.csv", SD_TriggerModes.AUTOTRIG, 0, 1, 4) < 0)
            {
                Console.WriteLine("Error loading the waveform file 'Triangular.csv', make sure the path is correct. Aborting the Demo...");
                Console.ReadKey();

                moduleAOU.close();
                return;
            }
            // Load, queue and run the triangular.csv waveform on channel 1
            if (moduleAOU.AWG(1, "Triangular.csv", SD_TriggerModes.AUTOTRIG, 0, 3, 3) < 0)
            {
                Console.WriteLine("Error loading the waveform file 'Triangular.csv', make sure the path is correct. Aborting the Demo...");
                Console.ReadKey();

                moduleAOU.close();
                return;
            }

            Console.WriteLine("Press any key to run the AWG on channel 0 with a long handmade RAW triangular waveform...");
            Console.ReadKey();

            double data = 0;
            int nPoints = 1000000;
            double inc = 0.1;
            short[] waveformData = new short[nPoints];
            for(int i = 0; i < nPoints; i++)
            {
                waveformData[i] = (short)(data*32767.0);
                data = data + inc;
                if(data > 1)
                {
                    data = 2-data;
                    inc = -0.1;
                }
                else if (data < -1)
                {
                    data = -2 - data;
                    inc = 0.1;
                }
            }

            if (moduleAOU.waveformLoad(SD_WaveformTypes.WAVE_ANALOG, waveformData, 0) < 0)
            {
                Console.WriteLine("Error loading the waveform, make sure its data and type are correct. Aborting the Demo...");
                Console.ReadKey();

                moduleAOU.close();
                return;
            }

            if (moduleAOU.AWGqueueWaveform(0, 0, 0, 0, 0, 0) < 0)
            {
                Console.WriteLine("Error queueing loaded waveform, make sure queue parameters are correct. Aborting the Demo...");
                Console.ReadKey();

                moduleAOU.close();
                return;
            }

            if (moduleAOU.AWGstart(0) < 0)
            {
                Console.WriteLine("Error running AWG. Aborting the Demo...");
                Console.ReadKey();

                moduleAOU.close();
                return;
            }

            Console.WriteLine("Press any key to quit the demo...");
            Console.ReadKey();

            moduleAOU.close();
        }
    }
}
