#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
 
#define SIZE 10
 
void *sorter(void *params);    //排序函数
void *merger(void *params);    //合并函数
 
int list[SIZE] = {7,12,19,3,18,4,2,6,15,8};
int result[SIZE];//题中所说的新数组，用于线程三的排序
 
//由于创建线程时只能传一个参数，
//因此把多个参数整合到一个结构体中
typedef struct{
    int from_index;
    int to_index;
} parameters;
 
int main (int argc, const char * argv[]) {
    int i;
    pthread_t workers[3];
    //线程1，排序前半段
    parameters *data1 = (parameters *) malloc (sizeof(parameters));
    data1->from_index = 0;
    data1->to_index = SIZE/2;
    pthread_create(&workers[0], NULL, sorter, data1);
    pthread_join(workers[0], NULL);
    free(data1);
    //线程2，排序后半段
    parameters *data2 = (parameters *) malloc (sizeof(parameters));
    data2->from_index = SIZE/2;
    data2->to_index = SIZE;
    pthread_create(&workers[1], NULL, sorter, data2);
    pthread_join(workers[1], NULL);
    free(data2);
    //线程3，排序新数组
    parameters *data3 = (parameters *) malloc(sizeof(parameters));
    data3->from_index = 0;
    data3->to_index = SIZE;
    pthread_create(&workers[2], NULL, merger, data3);
    pthread_join(workers[2], NULL);
    free(data3);          
    return 0;
}
 
void *sorter(void *params){
    parameters* p = (parameters *)params;
    int begin = p->from_index;
    int end = p->to_index;
    int i,j,k;
    //排序前打印
    for(i = begin; i<end; i++)
        printf(" %d ", list[i]);
    printf("\n");
    //开始排序
    for(i=0; i<end-begin; i++){
        for(j=begin; j<end-i-1; j++){
            if(list[j] > list[j+1]){
                k = list[j];
                list[j] = list[j+1];
                list[j+1] = k;     
            }
        }
    } 
    //排序后打印
    for(i = begin; i<end; i++)
        printf(" %d ", list[i]);
    printf("\n");
    //将排序后的原数组的值赋值给result数组
    for(i=begin; i<end; i++)
        result[i]=list[i];
    pthread_exit(0);
}
 

void *merger(void *params){
    parameters* p = (parameters *)params;
    int begin = p->from_index;
    int end = p->to_index;
    int i,j,k;
    //排序前打印
    for(i = begin; i<end; i++)
        printf(" %d ", result[i]);
    printf("\n");
    //排序新数组
    for(i=begin; i<end; i++){
        for(j=begin; j<end-i-1; j++){
            if(result[j] > result[j+1]){
                k = result[j];
                result[j] = result[j+1];
                result[j+1] = k; 
            }
        }
    }
    //排序后打印
    for(i = begin; i<end; i++)
        printf(" %d ", result[i]);
    printf("\n");

    pthread_exit(0);
}