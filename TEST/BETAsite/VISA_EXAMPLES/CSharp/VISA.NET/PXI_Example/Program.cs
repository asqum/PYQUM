////////////////////////////////////////////////////////////////////////////////
// © Keysight Technologies 2016
//
// You have a royalty-free right to use, modify, reproduce and distribute
// the Sample Application Files (and/or any modified version) in any way
// you find useful, provided that you agree that Keysight Technologies has no
// warranty, obligations or liability for any Sample Application Files.
//
////////////////////////////////////////////////////////////////////////////////

using System;
using System.Collections.Generic;
using System.Text;

using Ivi.Visa;
using Ivi.Visa.FormattedIO;

namespace PXI_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            // Change this variable to the address of your instrument
            string VISA_ADDRESS = "Your instrument's VISA address goes here!";

            // Create a connection (session) to the PXI module 
            // Change VISA_ADDRESS to a PXI address, e.g. "PXI0::23-0.0::INSTR"
            IPxiSession session = GlobalResourceManager.Open(VISA_ADDRESS) as IPxiSession;

            Console.WriteLine("Manufacturer: {0}\r\nModel: {1}\r\nChassis: {2}\r\nSlot: {3}\r\nBus-Device.Function: {4}-{5}.{6}\r\n",
                session.ManufacturerName,
                session.ModelName,
                session.ChassisNumber,
                session.Slot,
                session.BusNumber,
                session.DeviceNumber,
                session.FunctionNumber);

            // Close the connection to the instrument
            session.Dispose();

            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
