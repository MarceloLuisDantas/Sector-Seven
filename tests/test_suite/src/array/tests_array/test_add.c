#include <stdio.h>
#include "../array.h"

int main() {
    Array *a1 = new_array(2);
    if (!add(a1, 10)) {
        printf("Should be able to add more elements\n");
        return 0;
    }

    if (!add(a1, 20)) {
        printf("Should be able to add more elements\n");
        return 0;
    }

    if (add(a1, 20)) {
        printf("Should not be able to add more elements\n");
        return 0;
    }

    printf("Everthing OK\n");
    return 1;
}