''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' © Keysight Technologies 2016
'
' You have a royalty-free right to use, modify, reproduce And distribute
' the Sample Application Files (And/Or any modified version) in any way
' you find useful, provided that you agree that Keysight Technologies has no
' warranty, obligations Or liability for any Sample Application Files.
'
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Imports System
Imports System.Collections.Generic
Imports System.Text

Imports Ivi.Visa
Imports Ivi.Visa.FormattedIO

Module Module1

    Sub Main()

        ' Change this variable to the address of your instrument
        Dim VISA_ADDRESS As String = "Your instrument's VISA address goes here!"

        ' Create a connection (session) to the RS-232 device. 
        ' Change VISA_ADDRESS to a serial address, e.g. "ASRL1::INSTR"
        Dim session As IMessageBasedSession = GlobalResourceManager.Open(VISA_ADDRESS)

        ' The first thing you should do with a serial port Is enable the Termination Character. Otherwise all of your read's will fail
        session.TerminationCharacterEnabled = True

        ' If you've setup the serial port settings in Connection Expert, you can remove this section. 
        ' Otherwise, set your connection parameters
        Dim serial As ISerialSession = session
        serial.BaudRate = 9600
        serial.DataBits = 8
        serial.Parity = SerialParity.None
        serial.FlowControl = SerialFlowControlModes.DtrDsr

        ' Send the *IDN? And read the response as strings
        Dim FormattedIO As MessageBasedFormattedIO = New MessageBasedFormattedIO(session)
        FormattedIO.WriteLine("*IDN?")
        Dim idnResponse As String = FormattedIO.ReadLine()

        Console.WriteLine("*IDN? returned: {0}", idnResponse)

        ' Close the connection to the instrument
        session.Dispose()

        Console.WriteLine(vbCrLf + "Press any key to exit...")
        Console.ReadKey()

    End Sub

End Module