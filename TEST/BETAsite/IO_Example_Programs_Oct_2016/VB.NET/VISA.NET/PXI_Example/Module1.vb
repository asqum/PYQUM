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

        ' Create a connection (session) to the PXI module 
        ' Change VISA_ADDRESS to a PXI address, e.g. "PXI0::23-0.0::INSTR"
        Dim session As IPxiSession = GlobalResourceManager.Open(VISA_ADDRESS)

        Console.WriteLine("Manufacturer: {0}" + vbCrLf + "Model: {1}" + vbCrLf + "Chassis: {2}" + vbCrLf + "Slot: {3}" + vbCrLf + "Bus-Device.Function: {4}-{5}.{6}" + vbCrLf,
                session.ManufacturerName,
                session.ModelName,
                session.ChassisNumber,
                session.Slot,
                session.BusNumber,
                session.DeviceNumber,
                session.FunctionNumber)

        ' Close the connection to the instrument
        session.Dispose()

        Console.WriteLine(vbCrLf + "Press any key to exit...")
        Console.ReadKey()

    End Sub

End Module