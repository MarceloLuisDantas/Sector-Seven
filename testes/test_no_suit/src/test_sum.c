#include <stdio.h>
#include "sum.h"

int main() {
    int total = sum(10, 10);
    if (total != 20)
        return 0;
    return 1;
}