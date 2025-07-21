#include <stdio.h>
#include "../array.h"

int main() {
    Array *a1 = newArray(10);
    Array *a2 = newArray(10);
    Array *a3 = concat(a1, a2);
    
    if (a3->max != 20) {
        printf("Not Ok\n");
        return 0;
    }
    printf("Ok\n");
    return 1;
}