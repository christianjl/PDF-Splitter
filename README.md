# PDF-Splitter

GUI tool to split an existing PDF file into separate pages or create a new PDF from selected pages.
Written for Python 3.5.1
* Completely functioning code, but still some refinement required.


**Installation:**

 Required module: PyPDF2
 Run the pdf_splitter.py file.
 
 
 **Usage:**
 
 ![GUI](http://i.imgur.com/3hbHgWC.png)
 
 `Split Into Individual Files` - Creates a new folder in the same location as the `File Location`. The folder name is the same as the specified PDF file with 'Split Files' appended. If the folder already exists, an unique number will be appended to prevent overwriting.
 
 `New File From Pages` - A new PDF file is created from the entered page ranges in the same location as the `File Location`. The file name is the same as the specified PDF file with '(Edited)' appended. If the file already exists, an unique number will be appended to prevent overwriting. 
 
 If `New File Name` is specified, the new PDF will be created with the entered name.
 
