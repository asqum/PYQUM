''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
' © Keysight Technologies 2016
'
' You have a royalty-free right to use, modify, reproduce And distribute
' the Sample Application Files (And'Or any modified version) in any way
' you find useful, provided that you agree that Keysight Technologies has no
' warranty, obligations Or liability for any Sample Application Files.
'
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Imports Ivi.Visa
Imports Ivi.Visa.FormattedIO

Module Module1

    Sub Main()

        ' Change this variable to the address of your instrument
        Dim VISA_ADDRESS As String = "Your instrument's VISA address goes here!"

        ' Create a connection (session) to the TCP/IP socket on the instrument. 
        ' Change VISA_ADDRESS to a SOCKET address, e.g. "TCPIP::169.254.104.59::5025::SOCKET"
        Dim session As IMessageBasedSession = GlobalResourceManager.Open(VISA_ADDRESS)

        ' The first thing you should do with a SOCKET connection Is enable the Termination Character. Otherwise all of your read's will fail
        session.TerminationCharacterEnabled = True

        ' We can find out details of the connection
        Dim socket As ITcpipSocketSession = session

        Console.WriteLine("IP: {0}" + vbCrLf + "Hostname: {1}" + vbCrLf + "Port: {2}" + vbCrLf,
            socket.Address,
            socket.HostName,
            socket.Port)

        ' Send the *IDN? And read the response as strings
        Dim FormattedIO As New MessageBasedFormattedIO(session)
        FormattedIO.WriteLine("*IDN?")
        Dim idnResponse As String = FormattedIO.ReadLine()

        Console.WriteLine("*IDN? returned: {0}", idnResponse)

        ' Close the connection to the instrument
        session.Dispose()

        Console.WriteLine(vbCrLf + "Press any key to exit...")
        Console.ReadKey()

    End Sub

End Module
