#!/usr/bin/env python
# coding: utf-8

# # FilesAndFoldersInDirectory

# In[1]:


from datetime import datetime
import os
import re
import random
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class FilesAndFoldersInDirectory:
    def __init__(self, directory_path, folder_name, folder_pattern, file_name, pattern, limit):
        """
        Initializes evaluator with directory from which to traverse, requires a folder name and regex pattern, 
        a file name and regex pattern, and a limit to stop the search.
        """
        self.directory_path = directory_path 
        self.folder_name = folder_name               
        self.folder_pattern = re.compile(folder_pattern) 
        self.file_name = file_name                       
        self.pattern = re.compile(pattern)               
        self.limit = limit                            
        self.today = datetime.now().strftime("%Y-%m-%d") 
        self.grouped_folders = defaultdict(list) 
        
    
    def retrieve_pattern_matched_files(self):
        pdf_files = []
        count = 0
        for root, dirs, files in os.walk(self.directory_path):
            if self.folder_pattern.search(root):                    
                for file in files:                               
                    if self.pattern.match(file):                      
                        pdf_files.append(os.path.join(file))        
                        count += 1                                   
                        if count == self.limit:                  
                            break
            if count == self.limit:
                break
        
        print(f"A total of {len(pdf_files)} retrieved {self.file_name} files from {self.folder_name} on {self.today}")
        
        random_sample_size = min(10, len(pdf_files))
        random_pdfs = random.sample(pdf_files, random_sample_size)
        
        print("\nRandomly selected samples:")
        for pdf in random_pdfs:
            print(pdf)

   
    def distribution_of_files_in_folders(self):
        pdf_files = []
        folder_pdf_count = {}
        total_count = 0
        total_submissions_folders = 0       
        
        for root, dirs, files in os.walk(self.directory_path):  
            if self.folder_pattern.search(root):                    
                total_submissions_folders += 1                     
                matched_count = 0                               
                for file in files:                                 
                    if self.pattern.match(file):                        
                        pdf_files.append(os.path.join(root, file))    
                        matched_count += 1                            
                        total_count += 1                           
                        if total_count == self.limit:                 
                            break
                folder_pdf_count[root] = matched_count              
            if total_count == self.limit:
                break
        
        self.grouped_folders = defaultdict(list) 
        
        for folder, count in folder_pdf_count.items():
            self.grouped_folders[count].append(folder)
        
        df = pd.DataFrame(list(folder_pdf_count.items()), columns=['Folder', 'PDF_Count'])
        
        counts, bins = np.histogram(df['PDF_Count'], bins=range(df['PDF_Count'].max() + 2)) 
        
        palette = sns.color_palette('colorblind', len(counts))
        
        plt.figure(figsize=(10, 6)) 
        plt.bar(bins[:-1], counts, width=1, edgecolor='black', color=palette, align='edge')
        plt.xticks(ticks=bins[:-1] + 0.5, labels=range(df['PDF_Count'].max() + 1)) 
        plt.title(f"Distribution of '{self.file_name}' in '{self.folder_name}' folders", fontsize=16)
        plt.xlabel("Number of files")
        plt.ylabel("Number of folders")
        plt.grid(False)
        plt.show()
        
        print(f"A total of {total_submissions_folders} {self.folder_name} folders within the directory on {self.today}\n")
        
        print(f"The distribution of files in those folders:")
        
        for count, folders in sorted(self.grouped_folders.items()):
            print(f"{len(folders)} folders with {count} {self.file_name}") 


    def show_files_in_random_folder(self, frequency):
        if frequency in self.grouped_folders:
            random_folder = random.choice(self.grouped_folders[frequency])  
            
            print(f"Randomly selected folder with {frequency} {self.file_name}: \n\n{random_folder}\n")
            
            for file in os.listdir(random_folder): 
                if self.pattern.match(file): 
                    print(file) 
        
        else:
            print(f"No folder with exactly {frequency} {self.file_name} found.") 

