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

namespace FindDevices
{
    class Program
    {
        static void Main(string[] args)
        {
            IEnumerable<string> devices;
            try
            {
                // Finding all devices and interfaces is straightforward
                Console.WriteLine("Find all devices and interfaces:");
                devices = GlobalResourceManager.Find();

                foreach (string device in devices)
                {
                    Console.WriteLine("\tAddress: {0}, Alias: {1}", device, GlobalResourceManager.Parse(device).AliasIfExists);
                }
            }
            catch (VisaException ex)
            {
                Console.WriteLine("Didn't find any devices!");
            }
            Console.WriteLine();

            // You can specify other device types using different search strings. Here are some common examples:
            
            // All instruments (no INTFC, BACKPLANE or MEMACC)
            Find("?*INSTR");
            // PXI modules
            Find("PXI?*INSTR");
            // USB devices
            Find("USB?*INSTR");
            // GPIB instruments
            Find("GPIB?*");
            // GPIB interfaces
            Find("GPIB?*INTFC");
            // GPIB instruments on the GPIB0 interface
            Find("GPIB0?*INSTR");
            // LAN instruments
            Find("TCPIP?*");
            // SOCKET (::SOCKET) instruments
            Find("TCPIP?*SOCKET");
            // VXI-11 (inst) instruments
            Find("TCPIP?*inst?*INSTR");
            // HiSLIP (hislip) instruments
            Find("TCPIP?*hislip?*INSTR");
            // RS-232 instruments
            Find("ASRL?*INSTR");

            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }

        static void Find(string searchString)
        {
            IEnumerable<string> devices;
            try
            {
                Console.WriteLine("Find with search string \"" + searchString + "\"");
                devices = GlobalResourceManager.Find(searchString);

                foreach (string device in devices)
                {
                    Console.WriteLine("\tAddress: {0}, Alias: {1}", device, GlobalResourceManager.Parse(device).AliasIfExists);
                }
            }
            catch (VisaException ex)
            {
                Console.WriteLine("... didn't find anything!");
            }
            Console.WriteLine();
        }
    }
}
