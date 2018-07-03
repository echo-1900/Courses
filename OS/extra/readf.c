#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

int main() {
    int in1,in2;
    char buffer[256];
    in1 = open("test.txt", O_RDONLY);
    in2 = open("test.txt", O_RDONLY);
    printf("fd:%d\n",in1);
    printf("fd:%d\n",in2);    
    while(read(in1, buffer, 1) > 0){
        printf("%c\n", *buffer);
	    sleep(3);
        if(read(in2, buffer, 1) > 0){
            printf("%c\n", *buffer);
            sleep(3);
        }

    }
    close(in1);
    close(in2);
    return 0;
}
