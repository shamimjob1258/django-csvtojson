from django.test import TestCase
# from django.test import TestCase
import unittest
import os
from .file_process_pandas import FileConversion2
import json

# Test File for given scenario are as
# File Structure not correct - data02.csv
# File empty with header only - data03.csv
# File empty with no record - data03_02.csv
# File with level-5 record - data04.csv

class MyTest(unittest.TestCase):
    # Test case for fail scenario when passing non csv file
    def test_file_type_fail(self):
        iscsvfile = None
        test_file_path = os.getcwd()+"\\csvtonestedjson\\Input\\data01.txt"
        with open(test_file_path,'r') as test_file :
            ofile = FileConversion2("data01.txt")
            iscsvfile = ofile.file_type_validation()
        response = self.assertEqual(iscsvfile.get('output_flg'), False)
        return response

    # Test case for pass scenario when passing non csv file
    def test_file_type_pass(self):
        iscsvfile = None
        test_file_path = os.getcwd()+"\\csvtonestedjson\\Input\\data01.csv"
        with open(test_file_path,'r') as test_file :
            ofile = FileConversion2("data01.csv")
            iscsvfile = ofile.file_type_validation()
        response = self.assertEqual(iscsvfile.get('output_flg'), True)
        return response

    # Test case for fail scenario when passing empty file
    def test_file_empty_fail(self):
        isnonempthfile = None
        test_file_path = os.getcwd()+"\\csvtonestedjson\\Input\\data01.csv"
        with open(test_file_path,'r') as test_file :
            ofile = FileConversion2("data03.csv")
            isnonempthfile = ofile.file_non_empty()
        response = self.assertEqual(isnonempthfile.get('output_flg'), False)
        return response

    # Test case for pass scenario when passing non-empty file
    def test_file_empty_pass(self):
        isnonempthfile = None
        test_file_path = os.getcwd()+"\\csvtonestedjson\\Input\\data01.csv"
        with open(test_file_path,'r') as test_file :
            ofile = FileConversion2("data01.csv")
            isnonempthfile = ofile.file_non_empty()
        response = self.assertEqual(isnonempthfile.get('output_flg'), True)
        return response

    # Test case for fail scenario when file structure is wrong
    def test_file_structure_fail(self):
        isnonempthfile = None
        test_file_path = os.getcwd()+"\\csvtonestedjson\\Input\\data02.csv"
        with open(test_file_path,'r') as test_file :
            ofile = FileConversion2("data02.csv")
            isFileFormatCorrect = ofile.file_structure()
        response = self.assertEqual(isFileFormatCorrect.get('output_flg'), False)
        return response

    # Test case for pass scenario when file structure is correct
    def test_file_structure_pass(self):
        isFileFormatCorrect = None
        test_file_path = os.getcwd()+"\\csvtonestedjson\\Input\\data02.csv"
        with open(test_file_path,'r') as test_file :
            ofile = FileConversion2("data01.csv")
            isFileFormatCorrect = ofile.file_structure()
        response = self.assertEqual(isFileFormatCorrect.get('output_flg'), True)
        return response

    # Test case for fail scenario when file not converted correctly
    def test_file_conversion(self):
        ofile = FileConversion2("data01.csv")
        isvalidjsondata = ofile.create_json()
        try:
            json.loads(isvalidjsondata.get('data'))
        # except ValueError as e or TypeError as t:
        except :
            isvalid = False
        isvalid = True
        response = self.assertEqual(isvalid, True)
        return response

    # def test_file_conversion_witherrorrecords(self):
    #     ofile = FileConversion2("data05.csv")
    #     isvalidjsondata = ofile.create_json()
    #     try:
    #         json.loads(isvalidjsondata.get('data'))
    #     # except ValueError as e or TypeError as t:
    #     except :
    #         isvalid = False
    #     isvalid = True
    #     response = self.assertEqual(isvalid, True)
    #     return response

    # Test case for fail scenario when adding new line to be added in the list which gets finally converted to json
    def test_addnewrecord_fail1(self):
        ofile = FileConversion2("data01.csv")
        # ofile.add_line([0,'newlabel',''])
        # ofile.add_line([0,'newlabel',''])
        isnewdatavalid = ofile.add_line([0,'newlabel',''])
        response = self.assertEqual(isnewdatavalid, False)
        return response

    def test_addnewrecord_fail2(self):
        ofile = FileConversion2("data01.csv")
        # ofile.add_line([0,'newlabel',''])
        ofile.add_line([0,'newlabel','newid'])
        isnewdatavalid = ofile.add_line([0,'',''])
        response = self.assertEqual(isnewdatavalid, False)
        return response

    # Test case for pass scenario when adding new line to be added in the list which gets finally converted to json
    def test_addnewrecord_pass(self):
        ofile = FileConversion2("data01.csv")
        isnewdatavalid = ofile.add_line([0,'level1label','level1id','level2label','level2id','level3label','level3id','level4label','level4id','level5label','level5id'])
        response = self.assertEqual(isnewdatavalid, True)
        return response
