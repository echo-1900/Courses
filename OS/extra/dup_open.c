#include<stdio.h>
#include<sys/stat.h>
#include<sys/stat.h>
#include<fcntl.h>

int main(){
	
	int ret[3];
	int d=6;
	char buf[256];
	ret[0]=open("test.txt",O_RDONLY,S_IRUSR);
	printf("P1 fd:%d\n",ret[0]);
	ret[1]=dup(ret[0]);
	printf("P2 fd:%d\n",ret[1]);
	ret[2]=dup2(ret[0],d);
	printf("P3 fd:%d\n",ret[2]);
	while(read(d,buf,1)!=-1)
	{
		printf("%c\n",*buf);
		sleep(3);
		if(read(ret[0],buf,1)>0){
		printf("%c\n",*buf);
		sleep(3);			
		}
	}
	return 0;
}
