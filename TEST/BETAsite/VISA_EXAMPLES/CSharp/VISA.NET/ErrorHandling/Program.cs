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

namespace ErrorHandling
{
    class Program
    {
        static void Main(string[] args)
        {
            // Change this variable to the address of your instrument
            string VISA_ADDRESS = "Your instrument's VISA address goes here!";

            IMessageBasedSession session = null;
            MessageBasedFormattedIO formattedIO;

            // Part 1:
            // 
            // Shows the mechanics of how to catch an exception (an error) in VISA.NET when it occurs. 
            // To stimulate an error, the code will try to open a connection t an instrument at an invalid address...
            try
            {
                // First we'll provide an invalid address and see what error we get 
                session = GlobalResourceManager.Open("BAD ADDRESS") as IMessageBasedSession;
            }
            catch (Exception ex)
            {
                Console.WriteLine("An exception has occurred!\r\n\r\n{0}\r\n", ex.ToString());

                // To get more specific information about the exception, we can check what kind of exception it is and add specific error handling code
                // In this example, that is done in the ExceptionHandler method
                ExceptionHandler(ex);
            }

            // Part 2:
            // 
            // Stimulate another error by sending an invalid query and trying to read its response. 
            // 
            // Before running this part, don't forget to set your instrument address in the 'VISA_ADDRESS' variable at the top of this method
            session = GlobalResourceManager.Open(VISA_ADDRESS) as IMessageBasedSession;
            formattedIO = new MessageBasedFormattedIO(session);

            // Misspell the *IDN? query as *IND?
            try
            {
                formattedIO.WriteLine("*IND?");
            }
            catch (Exception ex)
            {
                Console.WriteLine("You'll never get here, because the *IND? data will get sent to the instrument successfully, it's the instrument that won't like it.");
            }

            // Try to read the response (*IND ?)
            try
            {
                string idnResponse = formattedIO.ReadLine();

                Console.WriteLine("*IDN? returned: {0}", idnResponse);
            }
            catch (IOTimeoutException timeoutException)
            {
                Console.WriteLine("The ReadLine call will timeout, because the instrument doesn't know what to do with the command that we sent it.");

                // Check the instrument to see if it has any errors in its queue
                string rawError = "";
                int errorCode = -1;
                string errorString = "";

                while (errorCode != 0)
                {
                    formattedIO.WriteLine("SYST:ERR?");
                    rawError = formattedIO.ReadLine();
                    errorCode = int.Parse(rawError.Split(',')[0]);
                    errorString = rawError.Split(',')[1];

                    Console.WriteLine("Error code: {0}, error message: {1}", errorCode, errorString.Trim());
                }
            }

            session.Dispose();

            Console.WriteLine("\r\nPress any key to exit...");
            Console.ReadKey();

        }

        static void ExceptionHandler(Exception ex)
        {
            // This is an example of accessing VISA.NET exceptions
            if (ex is IOTimeoutException)
            {
                Console.WriteLine("A timeout has occurred!\r\n");
            }
            else if (ex is NativeVisaException)
            {
                Console.WriteLine("A native VISA exception has occurred!\r\n");

                // To get more information about the error look at the ErrorCode property by 
                //     typecasting the generic exception to the more-specific Native VISA Exception    
                int errorCode = (ex as NativeVisaException).ErrorCode;
                Console.WriteLine("\r\n\tError code: {0}\r\n\tError name: {1}\r\n",
                    errorCode,
                    NativeErrorCode.GetMacroNameFromStatusCode(errorCode));
            }
            else if (ex is VisaException)
            {
                Console.WriteLine("A VISA exception has occurred!\r\n");
            }
            else
            {
                Console.WriteLine("Some other type of exception occurred: {0}\r\n", ex.GetType());
            }
        }
    }
}
