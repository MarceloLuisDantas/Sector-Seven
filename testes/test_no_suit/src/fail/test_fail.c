#include <stdio.h>
#include <stdbool.h>
#include "fail.h"

int main() {
    printf("STDIO of the test_fail\n");

    if (fail(false)) 
        return 0;
    
    return 1;
}