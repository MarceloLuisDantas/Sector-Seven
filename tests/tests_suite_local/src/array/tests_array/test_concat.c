#include <stdio.h>
#include "../array.h"

int main() {
    Array *a1 = new_array(2);
    add(a1, 10);

    Array *a2 = new_array(2);
    add(a2, 20);
    add(a2, 30);

    Array *a3 = concat(a1, a2);
    if (a3->size != 4) {
        printf("Size should be 4, but is %d\n", a3->size);
        return 0;
    }

    if (a3->len != 3) {
        printf("Len should be 3, but is %d\n", a3->len);
        return 0;
    }

    printf("Everything OK\n");
    return 1;
}