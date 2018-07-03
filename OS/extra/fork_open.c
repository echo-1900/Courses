#include<stdio.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<fcntl.h>
#include<unistd.h>

int main(){
	int i,j;
	pid_t pid;
	char buf[256];
	i=open("test.txt",O_RDONLY,S_IRUSR);
	printf("father:%d\n",i);
	pid=fork();
	if(pid<0)
		printf("error");
	else if(pid==0){
		j=open("test.txt",O_RDONLY,S_IRUSR);
		printf("child:%d\n",j);
		while(read(j,buf,1)!=-1){
			printf("%c\n",*buf);
			sleep(3);
		}
	}
	else{
		while(read(i,buf,1)!=-1){
			printf("%c\n",*buf);
			sleep(3);
		}
	}
	return 0;
}
