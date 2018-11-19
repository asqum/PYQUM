#include <iostream>
using namespace KeysightSD1;

void main()
{
	int status;

	//Create an instance of the AOU module
    SD_AOU ^moduleAOU = gcnew SD_AOU();

    //Open a physical AOU-H0002 module on Slot 4
    if ((status = moduleAOU->open("SD-PXE-AOU-H0002", 0, 4)) < 0)
    {
		std::cout << "Error openning the Module 'SD-PXE-AOU-H0002', make sure the slot and chassis are correct. Aborting the Demo..." << std::endl;
		std::cin.get();

        return;
    }

    // Config amplitude and setup AWG in channels 0 and 1
    moduleAOU->channelAmplitude(0, 1.2);				// 1.2 Volts Peak
    moduleAOU->channelWaveShape(0, SD_Waveshapes().AOU_AWG);
    moduleAOU->channelAmplitude(1, 1.2);				// 1.2 Volts Peak
    moduleAOU->channelWaveShape(1, SD_Waveshapes().AOU_AWG);

    std::cout << "Press enter to run the AWG on channel 0 (infinite cycles of a Triangular with prescaler 2)..." << std::endl;
    std::cin.get();
    // Load, queue and run the Triangular.csv waveform on channel 0
    if((status = moduleAOU->AWG(0, "Triangular.csv", SD_TriggerModes().AUTOTRIG, 0, 0, 2)) < 0)
    {
        std::cout << "Error loading the waveform file 'Triangular.csv', make sure the path is correct. Aborting the Demo..." << std::endl;
        std::cin.get();

        moduleAOU->close();
        return;
    }

    std::cout << "Press enter to run the AWG on channel 1 (2 cycles of a Triangular with prescaler 5)..." << std::endl;
    std::cin.get();
    // Load, queue and run the Triangular.csv waveform on channel 1
    if (moduleAOU->AWG(1, "Triangular.csv", SD_TriggerModes().AUTOTRIG, 0, 2, 5) < 0)
    {
        std::cout << "Error loading the waveform file 'Triangular.csv', make sure the path is correct. Aborting the Demo..." << std::endl;
        std::cin.get();

        moduleAOU->close();
        return;
    }

    std::cout << "Press enter to stop the AWGs 0 and 1..." << std::endl;
    std::cin.get();
    //Stop simultaneously the AWGs of channels 0 and 1.
    moduleAOU->AWGstopMultiple(3);

            
    std::cout << "Press enter to run the AWG on channel 0 and 1..." << std::endl;
    std::cout << "(Channel 0: 1 cycle Triangular with prescaler 4 -- Channel 1: 3 cycles Triangular with prescaler 3)" << std::endl;
    std::cin.get();
    // Load, queue and run the triangular.csv waveform on channel 0
    if (moduleAOU->AWG(0, "Triangular.csv", SD_TriggerModes().AUTOTRIG, 0, 1, 4) < 0)
    {
        std::cout << "Error loading the waveform file 'Triangular.csv', make sure the path is correct. Aborting the Demo..." << std::endl;
        std::cin.get();

        moduleAOU->close();
        return;
    }
    // Load, queue and run the triangular.csv waveform on channel 1
    if (moduleAOU->AWG(1, "Triangular.csv", SD_TriggerModes().AUTOTRIG, 0, 3, 3) < 0)
    {
        std::cout << "Error loading the waveform file 'Triangular.csv', make sure the path is correct. Aborting the Demo..." << std::endl;
        std::cin.get();

        moduleAOU->close();
        return;
    }

    std::cout << "Press enter to quit the demo..." << std::endl;
    std::cin.get();

    moduleAOU->close();
}
