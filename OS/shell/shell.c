#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#define MAX_LINE 1024 //命令长度限制


char *history[10]; //历史命令数组
int count=0;       //当前数组中命令数目

int print_history(){
	int i,j;
	if(count>9)
		j=9;
	else
		j=count;
	printf("Command history:\n");
	for(i=j;i>=0;i--)
		printf("%d. %s\n",i,history[i]);
	return 0;
}

int format_command(char input_buffer[], char *args[], int *wait_flag){
	//buff用于缓存待处理命令，args用于存处理过的命令，wait_flag标识是否要后台执行
	int i;
	int j=0;
	int length;
	char * s; //用于临时存分割后得到的小字符串

	//读取标准输入到input_buffer并返回长度
	length=read(STDIN_FILENO,input_buffer,MAX_LINE); 
	//读取命令失败时错误处理
	if(length<=0){
		printf("Command not read!\n");
		return -1;
	}
	//读取成功则将其加入历史
	else{
		history[count++%10]=input_buffer;
	}
	//分割输入的命令
	s=strtok(input_buffer," ");
	while(s){
		args[j]=s;
		s=strtok(NULL," ");
		j++;
	}
	args[j-1][strlen(args[j-1])-1]=0; //去除回车字符
	//判断是不是后台执行
	//因为读入的时候会读入回车为一个字符，所以此处采取讨巧的办法比较字符，但是存在安全隐患
	if(args[j-1][0]=='&')
		*wait_flag=1; 

	//如果是history命令则打印历史命令
	if(strcmp(args[0],"history")==0){		
        if(count>0){
            print_history();
		}
		else{
			printf("\nNo Commands in the history\n");
			return -1;
		}
    }
}



int main(){
	int flag;  //当存在&时flag置1
	char input_buffer[MAX_LINE];
	char *args[MAX_LINE/2+1];
	pid_t pid;
	//shell循环的标志位
	int should_run=1;

	while(should_run){
		flag=0;
		printf("osh>");
		fflush(stdout);
		if(-1!=format_command(input_buffer,args,&flag)){
			pid=fork();
			if(pid<0){
				printf("Fork failed.");
				exit(1);
			}
			else if(pid==0){
				if(execvp(args[0],args)==-1)
					printf("Execute failed.\n");
			}
			else{
				if(flag==0)   //表明此时子进程没有声明要在后台执行
					wait(NULL);
			}
		}
	}

}