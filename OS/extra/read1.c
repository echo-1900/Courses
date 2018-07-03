#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

int main() {
    int in1;
    char buffer[256];
    in1 = open("test.txt", O_RDONLY); 
    while(read(in1, buffer, 1) > 0){
        printf("%c\n", *buffer);
	    sleep(3);
    }
    close(in1);
    return 0;
}
