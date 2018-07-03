#include<stdio.h>
#include<sys/stat.h>
#include<fcntl.h>

int main(){
	int ret[3] = {0};
	ret[0] = open("1.txt", O_RDONLY);
	ret[1] = open("2.txt", O_RDONLY);
	ret[2] = open("3.txt", O_RDONLY);
	ret[3] = open("4.txt", O_RDONLY);
	printf("%2d %2d %2d %2d\n",ret[0],ret[1],ret[2],ret[3]);
	return 0;
}

