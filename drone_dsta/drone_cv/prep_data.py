import csv

file_name = "archive/ntut_drone_test/ntut_drone_test/Drone_004/vott-csv-export/Drone_004-export.csv"
output_path = ""
with open(file_name, 'r') as csvfile:
    # create the reader object
    csvreader = csv.reader(csvfile)
    
    # check if the output file is present
    os.makedirs(folder_path, exist_ok=True)
    # iterate through each row in the csv file
    for row in csvreader:
        # read each line of the csv
        label = row[0]
        x_min = row[1]
        y_min = row[2]
        x_max = row[3]
        y_max = row[4]
        
        # prepping the data
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        width = x_max - x_min
        length = y_max - y_min
        
        # create a new file and append it to the folder\
        filename = os.path.splitext(label)[0] + '.txt'
        filepath = os.path.join(output_path, file_name)
        
        # check if the file exists
        if os.path.exists(filepath):
            # it exists
        else:
            # it doesnt exist
            with open(file_path, 'w') as file:
                file.write()