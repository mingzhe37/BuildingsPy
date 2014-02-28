#!/usr/bin/env python
import unittest

class Test_regressiontest_Tester(unittest.TestCase):
    """
       This class contains the unit tests for
       :mod:`buildingspy.regressiontest.Tester`.
    """

    def test_regressiontest(self):
        import os
        import buildingspy.development.regressiontest as r
        rt = r.Tester()
        myMoLib = os.path.join("buildingspy", "tests", "MyModelicaLibrary")
        rt.setLibraryRoot(myMoLib)
        rt.run()
        # Delete temporary files
        os.remove('dymola.log')
        os.remove('unitTests.log')
        
        # Verify that invalid packages raise an OSError.
        rt.setSinglePackage("this.package.does.not.exist")
        self.assertRaises(OSError, rt.run)
        

    def test_runSimulation(self):
        import buildingspy.development.regressiontest as r
        self.assertRaises(OSError, \
                          r.runSimulation, ".", "this_command_does_not_exist")
        
    def test_areResultsEqual(self):
        import buildingspy.development.regressiontest as r
        rt = r.Tester()
        tMin = 10
        tMax = 50
        nPoi = 101
        tOld = [tMin, tMax]
        yOld = [10, 10]
        tNew = [tMin+float(i)/(nPoi-1)*(tMax-tMin) for i in range(nPoi) ]
        yNew = [10.0 for i in range(nPoi)]
        varNam = "testVariable"
        filNam = "testFilename"
        (equ, _, _) = rt.areResultsEqual(tOld, yOld, tNew, yNew, varNam, filNam)
        self.assertTrue(equ, "Test 1 for equality failed.")
        # Test with arguments reversed.
        (equ, _, _) = rt.areResultsEqual(tNew, yNew, tOld, yOld, varNam, filNam)
        self.assertTrue(equ, "Test 2 for equality failed.")
        # Modify arguments, now both tests should return false
        yNew[2] = 11.0 
        (equ, timMaxErr, _) = rt.areResultsEqual(tOld, yOld, tNew, yNew, varNam, filNam)
        self.assertFalse(equ, "Test 1 for equality should have returned false.")
        self.assertEqual(tNew[2], timMaxErr, "Time of maximum error is wrong for test 1.")
        # Test with arguments reversed.
        (equ, timMaxErr, _) = rt.areResultsEqual(tNew, yNew, tOld, yOld, varNam, filNam)
        self.assertFalse(equ, "Test 2 for equality should have returned false.")
        self.assertEqual(tNew[2], timMaxErr, "Time of maximum error is wrong for test 2.")        
        
        # Test the case where the simulation may have failed and hence the end
        # time is smaller than the end time of the reference results
        tNew = [tMin+float(i)/(nPoi-1)*0.9*(tMax-tMin) for i in range(nPoi) ]
        yNew = [10.0 for i in range(nPoi)]
        (equ, timMaxErr, _) = rt.areResultsEqual(tNew, yNew, tOld, yOld, varNam, filNam)        
        self.assertFalse(equ, "Test with smaller simulation end time should have returned false.")
        # Test for different start time
        tNew = [0.1 + tMin+float(i)/(nPoi-1)*(tMax-tMin) for i in range(nPoi) ]
        (equ, timMaxErr, _) = rt.areResultsEqual(tNew, yNew, tOld, yOld, varNam, filNam)        
        self.assertFalse(equ, "Test with smaller simulation start time should have returned false.")

if __name__ == '__main__':
    unittest.main()
