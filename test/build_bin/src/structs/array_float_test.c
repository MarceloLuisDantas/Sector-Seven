#include <stdio.h>
#include <math.h>

#include "array_float.h"

int float_equals(float a, float b, float epsilon) {
    return fabs(a - b) < epsilon;
}

int main() {

    ArrayFloat *af = newArrayFloat(5);
    int x = addFloat(af, 10.20);

    if (float_equals(af->array[0], 10.2, 1e-5)) {
        printf("Ok float\n");
        return 0;
    } 

    printf("%f\n", af->array[0]);
    return 1;
}