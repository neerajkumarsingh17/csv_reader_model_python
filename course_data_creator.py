__author__ = 'Neeraj Kumar'
import sys, csv, os, xlrd, json
from django.core.management.base import BaseCommand
from dashboards.user_dashboard.models import Course

loc = ("/home/manprax/dashboard/Slides_per_section.csv")



class Command(BaseCommand):
    """
    This is used pushing data to mongodb
    Remark: Don't change any line of code without discussion
    """
    args = ''
    help = 'Used For Push data from API to Mongodb'

    # workbook = xlrd.open_workbook("Slides_per_section.xlsx")
    # sheet = workbook.sheet_by_index(0)

    def handle(self, *args, **options):
        """
        :param args:
        :param options:
        :return:
        """
        self.stdout.write("===> Operation Start ===>")
        data_dict = {}
        with open(loc, "r") as inputFile:
            cvsReader = csv.reader(inputFile)
            next(cvsReader, None)  # skip the header row
            try:
                index=1
                cvsReader=list(cvsReader)
                while index<len(cvsReader)-1:
                    course = Course()
                    course.course_name=cvsReader[index][0]
                    course.slides_count=cvsReader[index][3]
                    data=[{'sub-section':int(cvsReader[index][2]),'display_name':cvsReader[index][1],"section":1}]
                    for i,j in enumerate(cvsReader[(index+1):]):
                        dict={}
                        if(cvsReader[index][0]==j[0]):
                            dict['section']=i+2
                            dict['sub-section']=int(j[2])
                            dict['display_name']=j[1]
                            data.append(dict)
                            index+=1
                            continue
                        else:
                            index+=1
                            break
                    course.section_input=data
                    course.save()
            except Exception as e:
                print("Exception here====>",e)
        self.stdout.write("===> Operation Done ===>")
