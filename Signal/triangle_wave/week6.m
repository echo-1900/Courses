function output = square_wave(n)
output = [];
unit = 4*pi/1000;
for i=0:1000
    t=i*unit;
    tmp=0;
    for k=1:n
        tmp=tmp+sin((2*k-1)*t)/(2*k-1);
    end
    output=[output,tmp]
end
end
