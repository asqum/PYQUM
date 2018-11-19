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

        ' Create a connection (session) to the instrument
        Dim session As IMessageBasedSession
        Try

            session = GlobalResourceManager.Open(VISA_ADDRESS)

        Catch visaException As NativeVisaException

            Console.WriteLine("Couldn't connect. Error is:" + vbCrLf + "{0}" + vbCrLf + "Press any key to exit...", visaException)
            Console.ReadKey()
            Return

        End Try

        ' Create a formatted I/O object which will help us format the data we want to send/receive to/from the instrument
        Dim FormattedIO As MessageBasedFormattedIO = New MessageBasedFormattedIO(session)

        ' For Serial And TCP/IP socket connections enable the read Termination Character, Or read's will timeout
        If session.ResourceName.Contains("ASRL") Or session.ResourceName.Contains("SOCKET") Then
            session.TerminationCharacterEnabled = True
        End If

        ' Send the *IDN? And read the response as strings
        FormattedIO.WriteLine("*IDN?")
        Dim idnResponse As String = FormattedIO.ReadLine()

        Console.WriteLine("*IDN? returned: {0}", idnResponse)

        ' Close the connection to the instrument
        session.Dispose()

        Console.WriteLine(vbCrLf + "Press any key to exit...")
        Console.ReadKey()

    End Sub

End Module


