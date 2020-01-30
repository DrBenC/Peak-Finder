"""
This script will look through a csv file, plot a graph and help locate peaks
"""

import pandas as pd
import glob
import os
from matplotlib import pyplot as plt
import numpy as np
from tkinter import *
from tkinter.ttk import Combobox
import time

#This retrieves the path of the script and searches for all .par files

#simple function to produce a mean of a list
def mean(list):
    total = sum(list)
    return total/(len(list))

#complex function - will go through a .txt file and give the locations (first column) of peaks in the second column
def peak_find(file):
    #turns out plt.close causes this entire program to crash lol
    #plt.close()
    plt.cla()
    data_frame = pd.read_csv(file+".txt", delim_whitespace = True, names = ["Energy", "Counts"])
    counts_list = list(data_frame["Counts"])
    
    energy_list = list(data_frame["Energy"])
    energy_reverse = list(reversed(energy_list))

    energy_list_peaks = []
    counts_peaks = []
        
    data_number = len(counts_list)

    threshold = int(threshold_var.get())
    space = int(space_var.get())
    
    for n, value in enumerate(counts_list):
           
        if n < space:           
            if value > (mean(counts_list[(n):(n+space)])+threshold):
                
                energy_list_peaks.append(energy_list[n])
                counts_peaks.append(counts_list[n])
        elif n > data_number-space:
            if value > (mean(counts_list[(n-space):(n)]))+threshold:
                
                energy_list_peaks.append(energy_list[n])
                counts_peaks.append(counts_list[n])
        else:
            
            if value > ((mean(counts_list[(n-space):(n+space)]))+threshold):
                
                energy_list_peaks.append(energy_list[n])
                counts_peaks.append(counts_list[n])

    #we get multiple values per actual peak by this method - so we need to average out the close values      

    to_mean = []
    reduced_e_peaks = [[energy_list_peaks[0]]]

    for x in energy_list_peaks[1:]:
        if x - reduced_e_peaks[-1][0] > -5: #can change this value
            reduced_e_peaks[-1].append(x)
            
        else:
            reduced_e_peaks.append([x])

    global final_peaks
    final_peaks = []
    
    for n in reduced_e_peaks:
        mean_peak = mean(n)
        final_peaks.append(round(mean_peak, 1))

    global peaks
    peaks = []
        
    for peak in final_peaks:
        peaks.append("Peak at "+str(peak)+" eV")
    #now we plot the data so we can show the user their data to compare with the peak readout
    plt.figsize = ("1x1")
    ax1 = plt.subplot()
    ax1.plot(energy_list, counts_list)
    ax1.set_xlim(energy_list[0], energy_reverse[0])
    
    plt.savefig(file+".png")
    
    

#this oversees the writing of the found peaks to a .txt file
    
def write_file():
    core_file_s = combo_txt.get()
    print (core_file_s)
    with open("Peak Output for "+core_file_s+".txt", "w") as output:
        for peak_2 in final_peaks:
            
            output.write(str(peak_2))
            output.write("\n")

#this is what happens when the button 'analyse' is pressed

def clicked_find():
    
    core_file_s = combo_txt.get()
    peak_find(core_file_s)           
                    
    lbl_peaks.configure(text = "Peaks found at: "+str(final_peaks))
  
    global photo
    photo = PhotoImage(file = core_file_s+".png")
    lbl_graph.create_image(300, 0, anchor="n", image=photo)
    
 
               
window = Tk()

window.title("DrBenC's Peak Finder")
window.geometry("650x600")

#the top label shows the files in the same directory, ready to put them in a combobox
abspath = os.path.abspath("PeakSearch.pyw")
path = os.path.dirname(abspath)

filenames1 = glob.glob(path + "/*.txt")
filenames2 = [os.path.split(y)[1] for y in filenames1]
filenames = [os.path.splitext(os.path.basename(z))[0] for z in filenames2]

txt_text = ("Detected the following files: "+str(filenames))

lbl_files = Label(window, text=txt_text)
lbl_files.grid(row = 1, column = 1, columnspan = 100, sticky = "w")

lbl_filename = Label(window, text = "File to process: ")
lbl_filename.grid(row = 2, column = 1, sticky = "w")

combo_txt = Combobox(window)
combo_txt["values"] = filenames
combo_txt.grid(row = 2, column = 2, padx = 1, sticky = "w")

#this is the section of the gui for changing 'threshold' and 'space'

lbl_threshold = Label(window, text = "Threshold Intensity: ")
lbl_threshold.grid(row = 3, column = 1, sticky = "w")

threshold_var = StringVar()
threshold_number = Entry(window, textvariable=threshold_var)
threshold_var.set(50)
threshold_number.grid(row = 3, column = 2, sticky="w")

lbl_window = Label(window, text = "Local Points: ")
lbl_window.grid(row = 3, column = 3, sticky = "w")

space_var = StringVar()
space_number = Entry(window, textvariable=space_var)
space_var.set(50)
space_number.grid(row = 3, column = 4, sticky="w")

threshold = int(threshold_var.get())
space = int(space_var.get())

#this presents the graph we plotted early by importing the .png we made

lbl_graph = Canvas(window, width=700, height=500)
lbl_graph.grid(row = 4, column = 1, columnspan = 5, sticky="n")

lbl_peaks = Label(window)
lbl_peaks.grid(row = 5, column=1, sticky = "w", columnspan = 50)

#these are the command buttons

button_analyse = Button(window, text = "Search for Peaks", command = clicked_find)
button_analyse.grid(row = 2, column = 3, sticky = "w")

button_print = Button(window, text = "Print Peaks to .txt", command = write_file)
button_print.grid(row = 2, column = 4, sticky = "w")

window.mainloop()    
