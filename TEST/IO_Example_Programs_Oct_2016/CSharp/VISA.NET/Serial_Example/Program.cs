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

namespace Serial_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            // Change this variable to the address of your instrument
            string VISA_ADDRESS = "Your instrument's VISA address goes here!";

            // Create a connection (session) to the RS-232 device. 
            // Change VISA_ADDRESS to a serial address, e.g. "ASRL1::INSTR"
            IMessageBasedSession session = GlobalResourceManager.Open(VISA_ADDRESS) as IMessageBasedSession;

            // The first thing you should do with a serial port is enable the Termination Character. Otherwise all of your read's will fail
            session.TerminationCharacterEnabled = true;

            // If you've setup the serial port settings in Connection Expert, you can remove this section. 
            // Otherwise, set your connection parameters
            ISerialSession serial = session as ISerialSession;
            serial.BaudRate = 9600;
            serial.DataBits = 8;
            serial.Parity = SerialParity.None;
            serial.FlowControl = SerialFlowControlModes.DtrDsr;

            // Send the *IDN? and read the response as strings
            MessageBasedFormattedIO formattedIO = new MessageBasedFormattedIO(session);
            formattedIO.WriteLine("*IDN?");
            string idnResponse = formattedIO.ReadLine();

            Console.WriteLine("*IDN? returned: {0}", idnResponse);

            // Close the connection to the instrument
            session.Dispose();

            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
