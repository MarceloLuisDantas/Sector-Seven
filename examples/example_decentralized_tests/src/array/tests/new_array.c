#include <stdio.h>
#include "../array.h"

int main() {
    Array *a1 = newArray(10);
    if (a1->max != 10) {
        printf("Not Ok\n");
        return 0;
    }
    printf("Ok\n");
    return 1;
}