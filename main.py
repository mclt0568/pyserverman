from global_modules import *
import tester
import sys

if __name__ == "__main__":

    # TESTS
    if "--test" in sys.argv or "-t" in sys.argv:
        tester.test_main(sys.argv)
