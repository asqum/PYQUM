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

        Dim session As IMessageBasedSession
        Dim formattedIO As MessageBasedFormattedIO

        ' Part 1
        ' 
        ' Shows the mechanics of how to catch an exception (an error) in VISA.NET when it occurs. 
        ' To stimulate an error, the code will try to open a connection t an instrument at an invalid address...
        Try

            ' First we'll provide an invalid address and see what error we get 
            session = GlobalResourceManager.Open("BAD ADDRESS")

        Catch ex As Exception

            Console.WriteLine("An exception has occurred!" + vbCrLf + vbCrLf + "{0}" + vbCrLf, ex.ToString())

            ' To get more specific information about the exception, we can check what kind of exception it Is And add specific error handling code
            ' In this example, that Is done in the ExceptionHandler method
            ExceptionHandler(ex)

        End Try


        ' Part 2
        ' 
        ' Stimulate another error by sending an invalid query And trying to read its response. 
        ' 
        ' Before running this part, don't forget to set your instrument address in the 'VISA_ADDRESS' variable at the top of this method
        session = GlobalResourceManager.Open(VISA_ADDRESS)
        formattedIO = New MessageBasedFormattedIO(session)

        ' Misspell the *IDN? query as *IND?
        Try

            formattedIO.WriteLine("*IND?")

        Catch ex As Exception

            Console.WriteLine("You'll never get here, because the *IND? data will get sent to the instrument successfully, it's the instrument that won't like it.")

        End Try


        ' Try to read the response (*IND ?)
        Try

            Dim idnResponse As String = formattedIO.ReadLine()
            Console.WriteLine("*IDN? returned: {0}", idnResponse)

        Catch timeoutException As IOTimeoutException

            Console.WriteLine("The ReadLine call will timeout, because the instrument doesn't know what to do with the command that we sent it.")

            ' Check the instrument to see if it has any errors in its queue
            Dim rawError As String = ""
            Dim errorCode As Integer = -1
            Dim errorString As String = ""

            While errorCode <> 0

                formattedIO.WriteLine("SYST:ERR?")
                rawError = formattedIO.ReadLine()
                errorCode = Integer.Parse(rawError.Split(",")(0))
                errorString = rawError.Split(",")(1)

                Console.WriteLine("Error code: {0}, error message: {1}", errorCode, errorString.Trim())

            End While
        End Try

        session.Dispose()

        Console.WriteLine(vbCrLf + "Press any key to exit...")
        Console.ReadKey()

    End Sub

    Sub ExceptionHandler(ex As Exception)

        ' This Is an example of accessing VISA.NET exceptions
        If TypeOf ex Is IOTimeoutException Then

            Console.WriteLine("A timeout has occurred!" + vbCrLf)

        ElseIf TypeOf ex Is NativeVisaException Then

            Console.WriteLine("A native VISA exception has occurred!" + vbCrLf)

            ' To get more information about the error look at the ErrorCode property by 
            '     typecasting the generic exception to the more-specific Native VISA Exception    
            Dim errorCode As Integer = DirectCast(ex, NativeVisaException).ErrorCode
            Console.WriteLine(vbCrLf + vbTab + "Error code: {0}" + vbCrLf + vbTab + "Error name: {1}" + vbCrLf,
                errorCode,
                NativeErrorCode.GetMacroNameFromStatusCode(errorCode))

        ElseIf TypeOf ex Is VisaException Then

            Console.WriteLine("A VISA exception has occurred!" + vbCrLf)

        Else

            Console.WriteLine("Some other type of exception occurred: {0}" + vbCrLf, ex.GetType())

        End If

    End Sub

End Module