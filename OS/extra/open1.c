#include<stdio.h>
#include<sys/stat.h>
#include<sys/stat.h>
#include<fcntl.h>

main(){
        int ret;
        ret = open("1.txt", O_RDONLY);
        printf("%d\n",ret);
}
