#include <stdio.h>

int main() {
    int c;
    float f;

    for (c = 0; c <= 100; c++) {
        if (c == 0) {
            printf("Celsius Fahrenheit\n");
        }
        
        if (c % 10 == 0) {
            f = (c * 1.8) + 32;
            printf("%d\t%.1f\n", c, f);
        }
    }

    return 0;
}