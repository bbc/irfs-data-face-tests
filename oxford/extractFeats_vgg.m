clear;
config.paths.net_path = 'data/vgg_face.mat';
config.paths.face_model_path = 'data/face_model.mat';

% useExtractedFaces = 1; 
% doDirs=textread('listPrimeMinisters.txt', '%s');
% featDir='PMs2_extractedFaces/';
% dataDir='~/data/PMsAll/PMs2/';

% useExtractedFaces = 0; 
% doDirs=textread('listPrimeMinisters.txt', '%s');
% featDir='PMs2/';
% dataDir='~/data/PMsAll/PMs2/';

% useExtractedFaces = 0; 
% doDirs=textread('listPrimeMinisters.txt', '%s');
% featDir='PMs/';
% dataDir='~/data/PMsAll/PMs/';

% useExtractedFaces = 0; 
% doDirs=textread('lfw.list', '%s');
% featDir='lfw/';
% dataDir='~/data/lfw/';

% useExtractedFaces = 0; 
% doDirs=textread('elvisTest.list', '%s');
% featDir='elvisPMs_last100/';
% dataDir='~/data/elvisAll/elvisPMs_last100/';

useExtractedFaces = 0; 
doDirs=textread('elvisTest.list', '%s');
featDir='elvisPMs/';
dataDir='~/data/elvisAll/elvisPMs/';

% useExtractedFaces = 0; 
% doDirs={'.'};
% featDir='elvis_notPM/';
% dataDir='~/data/elvisAll/elvis_notPM/';

convNet = lib.face_feats.convNet(config.paths.net_path);
faceDet = lib.face_detector.dpmCascadeDetector(config.paths.face_model_path);

redo = 0;

for d=1:length(doDirs)
    if useExtractedFaces
        mydir = [dataDir doDirs{d} '/extractedFaces/'];
    else
        mydir = [dataDir doDirs{d} '/'];
    end
    resDir = [featDir doDirs{d}];
    if ~exist(resDir,'dir')
        mkdir(resDir)
    end
    f=dir([mydir '*.*']);
    
    for i=1:length(f)
        imgFile=f(i).name;
        if imgFile(1) == '.'
            continue
        end
        saveFile = [resDir '/' imgFile '.vgg1'];
        if ~redo
            if exist(saveFile, 'file')
                continue
            end
        end
        disp([mydir imgFile])
        allfeat = [];
        try
            img = imread([mydir imgFile]);
        catch
            disp(['file not readable: ' mydir imgFile])
            continue
        end
        
        if ~useExtractedFaces
            % detect faces
            try
                det = faceDet.detect(img);
            catch
                disp(['face detection failed: ' mydir imgFile])
                continue
            end
            for c=1:size(det,2)
                try
                    crop = lib.face_proc.faceCrop.crop(img,det(1:4,c));
                catch
                    disp('cropping failed')
                    continue
                end
                try
                    n = convNet.simpleNN(crop);
                catch
                    disp('convNet failed')
                    continue
                end
                if size(n,2)>1
                    disp('convNet return matrix instead of vector, ignoring')
                    continue
                end
                nNorm = n./norm(n);
                allfeat = [allfeat; nNorm'];
            end
        else            
            try
                n = convNet.simpleNN(img);
            catch
                disp('problem extracting features')
                continue
            end
            if size(n,2)>1
                disp('convNet return matrix instead of vector, ignoring')
                continue
            end
            nNorm = n./norm(n);
            allfeat = nNorm';
        end
        csvwrite(saveFile, allfeat);
    end

end
