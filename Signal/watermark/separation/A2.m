I1=imread('A2.png');%梦露&爱因斯坦
g1=rgb2gray(I1);
s=fftshift(fft2(g1));
[M,N]=size(s);
s1=zeros(M,N);
s2=zeros(M,N);
n1=fix(M/2);
n2=fix(N/2);

%理想低通滤波器取d0=10  （15,30）可变
d0=12;
for i=1:M
    for j=1:N
        d=sqrt((i-n1)^2+(j-n2)^2);
        if d<d0
            h=1;
        else
            h=0;
        end
        s1(i,j)=h*s(i,j);
    end
end
s1=ifftshift(s1);
s1=uint8(real(ifft2(s1)));
figure(1);
imshow(s1);
imwrite(s1,'she.jpg','JPG');

%理想高通滤波器取d02=5  （15,30）可变
d02=12;
for i=1:M
    for j=1:N
        d=sqrt((i-n1)^2+(j-n2)^2);
        if d<d02
            h=0;
        else
            h=1;
        end
        s2(i,j)=h*s(i,j);
    end
end
s2=ifftshift(s2);
s2=uint8(real(ifft2(s2)));
figure(2);
imshow(s2);
imwrite(s2,'he.jpg','JPG');

