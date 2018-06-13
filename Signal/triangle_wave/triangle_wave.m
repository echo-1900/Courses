function output = triangle_wave(n)
output = [];
unit = 4*pi/1000;
for i=0:1000
    t=i*unit;
    tmp=0;
    for k=0:n
        tmp=tmp+(-1)^k*sin((2*k+1)*t)/((2*k+1)^2);
    end
    output=[output,tmp];
end
end
