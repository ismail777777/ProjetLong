#include <stdio.h>

typedef struct {
    int x;
    int y;
} Point;

typedef struct {
    int red;
    int green;
    int blue;
} Color;

struct Complex {
    double real;
    double imag;
};

struct Compilation{
    double real;
    double imag;
};

Point g_point;
int g_int;
int *g_pointer;


void printPoint(Point p) {
    Complex z;
    printf("Point: (%d, %d)\n", p.x, p.y);
    if (true) {
        //...
    }
}

void printColor(Color c, Point p) {
    printPoint(p);
    printPoint(point);
    g_int = 0;
    printf("Color: (R:%d, G:%d, B:%d)\n", c.red, c.green, c.blue);
}

void printComplex(Complex z) {
    printf("Complex Number: %.2f + %.2fi\n", z.real, z.imag);
}

void modifyValues(int *ptr) {
    printPoint(g_point);
    (*ptr)++;
}

void modifyPoint(Point *p, int * ptr) {
    modifyPoint(ptr);
    p->x++;
    p->y++;
}

void printPointAndColor(Point p, Color c) {
    printPoint(p);
    printColor(c);
}

int main() {
    modifyValues(g_pointer);
    
    int num = 10;
    int *ptr = &num;
    g_int++;
    printf("Original Values:\n");
    printPoint(point);
    printColor(color);
    printComplex(complexNum);
    printf("Integer value: %d\n", num);
    if(true){
        //....
    }
    modifyPoint(&point);
    modifyValues(ptr);

    printf("\nModified Values:\n");
    printPointAndColor(point, color);
    printComplex(complexNum);
    printf("Integer value: %d\n", num);

    return 0;
}