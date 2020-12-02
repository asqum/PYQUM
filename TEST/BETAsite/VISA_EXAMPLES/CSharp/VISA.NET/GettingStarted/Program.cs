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

namespace GettingStarted
{
    class Program
    {
        static void Main(string[] args)
        {
            // Change this variable to the address of your instrument
            string VISA_ADDRESS = "Your instrument's VISA address goes here!";

            // Create a connection (session) to the instrument
            IMessageBasedSession session;
            try
            {
                session = GlobalResourceManager.Open(VISA_ADDRESS) as IMessageBasedSession;
            }
            catch(NativeVisaException visaException)
            {
                Console.WriteLine("Couldn't connect. Error is:\r\n{0}\r\nPress any key to exit...", visaException);
                Console.ReadKey();
                return;
            }

            // Create a formatted I/O object which will help us format the data we want to send/receive to/from the instrument
            MessageBasedFormattedIO formattedIO = new MessageBasedFormattedIO(session);

            // For Serial and TCP/IP socket connections enable the read Termination Character, or read's will timeout
            if (session.ResourceName.Contains("ASRL") || session.ResourceName.Contains("SOCKET"))
                session.TerminationCharacterEnabled = true;

            // Send the *IDN? and read the response as strings
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
