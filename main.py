import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import statistics




def convert_grade(grade):
    if grade == 'A':
        return 4.0
    elif grade == 'A-':
        return 3.7
    elif grade == 'B+':
        return 3.3
    elif grade == 'B':
        return 3.0
    elif grade == 'B-':
        return 2.7
    elif grade == 'C+':
        return 2.3
    elif grade == 'C':
        return 2.0
    elif grade == 'C-':
        return 1.7
    elif grade == 'D+':
        return 1.3
    elif grade == 'D':
        return 1.0
    elif grade == 'D-':
        return 0.7
    elif grade == 'F':
        return 0.0
    else:
        return 0.0
def getData(df):
    df.drop(0)
    df.columns = ['Data']
    df = df.drop(0)
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df[~df["Grade"].str.contains("I|W")]
    return df
def getGPA():
    df = pd.read_csv(filepath, sep='|', header=None)
    df.drop(0)
    df.columns = ['Data']
    df = df.drop(0)
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df[~df["Grade"].str.contains("I|W")]
    df['Numerical Grade'] = df['Grade'].apply(convert_grade)
    avg_numerical_grade = df['Numerical Grade'].mean()
    return avg_numerical_grade

def getSECGPAdf(df):
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df[~df["Grade"].str.contains("I|W")]
    df['Numerical Grade'] = df['Grade'].apply(convert_grade)
    avg_numerical_grade = df['Numerical Grade'].mean()
    return avg_numerical_grade

def num_grades(keys):
    line = []
    linef = []
    with open(keys, "r") as f:
        sections = f.readlines()
    sections.pop(0)

    for x in range(len(sections)):
        sections[x] = sections[x].strip()
        with open(sections[x], "r") as f:
            lines = f.readlines()
            lines.pop(0)
            linef.extend(lines)
    for x in range (len(linef)):
        linef[x] = linef[x].strip()


    df = pd.DataFrame(linef)
    df.drop(0)
    df.columns = ['Data']
    df = df.drop(0)
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df.drop('Data', axis=1)
    df['GPA'] = df['Grade'].apply(convert_grade)
    df = df[~df["Grade"].str.contains("I|W|P|NP")]
    grades = df['Grade'].tolist()
    grades
    order = ['A','A-','B+', 'B','B-', 'C','C-', 'D', 'F']
    counts = [grades.count(grade) for grade in order]
    output_list = [f"{grade}: {count}" for grade, count in zip(order, counts) if count > 0]
    output_string = ", ".join(output_list)
    return output_string

def getSTDEV(keys):
    lines = []
    linef = []
    with open(keys, "r") as f:
        sections = f.readlines()
        sections.pop(0)

        for x in range(len(sections)):
            sections[x] = sections[x].strip()
            with open(sections[x], "r") as f:
                lines = f.readlines()
                lines.pop(0)
                linef.extend(lines)
    for x in range(len(linef)):
        linef[x] = linef[x].strip()

    df = pd.DataFrame(linef)
    df.drop(0)
    df.columns = ['Data']
    df = df.drop(0)
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df.drop('Data', axis=1)
    df['GPA'] = df['Grade'].apply(convert_grade)
    df = df[~df["Grade"].str.contains("I|W|P|NP")]

    grades = df['GPA'].tolist()
    std_dev = statistics.stdev(grades)

    return std_dev

def get_GRP_GPA(keys):
    gpa_list = []

    with open(keys, "r") as f:
        sections = f.readlines()
    sections.pop(0)

    for y in range(len(sections)):
        sections[y] = sections[y].strip()
        with open(sections[y], "r") as f:
            lines = f.readlines()
        lines.pop(0)
        for j in range(len(lines)):
            lines[j] = lines[j].strip()
        df = pd.DataFrame(lines, columns=['Data'])
        gpa = (getSECGPAdf(df))
        gpa_list.append(gpa)
        average = sum(gpa_list) / len(gpa_list)
    return average
def get_sec_gpa(keys):
    with open(keys, "r") as f:
        sections = f.readlines()
        sections.pop(0)
    for x in range(len(sections)):
            sections[x] = sections[x].strip()
    value = app.get_selection2()
    with open(sections[value], "r") as f:
        lines = f.readlines()
        lines.pop(0)
    for j in range(len(lines)):
        lines[j] = lines[j].strip()
    df = pd.DataFrame(lines)
    df.columns = ['Data']
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df[~df["Grade"].str.contains("I|W|P|NP")]
    df['Numerical Grade'] = df['Grade'].apply(convert_grade)
    avg_numerical_grade = df['Numerical Grade'].mean()
    return avg_numerical_grade

def get_z_score(keys):
    stdev = getSTDEV(keys)
    grp_gpa = get_GRP_GPA(keys)
    sec_gpa = get_sec_gpa(keys)
    result = (sec_gpa - grp_gpa)/stdev
    return result

def create_dict(path):
    group_files = {}
    with open(path, "r") as f:
        groups = f.readlines()
    groups.pop(0)

    #Add the GRP files from RUN file
    for i in range(len(groups)):
        groups[i] = groups[i].strip()
        group_files[groups[i]] = {}
    keys = list(group_files.keys())
    for x in range (len(keys)):
        group_files[keys[x]]["Number of Courses"] = (num_courses(keys[x]))
        group_files[keys[x]]["Number of Students"] = (num_students(keys[x]))
        group_files[keys[x]]["Average GPA"] = (get_GRP_GPA(keys[x]))
        group_files[keys[x]]["Number of Grades"] = (num_grades(keys[x]))

    return group_files

def num_courses(keys):

    with open(keys, "r") as f:
        sections = f.readlines()
    sections.pop(0)
    for y in range(len(sections)):
        sections[y] = sections[y].strip()
        sections[y] = sections[y][:-7]

    count = len(set(sections))
    return count

def num_students(keys):
    count = 0
    with open(keys, "r") as f:
        sections = f.readlines()
    sections.pop(0)
    for i in range(len(sections)):
        sections[i] = sections[i].strip()

    for x in range(len(sections)):
        with open(sections[x], "r") as f:
            lines = f.readlines()
        lines.pop(0)
        length = len(lines)
        count = length + count
    return count

#create_dict("TESTRUN.RUN")

def writeReport(group_files):
    keys = list(group_files.keys())

    for x in range (len(keys)):
        group_files[keys[x]]["Number of Courses"] = (num_courses(keys[x]))
        group_files[keys[x]]["Number of Students"] = (num_students(keys[x]))
        group_files[keys[x]]["Average GPA"] = (get_GRP_GPA(keys[x]))
        group_files[keys[x]]["Number of Grades"] = (num_grades(keys[x]))

    return group_files

def getSections(keys):
    with open(keys, "r") as f:
        sections = f.readlines()
        sections.pop(0)
        for i in range(len(sections)):
            sections[i] = sections[i].strip()
    return sections

"""
#print(getGPA(pd.read_csv(openFile(), sep='|', header=None)))
#Root
root = Tk()
root.title("GPA Calculator")
root.geometry("500x800")

#Button that Opens File explorer
button = Button(text = "Open", command = openFile)

#TextBox that displays the chosen file

textbox = Text(root,height=5, width=30)


button.pack()
textbox.pack()
root.mainloop()
"""


class root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPA Calculator")
        self.geometry("800x800")

        #Create search button
        self.button = Button(self, text = "Open RUN", command = self.openFile)
        self.button.place(x=300, y=20, width=75, height=50)

        # Create calculate button
        self.button = Button(self, text="Calculate", command = self.calc)
        self.button.place(x=375, y=100, width=75, height=50)

        #Create an open button to open the GRP
        self.button2 = Button(self, text="Open GRP", command = self.showSEC)
        self.button2.place(x=300, y=100, width=75, height=50)

        # Create an open button to calc the z_score
        self.button3 = Button(self, text="Z-Score", command=self.show_z_score)
        self.button3.place(x=300, y=180, width=75, height=50)

        #Create textbox that holds the file path
        self.textbox = Text(self, height=5, width=30)
        self.textbox.place(x=10, y=20, width=250, height=50)

        # Create textbox2 for idk
        self.textbox2 = Text(self, height=5, width=30)
        self.textbox2.place(x=500, y=180, width=250, height=50)

        #Create textbox for output of dictionary
        self.textbox3 = Text(self, height=40, width=40)
        self.textbox3.place(x=500, y=20, width=250, height=150)
        self.grp = tk.StringVar()
        #Create List Box that stores the GRP files
        self.list = Listbox(self,exportselection=False)
        self.list.place(x=10, y=100, width=250, height=50)

        # Create List Box that stores the SEC files
        self.list2 = Listbox(self,exportselection=False)
        self.list2.place(x=10, y=180, width=250, height=50)
        #keys = self.getKeys()
        #for item in keys:
        #    self.drop["menu"].add_command(label=item, command= self._setit(grp, item))

    def writeRep2(group_files):
        keys = list(group_files.keys())
        values = group_files[keys[0]]

        for key, value in values.items():
            print(key + ': ' + str(value))

    def openFile(self):
        filepath = filedialog.askopenfilename()
        s1 = "\\"
        s2 = "/"
        filepath = filepath.replace(s1, s2)
        self.textbox.delete(1.0, END)
        self.textbox.insert(END, filepath)
        self.list.delete(0, END)


        group_files = {}

        with open(filepath, "r") as f:
            groups = f.readlines()
        groups.pop(0)

        # Add the GRP files from RUN file
        for i in range(len(groups)):
            groups[i] = groups[i].strip()
            group_files[groups[i]] = {}
        keys = list(group_files.keys())

        for element in keys:
            self.list.insert(tk.END, element)

    def get_selection(self):
        selection = self.list.curselection()
        if selection:
            return int(selection[0])
        else:
            return None
    def get_selection2(self):
        selection = self.list2.curselection()
        if selection:
            return int(selection[0])
        else:
            return None
    def getFilePath(self):
        value=self.textbox.get("1.0","end-1c")
        return value

    def getKeys(self):
        group_files = {}
        path = self.getFilePath()
        with open(path, "r") as f:
            groups = f.readlines()
        groups.pop(0)

        # Add the GRP files from RUN file
        for i in range(len(groups)):
            groups[i] = groups[i].strip()
            group_files[groups[i]] = {}
        keys = list(group_files.keys())
        return keys

    def getKeys2(self):
        group_files = {}
        path = self.getFilePath()
        with open(path, "r") as f:
            groups = f.readlines()
        groups.pop(0)

        # Add the GRP files from RUN file
        for i in range(len(groups)):
            groups[i] = groups[i].strip()
            group_files[groups[i]] = {}
        pre_key = list(group_files.keys())

        with open(pre_key[0], "r") as f:
            sections = f.readlines()
            sections.pop(0)
        for x in range(len(sections)):
            sections[x] = sections[x].strip()
        keys = sections
        return keys




    def calc(self):
        self.group_files = create_dict(self.getFilePath())
        keys = list(self.group_files.keys())
        selc = self.get_selection()
        values = self.group_files[keys[selc]]
        self.textbox3.delete(1.0, END)
        for key, value in values.items():
            self.textbox3.insert(END, (key + ': ' + str(value) + '\n'))
    def showSEC(self):
        keys = self.getKeys()
        selc = self.get_selection()
        sections = getSections(keys[selc])
        self.list2.delete(0, END)
        for section in sections:
            self.list2.insert(tk.END, section)
    def show_z_score(self):
        self.textbox2.delete(1.0, END)

        keys1 = self.getKeys()
        #keys2 = self.getKeys2()
        selc1 = self.get_selection()
        #selc2 = self.get_selection2()

        result = get_z_score(keys1[selc1])
        self.textbox2.insert(tk.END, result)

if __name__ == "__main__":

    app = root()
    app.mainloop()