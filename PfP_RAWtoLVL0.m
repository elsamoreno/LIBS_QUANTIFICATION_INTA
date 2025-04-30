% Batch BB1 spectra processing for calibrated X axes
clc; close all; clear all;

% Define input folder
infolder = 'C:\Nacho\Universidad\Prácticas Raman\LIBS_QUANTIFICATION_INTA\Spectra\RAW';

% Processing type substract DARK and calibrate X axis

% Define laser wavelength (nm)
%wvl_bb1_flight = 532.13;

% LIBS calibration coefficients (1st batch - FLIGHT)
x0 = [2.363808772E+2 3.535332588E+2 4.509610246E+2 6.914959256+2];
a1 = [6.977368338E-2 6.327125637E-2 1.388004125E-1 1.999795250E-1];
a2 = [-2.989756552E-6 -3.85818080E-6 -5.651456509E-6 -8.271906559E-6];
a3 = [-3.366447522E-10 -3.522177877E-10 -7.343665330E-10 -1.139385848E-9];

%Names of the channels 
spectrometers = {'UV1','UV2','VIS','NIR'};

% % Raman Calibration coefficients (640SP - FLIGHT) No los sabemos para BB2
% x0_R = [4.642532723E+2];
% a1_R = [1.328996462E-1];
% a2_R = [-7.301289976E-6];
% a3_R = [-5.220779717E-10];

%% Get subfolders
tmp = dir(infolder);
tmp_count = 1;
for ii = 1:size(tmp,1)
    if (tmp(ii).isdir == 1) & not(strcmp(tmp(ii).name,'.')) & not(strcmp(tmp(ii).name, '..'))
        folderlist{tmp_count} = tmp(ii).name;
        tmp_count = tmp_count+1;
    end
end

disp(['Detected folders: ' int2str(length(folderlist))]);

for ii = 1:length(folderlist)
    disp(['Processing folder ' int2str(ii) ', ' folderlist{ii}]);
    
    % Output folder is different according to processing
    [parentFolder,~,~] = fileparts(infolder);
    % count how many “_” there are
    if sum(folderlist{ii} == '_') == 1
        % split at the underscore
        parts = strsplit(folderlist{ii}, '_');
        before = parts{1};
        after  = parts{2};
        outfolder = [parentFolder '\Level0\' before '\' after];
    else
        outfolder = [parentFolder '\Level0\' folderlist{ii}];
    end
    
    % Create outfolder (if not already available)
    if not(exist(outfolder,'dir'))
        mkdir(outfolder);
    end


    %% Process LIBS spectra
    % Iterate over four spectrometers
    for zz = 1:4
        % Load DARK
        try
            filetmp = dir([infolder folderlist{ii} '\' '*SpectrometerID_' num2str(zz-1) '*_libs_DARK_*.xy']);
            if (isempty(filetmp))
                disp(['No files found on ' infolder folderlist{ii}]);
                continue;
            end
            fid1 = fopen([infolder folderlist{ii} '\' filetmp(1).name]) ;
            dark = textscan(fid1,'%f %f','delimiter',';');
            dark = cell2mat(dark);
        catch
            disp(['Error while reading ' infolder folderlist{ii} filetmp(1).name]);
            dark = zeros(2048,2);
            continue;
        end
        fclose(fid1);
        
        % Search for measurements and iterate
        filetmp = dir([infolder folderlist{ii} '\' '*SpectrometerID_' num2str(zz-1) '*_libs_raw_*.xy']);
        for nn = 1:length(filetmp)
            try
                fid1 = fopen([infolder folderlist{ii} '\' filetmp(nn).name]) ;
                data = textscan(fid1,'%f %f','delimiter',';');
                data = cell2mat(data);
            catch
                disp(['Error while reading ' infolder folderlist{ii} filetmp(nn).name]);
                return;
            end
            fclose(fid1);
            
            data_out(:,1) = double(x0(zz)+a1(zz)*data(:,1)+a2(zz)*data(:,1).^2+a3(zz)*data(:,1).^3);
            data_out(:,2) = uint16(data(:,2)-dark(:,2));

            % Create new filename
            fname = filetmp(nn).name;
            expr = 'spectrometer(\d+)_spectrum(\d+)\.xy$';
            tok = regexp(fname, expr, 'tokens');
            if ~isempty(tok)
                X = str2double(tok{1}{1});   % convierte el primer token a número
                Y = tok{1}{2};
                newname = [folderlist{ii} '_shot' Y '_' spectrometers{Y+1} '.xy'];
            else
                newname = [filetmp(nn).name(1:(strfind(filetmp(nn).name,'_libs_raw')-1)) '_processed_libs_spectrum_' num2str(zz-1) '.xy'];
            end
            
            % Write signal counts in TXT file w/o decimals and ; separator (1 row)
            dlmwrite([outfolder newname], data_out, 'delimiter',';', 'precision', '%.2f');
        end
    end
    
    % %% Process Raman spectrum
    % % Load DARK
    % try
    %     filetmp = dir([infolder folderlist{ii} '\' '*_raman_DARK_*.xy']);
    %     fid1 = fopen([infolder folderlist{ii} '\' filetmp(1).name]) ;
    %     dark = textscan(fid1,'%f %f','delimiter',';');
    %     dark = cell2mat(dark);
    % catch
    %     disp(['Error while reading ' infolder folderlist{ii}]);
    %     dark = zeros(2048,2);
    %     continue;
    % end
    % fclose(fid1);
    % 
    % % Search for measurements and iterate
    % filetmp = dir([infolder folderlist{ii} '\' '*_raman_raw_*.xy']);
    % for nn = 1:length(filetmp)
    %     try
    %         fid1 = fopen([infolder folderlist{ii} '\' filetmp(nn).name]) ;
    %         data = textscan(fid1,'%f %f','delimiter',';');
    %         data = cell2mat(data);
    %     catch
    %         disp(['Error while reading ' infolder folderlist{ii}]);
    %         continue;
    %     end
    %     fclose(fid1);
    % 
    %     data_out(:,1) = double(x0_R+a1_R*data(:,1)+a2_R*data(:,1).^2+a3_R*data(:,1).^3);
    %     data_out(:,1) = double(1E7*(1/wvl_bb1_flight - 1./data_out(:,1)));
    %     data_out(:,2) = uint16(data(:,2)-dark(:,2));
    % 
    %     % Create new filename
    %     newname = [filetmp(nn).name(1:(strfind(filetmp(nn).name,'.')-1)) '_processed.xy'];
    % 
    %     % Write signal counts in TXT file w/o decimals and ; separator (1 row)
    %     dlmwrite([outfolder newname], data_out, 'delimiter',';', 'precision', '%.2f');
    % end
end


