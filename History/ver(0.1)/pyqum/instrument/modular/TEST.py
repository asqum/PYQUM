# For TESTING of ALL Modular

from pyqum.instrument.modular import AWG
import time#, AWG
from colorama import init, Fore, Back
init(autoreset=True)

# print(AWG.active_marker.__doc__) #Help DocStrings

def run():
    start = time.time()

    print("location of '2':", id(2))
    print("location of '4':", id(4))
    print("location of '6':", id(6))
    print("location of '8':", id(8))

    def INIT():
        initstatus, session= AWG.InitWithOptions()
        print(Fore.GREEN + "\nAWG is initialized at session: %s, Error: %s" %(session, initstatus)) #status=0 means no error
        print(Fore.YELLOW + "location of session:", id(session))
        return session

    def MODEL(session):
        wrapped = AWG.model(session)
        print(Fore.BLACK + Back.WHITE + "Inquired instrument's model: %s, Error: %s" % (wrapped[1], wrapped[0]))
        return

    # Testing Get/Set String
    def MARK(session):
        wrapped = AWG.active_marker(session)
        print(Fore.RED + "\nActive marker(physical name): %s, Error: %s" % (wrapped[1], wrapped[0]))
        wrapped = AWG.active_marker(session, action=["Set", "3"])
        print(Fore.MAGENTA + "SET Active marker(physical name): %s, Error: %s" % (wrapped[1], wrapped[0]))
        wrapped = AWG.active_marker(session)
        print(Fore.RED + "Active marker(physical name): %s, Error: %s" % (wrapped[1], wrapped[0]))
        return

    # Testing Get String
    def NAME(session):
        wrapped = AWG.logical_name(session)
        print(Fore.CYAN + "\nLogical Name: %s, Error: %s" % (wrapped[1], wrapped[0]))
        name = wrapped[1]
        return name

    # Testing Get String
    def RESOURC(session):
        wrapped = AWG.resource_descriptor(session)
        print(Fore.RED + Back.YELLOW + "\nResource Descriptor: %s, Error: %s" % (wrapped[1], wrapped[0]))
        return

    # Testing Get/Set Int32
    def SOURC(session):
        wrapped = AWG.marker_source(session)
        print(Fore.BLUE + Back.CYAN + "\nmarker source: %s, Error: %s" % (wrapped[1], wrapped[0]))
        wrapped = AWG.marker_source(session, action=["Set", 10])
        print(Fore.CYAN + Back.BLUE + "SET marker source: %s, Error: %s" % (wrapped[1], wrapped[0]))
        wrapped = AWG.marker_source(session)
        print(Fore.BLUE + Back.CYAN + "marker source: %s, Error: %s" % (wrapped[1], wrapped[0]))
        return

    # Testing Get/Set Real64
    def DELAY(session):
        wrapped = AWG.marker_delay(session)
        print("\nmarker delay: %s, Error: %s" % (wrapped[1], wrapped[0]))
        wrapped = AWG.marker_delay(session, action=["Set", 5e-7])
        print("SET marker delay: %s, Error: %s" % (wrapped[1], wrapped[0]))
        wrapped = AWG.marker_delay(session)
        print("marker delay: %s, Error: %s" % (wrapped[1], wrapped[0]))

    def CLOS(session):
        closestatus = AWG.close(session)
        print(Fore.RED + "\nAWG is closed. Error: %s" % closestatus)

    s = INIT()
    n = NAME(s)

    MODEL(n)
    
    RESOURC(s)
    MARK(s)
    SOURC(s)
    DELAY(s)
    CLOS(s)

    for i in range(0):
        initstatus, s= AWG.InitWithOptions()
        print("\nAWG is initialized at session: %s, Error: %s" %(s, initstatus))
        print("location of session:", id(s))
        closestatus = AWG.close(s)
        print("\nAWG is closed. Error: ", closestatus)

    end = time.time()
    duration = end - start
    print("\nIt took {:.5f}s to complete".format(duration))

run()



