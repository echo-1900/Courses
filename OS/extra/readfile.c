#include<stdio.h>
#include<sys/stat.h>
#include<sys/stat.h>
#include<fcntl.h>
#include<unistd.h>
#include<errno.h>

int main(){
	int i;
	int j;
	char *buf;
	i = open("test.txt",O_RDONLY);
	printf("fd:%d\n",i);
	if(j = read(i,buf,1)<0)
	{
	perror("read:");
	}
	while(read(i,buf,1) != -1)
	{
		printf("%c\n",*buf);
		sleep(3);
	}
	close(i);
	return 0;
}
