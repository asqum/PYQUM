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

namespace Socket_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            // Change this variable to the address of your instrument
            string VISA_ADDRESS = "Your instrument's VISA address goes here!";

            // Create a connection (session) to the TCP/IP socket on the instrument. 
            // Change VISA_ADDRESS to a SOCKET address, e.g. "TCPIP::169.254.104.59::5025::SOCKET"
            IMessageBasedSession session = GlobalResourceManager.Open(VISA_ADDRESS) as IMessageBasedSession;

            // The first thing you should do with a SOCKET connection is enable the Termination Character. Otherwise all of your read's will fail
            session.TerminationCharacterEnabled = true;

            // We can find out details of the connection
            ITcpipSocketSession socket = session as ITcpipSocketSession;
            Console.WriteLine("IP: {0}\r\nHostname: {1}\r\nPort: {2}\r\n",
                socket.Address,
                socket.HostName,
                socket.Port);

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
