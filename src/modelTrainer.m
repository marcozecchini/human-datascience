rootFolder = fullfile('..\dataset', 'base');

imagesPath = fullfile(rootFolder, 'statues_faces');

imgSets = [imageSet(fullfile(imagesPath, 'afrodite')),
            imageSet(fullfile(imagesPath, 'apollo')),
            imageSet(fullfile(imagesPath, 'atena')),
            imageSet(fullfile(imagesPath, 'amazzone')),
            imageSet(fullfile(imagesPath, 'atleta')),
            imageSet(fullfile(imagesPath, 'eracle')),
            imageSet(fullfile(imagesPath, 'era-minerva')),
            imageSet(fullfile(imagesPath, 'hermes')),
            imageSet(fullfile(imagesPath, 'menandro'))
            ];

%prints the categories labels
{imgSets.Description}

%prints the number of pics for each category used for the model
[imgSets.Count]

%balance dataset
if 0
    %min number of images in a category
    minSetCount = min([imgSets.Count]); 

    %making all the sets of the same size
    imgSets = partition(imgSets, minSetCount, 'randomize');
end

%prints the number of pics for each category used for the model(all the same number
[imgSets.Count]

%partitioning in training set and validation set
[trainingSets, validationSets] = partition(imgSets, 0.7, 'randomize');


%extracting features and creating visual words
bag = bagOfFeatures(trainingSets, 'VocabularySize', 2500);

%training model
categoryClassifier = trainImageCategoryClassifier(trainingSets, bag);

%creating confusion matrix on the training set
confMatrix = evaluate(categoryClassifier, trainingSets);

% Compute average accuracy
mean(diag(confMatrix));

%creating confusion matrix on the validation set
confMatrix = evaluate(categoryClassifier, validationSets);

% Compute average accuracy
mean(diag(confMatrix));
