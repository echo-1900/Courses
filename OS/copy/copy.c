#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>


int main(int arge,char **argv)
{
    int fd_in = 0;
    int fd_out = 0;
    int n_read = 0;
    int n_write = 0;
    char buf[1024];
    //1.open source file
    fd_in = open(argv[1],O_RDONLY);

    //2.open destination file
    fd_out = open(argv[2],O_RDWR|O_CREAT,0755);

    //3.read source file
    while((n_read = read(fd_in,buf,1024)) > 0)
    {       
        printf("read %s: %d bytes!\n",argv[1],n_read);
        n_write = write(fd_out,buf,n_read);
        printf("write %s: %d bytes!\n",argv[2],n_write);
    }
    close(fd_in);
    close(fd_out);
    //4.write destination

    return 0;

}