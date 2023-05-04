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
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys
    with open(path, "r") as f:
        sections = f.readlines()
        sections.pop(0)

    for x in range(len(sections)):
        sections[x] = sections[x].strip()
        path2 = filepath.rpartition('/')[0] + '/' + sections[x]
        with open(path2, "r") as f:
            lines = f.readlines()
            lines.pop(0)
            linef.extend(lines)
    for x in range(len(linef)):
        linef[x] = linef[x].strip()

    df = pd.DataFrame(linef)
    df.columns = ['Data']
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df.drop('Data', axis=1)
    df['GPA'] = df['Grade'].apply(convert_grade)
    df = df[~df["Grade"].str.contains("I|W|P|NP")]
    grades = df['Grade'].tolist()
    grade_counts = {}
    for grade in grades:
        if grade in grade_counts:
            grade_counts[grade] += 1
        else:
            grade_counts[grade] = 1
    grade_order = ['A', 'A-', 'B+', 'B', 'C', 'D', 'F']
    grade_strings = []
    for grade in grade_order:
        if grade in grade_counts:
            grade_string = grade + ': ' + str(grade_counts[grade])
            grade_strings.append(grade_string)
    result = ', '.join(grade_strings)
    return result


def getSTDEV(keys):
    linef = []
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys
    with open(path, "r") as f:
        sections = f.readlines()
        sections.pop(0)

    for x in range(len(sections)):
        sections[x] = sections[x].strip()
        path2 = filepath.rpartition('/')[0] + '/' + sections[x]
        with open(path2, "r") as f:
            lines = f.readlines()
            lines.pop(0)
            linef.extend(lines)
    for x in range(len(linef)):
        linef[x] = linef[x].strip()

    df = pd.DataFrame(linef)
    df.columns = ['Data']
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
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys
    with open(path, "r") as f:
        sections = f.readlines()
        sections.pop(0)

    for x in range(len(sections)):
        sections[x] = sections[x].strip()
        path2 = filepath.rpartition('/')[0] + '/' + sections[x]
        with open(path2, "r") as f:
            lines = f.readlines()
            lines.pop(0)
            linef.extend(lines)
    for x in range(len(linef)):
        linef[x] = linef[x].strip()

    df = pd.DataFrame(linef)
    df.columns = ['Data']
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df = df.drop('Data', axis=1)
    df['GPA'] = df['Grade'].apply(convert_grade)
    df = df[~df["Grade"].str.contains("I|W|P|NP")]

    grades = df['GPA'].tolist()
    avg = sum(grades) / len(grades)
    avg = round(avg, 2)
    return avg


def get_sec_gpa(keys):
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys
    with open(path, "r") as f:
        sections = f.readlines()
        sections.pop(0)
    for x in range(len(sections)):
        sections[x] = sections[x].strip()
    value = app.get_selection2()
    path2 = filepath.rpartition('/')[0] + '/' + sections[value]
    with open(path2, "r") as f:
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
    result = (sec_gpa - grp_gpa) / stdev
    result = round(result, 3)
    return result


def create_dict(path):
    group_files = {}
    with open(path, "r") as f:
        groups = f.readlines()
    groups.pop(0)

    # Add the GRP files from RUN file
    for i in range(len(groups)):
        groups[i] = groups[i].strip()
        group_files[groups[i]] = {}
    keys = list(group_files.keys())
    for x in range(len(keys)):
        group_files[keys[x]]["Number of Courses"] = (num_courses(keys[x]))
        group_files[keys[x]]["Number of Students"] = (num_students(keys[x]))
        group_files[keys[x]]["Average GPA"] = (get_GRP_GPA(keys[x]))
        group_files[keys[x]]["Number of Grades"] = (num_grades(keys[x]))

    return group_files


def num_courses(keys):
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys
    with open(path, "r") as f:
        sections = f.readlines()
    sections.pop(0)
    for y in range(len(sections)):
        sections[y] = sections[y].strip()
        sections[y] = sections[y][:-7]

    count = len(set(sections))
    return count


def num_students(keys):
    count = 0
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys

    with open(path, "r") as f:
        sections = f.readlines()
    sections.pop(0)
    for i in range(len(sections)):
        sections[i] = sections[i].strip()
    for x in range(len(sections)):
        path2 = filepath.rpartition('/')[0] + '/' + sections[x]
        with open(path2, "r") as f:
            lines = f.readlines()
        df = pd.DataFrame(lines)
        df.columns = ['Data']
        df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
        df["Student Id"] = df["Student Id"].str.strip('"')
        stid = df["Student Id"].tolist()
        length = len(set(stid))
        count = length + count
    return count


def getSections(keys):
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys

    with open(path, "r") as f:
        sections = f.readlines()
        sections.pop(0)
        for i in range(len(sections)):
            sections[i] = sections[i].strip()
    return sections


def getGRPHist(keys):
    linesf = []
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys

    with open(path, "r") as f:
        sections = f.readlines()
    sections.pop(0)

    for y in range(len(sections)):
        sections[y] = sections[y].strip()
        path2 = filepath.rpartition('/')[0] + '/' + sections[y]
        with open(path2, "r") as f:
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

    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Group')

    return grade_dict


def getSECHIST(keys):
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys

    with open(path, "r") as f:
        sections = f.readlines()
        sections.pop(0)
    for x in range(len(sections)):
        sections[x] = sections[x].strip()
    value = app.get_selection2()

    path2 = filepath.rpartition('/')[0] + '/' + sections[value]
    with open(path2, "r") as f:
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

    for grade in data:
        if grade in grade_dict:
            grade_dict[grade] += 1

    plt.bar(grade_dict.keys(), grade_dict.values())

    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Section')
    return grade_dict


def getSecData(keys):
    filepath = app.getFilePath()
    path = filepath.rpartition('/')[0] + '/' + keys
    with open(path, "r") as f:
        sections = f.readlines()
    sections.pop(0)
    value = app.get_selection2()

    for y in range(len(sections)):
        sections[y] = sections[y].strip()

    path2 = filepath.rpartition('/')[0] + '/' + sections[value]
    with open(path2, "r") as f:
        lines = f.readlines()
    lines.pop(0)
    for j in range(len(lines)):
        lines[j] = lines[j].strip()
    df = pd.DataFrame(lines, columns=['Data'])
    df[['Last Name', 'First Name', 'Student Id', 'Grade']] = df['Data'].str.split(',', expand=True)
    df['Grade'] = df['Grade'].str.strip('"')
    df['Last Name'] = df['Last Name'].str.strip('"')
    df['First Name'] = df['First Name'].str.strip('"')
    df['Student Id'] = df['Student Id'].str.strip('"')

    df = df.drop('Data', axis=1)

    return df


class root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("GPA Calculator")
        self.geometry("920x800")

        # Create search button
        self.button = Button(self, text="Open RUN", command=self.openFile)
        self.button.place(x=590, y=30, width=75, height=40)

        # Create GRP Report button
        self.button = Button(self, text="GRP Report", command=self.calc)
        self.button.place(x=450, y=100, width=75, height=50)

        # Create textbox for output of GRP Results
        self.textbox3 = Text(self)
        self.textbox3.place(x=530, y=100, width=250, height=100)

        # Create an open button to open the GRP
        self.button2 = Button(self, text="Open GRP", command=self.showSEC)
        self.button2.place(x=275, y=100, width=75, height=50)

        # Create an open button to calc the z_score
        self.button3 = Button(self, text="Z-Score", command=self.show_z_score)
        self.button3.place(x=450, y=210, width=75, height=30)

        # Create textbox2 for the Z-score result
        self.textbox2 = Text(self)
        self.textbox2.place(x=530, y=210, width=250, height=30)

        # Button to show the Selected Section Data
        self.button4 = Button(self, text="Open SEC", command=self.showData)
        self.button4.place(x=275, y=180, width=75, height=50)

        # Create textbox that holds the file path
        self.textbox = Text(self)
        self.textbox.place(x=10, y=30, width=575, height=40)

        # Label the FilePath Box
        self.label = Label(self, text="File Path")
        self.label.place(x=10, y=7)

        # Create List Box that stores the GRP files
        self.list = Listbox(self, exportselection=False)
        self.list.place(x=10, y=100, width=250, height=50)

        # Create List Box that stores the SEC files
        self.list2 = Listbox(self, exportselection=False)
        self.list2.place(x=10, y=180, width=250, height=50)

        # Create a button to Output the Histogram
        self.button4 = Button(self, text="Histogram", command=self.displayhist)
        self.button4.place(x=450, y=265, width=75, height=30)

        # Create a canvas to hold Group Histogram
        self.canvas1 = self.create_canvas("Group")
        self.canvas1.get_tk_widget().place(x=450, y=310, width=450, height=200)

        # Create a cavas to hold a section histogram
        self.canvas2 = self.create_canvas("Section")
        self.canvas2.get_tk_widget().place(x=450, y=530, width=450, height=200)

        # Create  table to hold section data
        self.treeview = Treeview(self, show='headings')
        self.treeview.place(x=10, y=250, width=340, height=480)
        self.scrollbar = Scrollbar(self, troughcolor='red', orient='vertical', command=self.treeview.yview)
        self.scrollbar.place(x=350, y=250, height=200)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_canvas(self, title):
        self.fig = Figure(figsize=(4, 3), dpi=100)
        ax = self.fig.add_subplot(111)
        ax.set_title(title)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        return canvas

    def displayhist(self):
        try:
            self.canvas1 = self.create_canvas("Group")
            self.canvas1.get_tk_widget().place(x=450, y=310, width=450, height=200)

            self.canvas2 = self.create_canvas("Section")
            self.canvas2.get_tk_widget().place(x=450, y=530, width=450, height=200)
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

        except TypeError:
            pass
        except FileNotFoundError:
            self.popup("Please open a RUN file")

    def close_window(self):
        self.quit()
        self.destroy()

    def showData(self):
        try:
            keys = self.getKeys()
            selc = self.get_selection()
            self.dataframe = getSecData(keys[selc])

            self.treeview.delete(*self.treeview.get_children())

            columns = list(self.dataframe.columns)
            self.treeview["columns"] = columns
            for col in columns:
                self.treeview.heading(col, text=col)
                self.treeview.column(col, width=100, anchor="center")

            for row in self.dataframe.itertuples(index=False):
                self.treeview.insert("", "end", values=row)
        except FileNotFoundError:
            self.popup("Please open a RUN file")
        except TypeError:
            self.popup("Please Select a SEC file")
    def clear(self):
        self.canvas1.get_tk_widget().destroy()
        self.canvas1 = self.create_canvas("Group")
        self.canvas1.get_tk_widget().place(x=450, y=310, width=450, height=200)

        self.canvas2.get_tk_widget().destroy()
        self.canvas2 = self.create_canvas("Section")
        self.canvas2.get_tk_widget().place(x=450, y=530, width=450, height=200)

        self.list.delete(0, END)
        self.list2.delete(0, END)
        self.textbox.delete(1.0, END)
        self.textbox2.delete(1.0, END)
        self.textbox3.delete(1.0, END)
        self.treeview.delete(*self.treeview.get_children())

    def openFile(self):
        try:
            self.clear()
            filepath = filedialog.askopenfilename()
            s1 = "\\"
            s2 = "/"
            filepath = filepath.replace(s1, s2)
            filetype = filepath[-3:]
            if filetype == "RUN":
                self.textbox.delete(1.0, END)
                self.textbox.insert(END, filepath)
                self.list.delete(0, END)

                group_files = {}

                with open(filepath, "r") as f:
                    groups = f.readlines()
                groups.pop(0)

                for i in range(len(groups)):
                    groups[i] = groups[i].strip()
                    group_files[groups[i]] = {}
                keys = list(group_files.keys())

                for group in keys:
                    self.list.insert(tk.END, group)
            else:
                self.popup("Please select a .RUN file type")
        except IndexError:
            self.popup("Please select a .RUN file type")

    def popup(self, text):
        popup = tk.Toplevel(self)
        popup.title("Popup")
        x = self.winfo_x() + self.winfo_width() // 2 - popup.winfo_width() // 2
        y = self.winfo_y() + self.winfo_height() // 2 - popup.winfo_height() // 2
        width = 300
        height = 25
        popup.geometry(f"{width}x{height}+{x}+{y}")
        label = tk.Label(popup, text=text)
        label.pack()

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
        value = self.textbox.get("1.0", "end-1c")
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
        try:
            self.group_files = create_dict(self.getFilePath())
            keys = list(self.group_files.keys())
            selc = self.get_selection()
            values = self.group_files[keys[selc]]
            self.textbox3.delete(1.0, END)
            for key, value in values.items():
                self.textbox3.insert(END, (key + ': ' + str(value) + '\n'))
        except FileNotFoundError:
            self.popup("Please Open a RUN file")
        except TypeError:
            self.popup("Please select a GRP file")

    def showSEC(self):
        try:
            keys = self.getKeys()
            selc = self.get_selection()
            sections = getSections(keys[selc])
            self.list2.delete(0, END)
            for section in sections:
                self.list2.insert(tk.END, section)
        except FileNotFoundError:
            self.popup("Please open a RUN file")
        except TypeError:
            self.popup("Please select a GRP file")

    def show_z_score(self):
        try:
            self.textbox2.delete(1.0, END)
            keys1 = self.getKeys()
            selc1 = self.get_selection()
            result = get_z_score(keys1[selc1])

            if(result > 2 or result < -2):
                result = str(result)
                result = result + ": Significant"
            else:
                result = str(result)
                result = result + ": Not Significant"
            self.textbox2.insert(tk.END, result)
        except TypeError:
            self.popup("Please select both a GRP and SEC file")
        except FileNotFoundError:
            self.popup("Please open a RUN file")


if __name__ == "__main__":
    app = root()
    app.mainloop()
