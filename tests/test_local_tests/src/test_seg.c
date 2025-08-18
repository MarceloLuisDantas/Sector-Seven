#include <stdio.h>

int main() {
    char *str = malloc(0);
    for (int i = 0; i != 200; i++) {
        str[i] = 'a';
        printf(str[i]);
    }
}
