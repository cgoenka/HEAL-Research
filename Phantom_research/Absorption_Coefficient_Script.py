# Import toolboxes
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plecs_helper as helper
import math

#Set names for every concentration tested
samples = ["Nothing", "Empty Cuvette", "Conc. 1", "Conc. 2", "Conc.3", "Conc.4","Conc.5","Conc.6","Conc.7","Conc.8","Conc.9","Conc.10","Conc.11", "Conc.12", "Conc.13", "Conc.14","Conc.15","Conc.16","Conc.17","Conc.18","Conc.19","Conc.20","Conc.21", "Conc.22", "Conc.23", "Conc.24","Conc.25","Conc.26","Conc.27","Conc.28","Conc.29","Conc.30","Conc.31", "Conc.32", "Conc.33", "Conc.34","Conc.35","Conc.36","Conc.37","Conc.38","Conc.39","Conc.40","Conc.41", "Conc.42", "Conc.43", "Conc.44","Conc.45","Conc.46","Conc.47","Conc.48","Conc.49","Conc.50","Conc.51", "Conc.52", "Conc.53", "Conc.54","Conc.55","Conc.56","Conc.57","Conc.58","Conc.59","Conc.60","Conc.61", "Conc.62", "Conc.63", "Conc.64","Conc.65"]
#set number of wavelengths to test
wavelengths = ["630nm", "710nm", "800nm", "905nm", "940nm","1000nm"]
#set sample length (distance light has to pass)
sample_length=1 # cm

#make data structure to store imported data setting wavelengths as x axis and concentrations as the y axis
experimental_data = {}
for sample in samples:
    sample_values = {}
    for wavelength in wavelengths:
        sample_values[wavelength] = []
    experimental_data[sample] = sample_values

#from imported data, get the test number and rename it into its actual concentration label
def get_sample_name_from_file_name(file_name):
    file_number = int(file_name[-9:-4], base = 10)
    # change the number after // for how many tests per concentration
    this_concentration = samples[file_number // 3]
    return this_concentration
    
#main for loop to import data into the data structure
for filename in os.listdir("Intensities of Only Milk and Only Ink"):
    #open the data from the folder "V1 values" AS variable filename but save as f
    with open(os.path.join("Intensities of Only Milk and Only Ink", filename), 'r') as f: # open in readonly mode
        for i, line in enumerate(f):
            # change i > # of lines before data you need. gets rid of random text
            if i > 14:
                #splits the data that comes in as a string into seperate strings by line (one line is a wavelength and its intensity)
                splitline = line.split()
                #pull wave lengths needed but the exact values that oceanview gives you
                if float(splitline[0]) in [630.188,710.104,800.131,905.029,940.061,1000.111]:
                    #call function to set sample name to which concentration it is
                    sample_name=get_sample_name_from_file_name(filename)
                    # rename the wavelengths from data into readable terms
                    wavelength=(splitline[0][:-4]) + "nm"
                    #set values for the intensities at each wavelength
                    intensity=splitline[1]
                    #put data into data structure
                    experimental_data[sample_name][wavelength].append(float(intensity))
  
#Math for average data from the 3 tests for each sample
averaged_data = {}
for sample in samples:
    sample_values = {}
    for wavelength in wavelengths:
        values_to_average=experimental_data[sample][wavelength]
        sample_values[wavelength] = round(sum(values_to_average)/3, 3)
    averaged_data[sample] = sample_values  

#take average data frame and make it into a matrix with Nothing and Empty Cuvette Values
avg_data_with_Not_and_Emp = pd.DataFrame.from_dict(averaged_data).transpose()
#print(avg_data_with_Not_and_Emp)     

#Seperate the first two rows of data for the zeroing intensities (Input Intensities)(one with nothing, one with an empty cuvette)
nothing_row = avg_data_with_Not_and_Emp.loc["Nothing"]
empty_c_row = avg_data_with_Not_and_Emp.loc["Empty Cuvette"]
#print(nothing_row)
#print(empty_c_row)

#take averaged data and remove the two rows for the nothing and empty cuvette values
avg_data_without_Not_and_Emp = avg_data_with_Not_and_Emp.copy()
avg_data_without_Not_and_Emp.drop(labels = ["Nothing", "Empty Cuvette"], axis = "rows", inplace = True)
#print(avg_data_without_Not_and_Emp)

# Nothing test as the zeroing intensities (Input Intensities)
for index, this_row in avg_data_with_Not_and_Emp.iterrows():
    if index == "Nothing" or index == "Empty Cuvette":
        continue
    #print(index)
    #math that solves for absorption coeffiction
    new_row = np.log(nothing_row / this_row) / sample_length
    #print(this_row)
    #print(new_row)
    avg_data_without_Not_and_Emp.loc[index] = new_row

#final data frame with Absorption coeffiction for nothing zeroing
avg_data_without_Not_and_Emp_transpose = avg_data_without_Not_and_Emp.transpose()
#print(avg_data_without_Not_and_Emp_transpose)


#############################################
# Empty Cuvette
avg_data_without_Not_and_Emp_empty_cuvette = avg_data_without_Not_and_Emp.copy()

# Empty Cuvette test as the zeroing intensities (Input Intensities)
for index, this_row in avg_data_with_Not_and_Emp.iterrows():
    if index == "Nothing" or index == "Empty Cuvette":
        continue
    #print(index)
    #math that solves for absorption coeffiction
    new_row = np.log(empty_c_row / this_row) / sample_length
    #print(this_row)
    #print(new_row)
    avg_data_without_Not_and_Emp_empty_cuvette.loc[index] = new_row

#final data frame with Absorption coeffiction for nothing zeroing
avg_data_without_Not_and_Emp_empty_cuvette_transpose = avg_data_without_Not_and_Emp_empty_cuvette.transpose()

mixture_label=np.arange(0,0.0065,0.0001)*1e-3
mixture_label_ink=np.arange(0,0.0023,0.0001)*1e-3
mixture_label_milk=np.arange(0.0001,0.0043,0.0001)*1e-3
############################################################
#ERROR CALCULATIONS
#Do math origionally done above with no averging
all_experimental_data=pd.DataFrame.from_dict(experimental_data).transpose()
#exp_nothing_row = all_experimental_data.loc["Nothing"]
#exp_empty_row= all_experimental_data.loc["Empty Cuvette"]
all_experimental_data_nothing_zero=all_experimental_data.copy()
all_experimental_data_nothing_zero.drop(labels=["Nothing", "Empty Cuvette"], axis = "rows", inplace= True)
print(all_experimental_data)

#using nothing as zeroing
for index, this_row in all_experimental_data.iterrows():
    if index == "Nothing" or index == "Empty Cuvette":
        continue
    #print(this_row)
    #print(type(nothing_row))
    Data_type = str
    for i in [0,1,2,3,4,5]:
        row=[]
        for f in [0,1,2]:
            row.append(np.log(nothing_row.iloc[i]/this_row.iloc[i][f])/sample_length)        
        new_row[i]=np.array(row, dtype=Data_type)
    all_experimental_data_nothing_zero.loc[index] = new_row

#find greatest error with nothing code
error_nothing=all_experimental_data_nothing_zero.copy()
for index, this_row in all_experimental_data_nothing_zero.iterrows():
    error=[]
    for i in [0,1,2,3,4,5]:
        error_1 = abs(float(this_row.iloc[i][0])-avg_data_without_Not_and_Emp.loc[index][i])
        #print(error_1)
        error_2 = abs(float(this_row.iloc[i][1])-avg_data_without_Not_and_Emp.loc[index][i])
        #print(error_2)
        error_3 = abs(float(this_row.iloc[i][2])-avg_data_without_Not_and_Emp.loc[index][i])
        #print(error_3)
        if math.isnan(error_1):
            error_1 = float(0)
        if math.isnan(error_2):
            error_2 = float(0)
        if math.isnan(error_3):
            error_3 = float(0)
        if error_1 >= error_2 and error_1 >= error_3:
            error.append(error_1)
        elif error_2 >= error_1 and error_2 >= error_3:
            error.append(error_2)
        elif error_3 >= error_1 and error_3 >= error_2:
            error.append(error_3) 
        #print(error) 
    #error_act=np.array(error,dtype=str)    
    error_nothing.loc[index] = error
    
#Error with empty cuvette
all_experimental_data_empty_zero=all_experimental_data.copy()
all_experimental_data_empty_zero.drop(labels=["Nothing", "Empty Cuvette"], axis = "rows", inplace= True)

#find all absorption coeffictions for error
for index, this_row in all_experimental_data.iterrows():
    if index == "Nothing" or index == "Empty Cuvette":
        continue
    #print(this_row)
    #print(type(nothing_row))
    Data_type = str
    for i in [0,1,2,3,4,5]:
        row=[]
        for f in [0,1,2]:
            row.append(np.log(empty_c_row.iloc[i]/this_row.iloc[i][f])/sample_length)        
        new_row[i]=np.array(row, dtype=Data_type)
    all_experimental_data_empty_zero.loc[index] = new_row

#find greatest error
error_empty=all_experimental_data_empty_zero.copy()
for index, this_row in all_experimental_data_empty_zero.iterrows():
    error=[]
    for i in [0,1,2,3,4,5]:
        error_1 = abs(float(this_row.iloc[i][0])-avg_data_without_Not_and_Emp.loc[index][i])
        #print(error_1)
        error_2 = abs(float(this_row.iloc[i][1])-avg_data_without_Not_and_Emp.loc[index][i])
        #print(error_2)
        error_3 = abs(float(this_row.iloc[i][2])-avg_data_without_Not_and_Emp.loc[index][i])
        #print(error_3)
        if math.isnan(error_1):
            error_1 = float(0)
        if math.isnan(error_2):
            error_2 = float(0)
        if math.isnan(error_3):
            error_3 = float(0)
        if error_1 >= error_2 and error_1 >= error_3:
            error.append(error_1)
        elif error_2 >= error_1 and error_2 >= error_3:
            error.append(error_2)
        elif error_3 >= error_1 and error_3 >= error_2:
            error.append(error_3) 
        #print(error) 
    #error_act=np.array(error,dtype=str)    
    error_empty.loc[index] = error

############################################################
#2 GRAPHS just zerod on empty and no cuvette 

fig, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1, sharex = False, sharey = False, figsize = (8, 8))
helper.axes_labels("", "L", "Absorption Coefficent", "mm^-1", title = "Absorption Coefficent for varying concentration of liquid phantoms zeroed with no cuvette", ax = ax1)
fig.autofmt_xdate()
for index, this_row in avg_data_without_Not_and_Emp_transpose.iterrows():
    #print(this_row)
    #ax1.plot(mixture_label,avg_data_without_Not_and_Emp[index],  label = f"Wavelength = {index}")
    ax1.errorbar(mixture_label,avg_data_without_Not_and_Emp[index], yerr = error_nothing[index] , label = f"Wavelength = {index}")
ax1.legend()
helper.axes_labels("Concentration Number", "L", "Absorption Coefficent", "mm^-1", title = "Absorption Coefficent for varying concentration of liquid phantoms zeroed with an empty cuvette", ax = ax2)
for index, this_row in avg_data_without_Not_and_Emp_empty_cuvette_transpose.iterrows():  
    #print(this_row)
    ax2.errorbar(mixture_label,avg_data_without_Not_and_Emp_empty_cuvette[index], yerr = error_empty[index] ,label = f"Wavelength = {index}")
ax2.legend()
plt.show()

######################################
#Split data for ink vs. milk
avg_data_nothing_ink_trans = avg_data_without_Not_and_Emp_transpose.iloc[:,:23]
avg_data_nothing_milk_trans= avg_data_without_Not_and_Emp_transpose.iloc[:,23:]
avg_data_empty_ink_trans= avg_data_without_Not_and_Emp_empty_cuvette_transpose.iloc[:,:23]
avg_data_empty_milk_trans= avg_data_without_Not_and_Emp_empty_cuvette_transpose.iloc[:,23:]
avg_data_nothing_ink = avg_data_without_Not_and_Emp.iloc[:23,:]
avg_data_nothing_milk= avg_data_without_Not_and_Emp.iloc[23:,:]
avg_data_empty_ink= avg_data_without_Not_and_Emp_empty_cuvette.iloc[:23,:]
avg_data_empty_milk= avg_data_without_Not_and_Emp_empty_cuvette.iloc[23:,:]
error_nothing_ink = error_nothing.iloc[:23,:]
error_nothing_milk= error_nothing.iloc[23:,:]
error_empty_ink= error_empty.iloc[:23,:]
error_empty_milk= error_empty.iloc[23:,:]

#milk vs ink and empty vs nothing

fig, (ax) = plt.subplots(nrows = 2, ncols = 2, sharex = False, sharey = False, figsize = (8, 8))
helper.axes_labels("", "L", "Absorption Coefficient", "mm^-1", title = "Concentrations of Ink Zeroed With No Cuvette", ax = ax[0,0])
fig.autofmt_xdate()
for index, this_row in avg_data_nothing_ink_trans.iterrows():
    #print(this_row)
    ax[0,0].errorbar(mixture_label_ink,avg_data_nothing_ink[index], yerr = error_nothing_ink[index],  label = f"Wavelength = {index}")
ax[0,0].legend(fontsize = "5",loc="upper left")
helper.axes_labels("", "L", "", "mm^-1", title = "Concentrations of Milk Zeroed With No Cuvette", ax = ax[0,1])
for index, this_row in avg_data_nothing_milk_trans.iterrows():  
    #print(this_row)
    ax[0,1].errorbar(mixture_label_milk,avg_data_nothing_milk[index], yerr = error_nothing_milk[index] , label = f"Wavelength = {index}")
ax[0,1].legend(fontsize = "5",loc="upper left")
helper.axes_labels("Amount of Ink", "L", "Absorption Coefficient", "mm^-1", title = "Concentrations of Ink Zeroed With an Empty Cuvette", ax = ax[1,0])
for index, this_row in avg_data_empty_ink_trans.iterrows():  
    #print(this_row)
    ax[1,0].errorbar(mixture_label_ink,avg_data_empty_ink[index], yerr = error_empty_ink[index] , label = f"Wavelength = {index}")
ax[1,0].legend(fontsize = "5",loc="upper left")
helper.axes_labels("Amount of Milk", "L", "", "mm^-1", title = "Concentrations of Milk Zeroed With an Empty Cuvette", ax = ax[1,1])
for index, this_row in avg_data_empty_milk_trans.iterrows():  
    #print(this_row)
    ax[1,1].errorbar(mixture_label_milk,avg_data_empty_milk[index], yerr = error_empty_milk[index]  ,label = f"Wavelength = {index}")
ax[1,1].legend(fontsize = "5",loc="upper left")
fig.suptitle('Absorption Coefficient of Aqueous Phantoms In Varying Concentrations')
plt.show()
plt.savefig("Ink_and_Absorption_Test_1.jpg")