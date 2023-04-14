function data = json2matrix(path)
    fid = fopen(path); % Opening the file
    raw = fread(fid,inf); % Reading the contents
    str = char(raw'); % Transformation
    fclose(fid); % Closing the file
    
    data = jsondecode(str); 

