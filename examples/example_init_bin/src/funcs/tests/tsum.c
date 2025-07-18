#include <stdio.h>
#include "../sum.h"

int main() {
    int num = sum(10, 20);
    if (num != 30) {
        printf("Not Ok - num should be 30, but got %d\n", num);
        return 0;
    }
    printf("Num Ok - %d\n", num);
    return 1;
}