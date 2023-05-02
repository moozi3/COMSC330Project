from tkinter.ttk import Treeview

import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import statistics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def convert_grade(grade):
    if grade == 'A':
        return 4.0
    elif grade == 'A-':
        return 3.67
    elif grade == 'B+':
        return 3.33
    elif grade == 'B':
        return 3.0
    elif grade == 'B-':
        return 2.67
    elif grade == 'C+':
        return 2.33
    elif grade == 'C':
        return 2.0
    elif grade == 'C-':
        return 1.67
    elif grade == 'D+':
        return 1.33
    elif grade == 'D':
        return 1.0
    elif grade == 'D-':
        return 0.67
    elif grade == 'F':
        return 0.0
    else:
        return 0.0





def num_grades(keys):
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
    avg = sum(grades) / len(grades)
    return avg
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



def getSections(keys):
    with open(keys, "r") as f:
        sections = f.readlines()
        sections.pop(0)
        for i in range(len(sections)):
            sections[i] = sections[i].strip()
    return sections

def getGRPHist(keys):
    gpa_list = []
    linesf = []
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
        linesf.extend(lines)
    df = pd.DataFrame(linesf, columns=['Data'])
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df[~df["Grade"].str.contains("I|W|P|NP")]
    df['Numerical Grade'] = df['Grade'].apply(convert_grade)
    data = df['Grade'].tolist()
    grades = ['F', 'D-', 'D', 'D+', 'C-', 'C', 'C+',
              'B-', 'B', 'B+', 'A-', 'A']
    grade_dict = {grade: 0 for grade in grades}


    # Count the frequency of each grade

    for grade in data:
        if grade in grade_dict:
            grade_dict[grade] += 1

    plt.bar(grade_dict.keys(), grade_dict.values())

    # Add labels and title
    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Group')

    # Display the plot
    return grade_dict

def getSECHIST(keys):
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

    df = pd.DataFrame(lines, columns=['Data'])
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df[~df["Grade"].str.contains("I|W|P|NP")]
    df['Numerical Grade'] = df['Grade'].apply(convert_grade)
    data = df['Grade'].tolist()
    grades = ['F', 'D-', 'D', 'D+', 'C-', 'C', 'C+',
              'B-', 'B', 'B+', 'A-', 'A']
    grade_dict = {grade: 0 for grade in grades}


        # Count the frequency of each grade

    for grade in data:
        if grade in grade_dict:
            grade_dict[grade] += 1

    plt.bar(grade_dict.keys(), grade_dict.values())

        # Add labels and title
    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Section')
    return grade_dict
def getSecData(keys):
    gpa_list = []
    linesf = []
    with open(keys, "r") as f:
        sections = f.readlines()
    sections.pop(0)
    value = app.get_selection2()

    for y in range(len(sections)):
        sections[y] = sections[y].strip()
    with open(sections[value], "r") as f:
        lines = f.readlines()
    lines.pop(0)
    for j in range(len(lines)):
        lines[j] = lines[j].strip()
    df = pd.DataFrame(lines, columns=['Data'])
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    return df

class root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("GPA Calculator")
        self.geometry("1200x1200")

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

        self.button4 = Button(self, text="Show", command=self.showData)
        self.button4.place(x=375, y=180, width=75, height=50)

        #Create textbox that holds the file path
        self.textbox = Text(self, height=5, width=30)
        self.textbox.place(x=10, y=20, width=250, height=50)

        # Create textbox2 for teh Z-score result
        self.textbox2 = Text(self, height=5, width=30)
        self.textbox2.place(x=500, y=180, width=250, height=50)

        #Create textbox for output of GRP Results
        self.textbox3 = Text(self, height=40, width=40)
        self.textbox3.place(x=500, y=20, width=250, height=150)
        self.grp = tk.StringVar()
        #Create List Box that stores the GRP files
        self.list = Listbox(self,exportselection=False)
        self.list.place(x=10, y=100, width=250, height=50)

        # Create List Box that stores the SEC files
        self.list2 = Listbox(self,exportselection=False)
        self.list2.place(x=10, y=180, width=250, height=50)
       #Create a button to Output the Histogram
        self.button4 = Button(self, text="Histogram",command = self.displayhist)
        self.button4.place(x=300, y=240, width=75, height=30)

       #Create a canvas to hold Group Histogram
        self.canvas1 = self.create_canvas("Group")
        self.canvas1.get_tk_widget().place(x=300, y=280, width=450, height=200)
        #Create a cavas to hold a section histogram
        self.canvas2 = self.create_canvas("Section")
        self.canvas2.get_tk_widget().place(x=300, y=500, width=450, height=200)

        #Create  table to hold section data
        self.treeview = Treeview(self, show='headings')
        self.treeview.place(x=10, y=250, width=280, height=400)
        self.scrollbar = Scrollbar(self, orient='vertical', command=self.treeview.yview)
        self.scrollbar.place(x=10, y=250, height=200)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_canvas(self,title):
        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title(title)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        return canvas
    def displayhist(self):


        self.canvas1 = self.create_canvas("Group")
        self.canvas1.get_tk_widget().place(x=300, y=280, width=450, height=200)

        self.canvas2 = self.create_canvas("Section")
        self.canvas2.get_tk_widget().place(x=300, y=500, width=450, height=200)
        self.group_files = create_dict(self.getFilePath())


        keys = list(self.group_files.keys())
        selc = self.get_selection()
        grade_dict = getGRPHist(keys[selc])

        fig1 = self.canvas1.figure

        ax1 = fig1.gca()
        ax1.set_title(keys[selc])

        ax1.bar(grade_dict.keys(), grade_dict.values())
        self.canvas1.draw()

        selc1 = self.get_selection2()
        keys2 = getSections(keys[selc])
        grade_dict2 = getSECHIST(keys[selc])
        fig2 = self.canvas2.figure

        ax2 = fig2.gca()
        ax2.set_title(keys2[selc1])

        ax2.bar(grade_dict2.keys(), grade_dict2.values())
        self.canvas2.draw()



    def close_window(self):
        self.quit()
        self.destroy()
    def showData(self):
        keys = self.getKeys()
        selc = self.get_selection()
        self.dataframe = getSecData(keys[selc])

        self.treeview.delete(*self.treeview.get_children())

        columns = list(self.dataframe.columns)
        self.treeview["columns"] = columns
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor="center")

        # Add data rows to Treeview
        for row in self.dataframe.itertuples(index=False):
            self.treeview.insert("", "end", values=row)


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
