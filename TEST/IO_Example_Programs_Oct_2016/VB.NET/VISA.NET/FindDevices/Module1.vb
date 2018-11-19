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

        Dim devices As IEnumerable(Of String)
        Try

            ' Finding all devices And interfaces Is straightforward
            Console.WriteLine("Find all devices and interfaces:")
            devices = GlobalResourceManager.Find()

            For Each device As String In devices

                Console.WriteLine(vbTab + "Address: {0}, Alias: {1}", device, GlobalResourceManager.Parse(device).AliasIfExists)

            Next

        Catch ex As VisaException

            Console.WriteLine("Didn't find any devices!")

        End Try

        Console.WriteLine()

        ' You can specify other device types using different search strings. Here are some common examples

        ' All instruments (no INTFC, BACKPLANE Or MEMACC)
        Find("?*INSTR")
        ' PXI modules
        Find("PXI?*INSTR")
        ' USB devices
        Find("USB?*INSTR")
        ' GPIB instruments
        Find("GPIB?*")
        ' GPIB interfaces
        Find("GPIB?*INTFC")
        ' GPIB instruments on the GPIB0 interface
        Find("GPIB0?*INSTR")
        ' LAN instruments
        Find("TCPIP?*")
        ' SOCKET (:SOCKET) instruments
        Find("TCPIP?*SOCKET")
        ' VXI-11 (inst) instruments
        Find("TCPIP?*inst?*INSTR")
        ' HiSLIP (hislip) instruments
        Find("TCPIP?*hislip?*INSTR")
        ' RS-232 instruments
        Find("ASRL?*INSTR")

        Console.WriteLine(vbCrLf + "Press any key to exit...")
        Console.ReadKey()

    End Sub

    Sub Find(searchString As String)

        Dim devices As IEnumerable(Of String)
        Try

            Console.WriteLine("Find with search string """ + searchString + """")
            devices = GlobalResourceManager.Find(searchString)

            For Each device As String In devices
                Console.WriteLine(vbTab + "Address: {0}, Alias: {1}", device, GlobalResourceManager.Parse(device).AliasIfExists)
            Next

        Catch ex As VisaException
            Console.WriteLine("... didn't find anything!")
        End Try

        Console.WriteLine()

    End Sub

End Module