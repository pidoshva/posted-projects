% Vadym Pidoshva
% Image Compression Project
% CS_3320
% Date Completed: Aug, 7, 2022
% ----------------------------------


x = imread("DSC_1662a.tif");
x = double(x);

[rows, cols] = size(x);
cols=cols/3;
colors = 3;

p=6;
Q=p*8./hilb(8);

% Compression
r=1;
CompImg = zeros(rows, cols);
while r <= (rows-7)
    c=1;
    while c <= (cols - 7)
        color=1;
        while color <= colors 
            xb = x(r:r+7,c:c+7,color);
            xc=xb-128;
            Y=dctC*xc;
            Y=Y*dctC';
            Yq=round(Y./Q); % Yq = compressed image
            CompImg(r:r+7,c:c+7,color) = Yq;

            color=color+1;
        end
        c=c+8;
    end
    r=r+8;
end

% Decompression
r=1;
DecompImg = zeros(rows, cols);
while r <= rows-7
    c=1;
    while c <= cols-7
        color=1;
        while color <= colors
            Yq = CompImg(r:r+7,c:c+7,color);
            Ydq=Yq.*Q;
            Xdq=dctC'*Ydq*dctC;
            Xe=Xdq+128; % Xe = decompressed image
            DecompImg(r:r+7,c:c+7,color) = Xe;

            color=color+1;
        end
        c=c+8;
    end
    r=r+8;
end

DecompImg=uint8(DecompImg);

% Displaying image
imshow(DecompImg)
% Saving image
imwrite(DecompImg,'DSC_1662a_p6_usable.jpg');

% DCT
function C=dctC()
n=8;
for i=1:n
    for j=1:n
       C(i, j) = cos((i-1)*(2*j-1)*pi/(2*n));
  end
end
C = sqrt(2/n) * C;
C(1, :) = C(1, :) / sqrt(2);
end
