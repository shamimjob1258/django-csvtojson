import csv, json
import pandas as pd
import os, io
import traceback
from datetime import datetime

class FileConversion2() :
    def __init__(self,file_name) :
        self.filepath = os.getcwd()+"\\csvtonestedjson\\Input\\"
        self.filename = str(file_name)
        self.filetype = str(self.filename).split(".")[-1]
        self.output_list = []
        self.jsonfilename = "output_json_"+datetime.now().strftime("%d-%m-%Y_%H-%M-%S")+".json"
        self.jsonfile = os.getcwd()+"\\csvtonestedjson\\Output\\"+self.jsonfilename
        self.failrecords = os.getcwd()+"\\csvtonestedjson\\Output\\fail_records.txt"
        self.level_count = 0
        self.base_url = ""
        self.header = []

    # Checking if file is valid or not
    def file_type_validation(self) :
        iscsvfile = False
        msg = "File type is not csv"
        if self.filetype == 'csv' :
            iscsvfile = True
            msg = "Valid csv file"
        return {'output_flg' : iscsvfile, 'output_msg' : msg}

    # Checking if file is valid or not
    def file_non_empty(self) :
        isnotempty = False
        msg = "File is empty or with only header line."
        with open(self.filepath+self.filename, 'r') as f:
            header = f.readline()
            try :
                line = next(f)
                while line != None or line != "" :
                    line_list = list(filter(lambda x : x != "" and x != "\n", line.split(",")))
                    if len(line_list) > 0 :
                        isnotempty = True
                        msg = "Valid non empty file"
                        self.base_url = line_list[0]
                        break
                    # line = next(f)
            except StopIteration as e:
                print("StopIteration error handled successfully")
        return {'output_flg' : isnotempty, 'output_msg' : msg}

    # Checking if file structure is correct i.e. first column is base url and after that in group of label, id, link
    def file_structure(self) :
        isvalid = False
        msg = "File Structure is wrong."
        with open(self.filepath+self.filename, 'r') as f:
            reader = f.readline()
            self.header = reader.rstrip().split(",")
            if len(self.header) > 3 and len(self.header[1:])%3 == 0 :
                isvalid = True
                msg = "Valid file structure"
            self.level_count = len(self.header[1:])//3
        return {'output_flg' : isvalid, 'output_msg' : msg}

    # Adding level elements of a line in its position
    def add_line(self, row) :
        process_flg = False
        level = 1
        index = 0
        i = 1
        j = 2
        # obj is json_output instance or its inner children instance
        obj = self.output_list
        link = self.base_url
        # Looping through each level of a line
        while row[i] != "" or row[j] != "" :
            row_label = row[i]
            row_id = row[j]
            found = False

            # if record is invalid skiping this record
            if row_label == "" and row_id == "" :
                process_flg = False
                break

            process_flg = True

            # searching if current level entry already exists or not
            for rec in obj :
                if rec.get('label') == row[i] or rec.get('id') == row[j] :
                    found = True
                    level = level + 1
                    index = obj.index(rec)
                    # obj will refer to its children list for next iteration
                    obj = obj[index].get('children')
                    link = rec.get('link')
                    break
            # From above loop given level already exists than stop this loop and continue next iteration
            if found == True :
                i += 2
                j += 2
                if level > self.level_count:
                    break
                continue
            elif row[i] == "" or row[j] == "" :
                process_flg = False
                break
            # Adding the current level data into obj
            link = link + '/' + row_id
            d = {'label' : row_label, 'id' : row_id, 'link' : link, 'children' : []}
            if level >= self.level_count :
                d.pop('children')
            obj.append(d.copy())
            level = level + 1
            index = obj.index(d)
            # obj will refer to its children list for next iteration
            obj = obj[index].get('children')
            i += 2
            j += 2
            if level > self.level_count:
                break
        return process_flg

    def create_json(self) :
        try :
            get_cols = filter(lambda x : self.header.index(x)%3!=0, self.header)
            df = pd.read_csv(self.filepath+self.filename,dtype=str,usecols=list(get_cols))
            df = df.dropna(axis = 0, how = 'all')
            df = df.drop_duplicates()
            df = df.fillna("")

            # self.write_log('w',"File Process Start","--------------------------------")
            # self.write_log('w',"Dataframe",str(df))
            for row in df.itertuples():
                rec_process = self.add_line(row)
                if rec_process == False :
                    with open(self.failrecords, 'a') as f:
                        f.write(str(list(row)[1:])+'\n')

            with open(str(self.jsonfile),'w') as outfile:
                json.dump(self.output_list, outfile, indent=4)

            return {'data' : self.output_list, 'file' : self.jsonfile}
        except Exception as error:
            print("Exception error -", (traceback.format_exc()))

    # Writing logs for debug purpose
    # def write_log(self,m,context,data) :
    #     with open(os.getcwd()+"\\app1\\Output\\log.txt",m) as outfile:
    #         # outfile.write("\n=========================================")
    #         outfile.write('\n'+context+'\n')
    #         outfile.write(str(data))
