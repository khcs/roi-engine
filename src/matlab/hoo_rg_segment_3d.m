function J = hoo_rg_segment_3d(I, x, y, z)

% 3D Region Growing Segmentation tool
% Author: Hoo Chang Shin
% Hoo.Shin@icr.ac.uk
% 08.Jan.10
% 
% Modified regiongrowing.m of D. Kroon
% (http://www.mathworks.com/matlabcentral/fileexchange/19084-region-growing
% )
% for 3D image.


% Maximum intensity distance
reg_maxdist=0.1; % set to 0.2 as default


J = zeros(size(I)); % Output
Isizes = size(I); % Dimensions of input image

reg_mean = I(x,y,z); % The mean of the segmented region
reg_size = 1; % Number of pixels in region

% Free memory to store neighbors of the (segmented) region
neg_free = 10000; neg_pos = 0;
neg_list = zeros(neg_free, 4);

pixdist = 0; % Distance of the region newest pixel to the regio mean

% Neighbor locations (footprint)
neigb = [-1 0 0; 1 0 0; 0 -1 0; 0 1 0; 0 0 -1; 0 0 1];

% Start regiongrowing until distance between regio and possible new pixels
% become higher than a certain threshold
while(pixdist<reg_maxdist&&reg_size<numel(I))
    
    % Add new neighbors pixels
    for j=1:6
        % Calculate the neighbor coordinate
        xn = x + neigb(j,1); yn = y + neigb(j,2); zn = z + neigb(j,3);
        
        % Check if neighbor is inside or outside the image
        ins=(xn>1)&&(yn>=1)&&(zn>=1)&&(xn<=Isizes(1))&&(yn<=Isizes(2))&&(zn<=Isizes(3));
        
        % Add neighbor if inside and not already part of the segmented area
        if(ins&&(J(xn,yn,zn)==0))
            neg_pos = neg_pos+1;
            neg_list(neg_pos,:) = [xn yn zn I(xn,yn,zn)]; J(xn,yn,zn)=1;
        end
    end
    
    % Add a new block of free memory
    if(neg_pos+10>neg_free), neg_free=neg_free+10000; neg_list((neg_pos+1):neg_free,:)=0; end
    
    % Add pixel with intensity nearest to the mean of the region, to the
    % region
    dist = abs(neg_list(1:neg_pos,4)-reg_mean);
    [pixdist, index] = min(dist);
    J(x,y,z)=2; reg_size=reg_size+1;
    
    % Calculate the new mean of the region
    reg_mean = (reg_mean*reg_size + neg_list(index,4))/(reg_size+1);
    
    % Save the x and y and z coordinates of the pixel (for the neighbor and
    % process)
    x = neg_list(index,1); y = neg_list(index,2); z = neg_list(index,3);
    
    % Remove the pixel from the neighbor (check) list
    neg_list(index,:)=neg_list(neg_pos,:); neg_pos=neg_pos-1;
end

% Return the segmented area as logical matrix
J=J>1;
