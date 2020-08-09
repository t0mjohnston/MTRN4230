kinectImage =  imread("Sample Image 1.png");
colourArg = 'blue';
shapeArg = 'circ';

centroid = processImage(kinectImage, colourArg, shapeArg);

if strcmp(centroid,'')
   disp('Error! Specified colour and or shape not present')
end

% colourMask = createMaskHSV(kinectImage,colourArg);
% colourAndShapeMask = createShapeMask(colourMask, shape);
% %imshow(colourAndShapeMask);
% 
% centroid = findObjectCentroidsFromMask(colourAndShapeMask);
% 
% showObjectAndCentroid(kinectImage, centroid)
% 
% 
% %%% shape selection
% 
% function centroid = findObjectCentroidsFromMask(colourAndShapeMask)
%     s = regionprops(colourAndShapeMask,'centroid');
%     if isempty(s.Centroid) == 0
%         centroid = "";
%         return
%     end
%     centroid = s.Centroid;
% end
% 
% function shapeMask= createShapeMask(binaryMask, shape)
%     if strcmp(shape, 'rect')
%         areaThreshLo = 2000;
%         areaThreshHi = 5000;
%         eccentThreshLo = 0.5; 
%         eccentThreshHi = 1;
%         
%     elseif strcmp(shape, 'circ')
%         areaThreshLo = 100;
%         areaThreshHi = 800;
%         eccentThreshLo = 0.05; 
%         eccentThreshHi = 0.2; 
%     else
%         shapeMask = binaryMask;
%         return;
%     end
%     
%     areaFilteredMask = bwareafilt(binaryMask, [areaThreshLo, areaThreshHi]);
%     
%     eccentAndAreaMask = bwpropfilt(areaFilteredMask, 'Eccentricity', [eccentThreshLo, eccentThreshHi]);
% 
%     %imfind circles if need be???
% 
%     shapeMask = eccentAndAreaMask;
% end
% 
% function showObjectAndCentroid(image, centroid)
%     imshow(image);
%     hold on;
%     plot(centroid(1), centroid(2), 'g*')
%     hold off;
% end
% 
