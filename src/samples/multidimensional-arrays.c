#include <stdio.h>

int main() {
    // const int aa[2][3][4] = {
    //   {
    //     {10, 11, 10, 11}, {12, 13, 12, 13}, {12, 345, 568, 1}
    //   },
    //   {
    //     {14, 15, 14, 15}, {16, 17, 16, 17}, {41, 345, 74, 34}
    //   }
    // };

    // const int a[][2][2] = {
    //     {
    //         {10, 11}, {12, 13}
    //     },
    //     {
    //         {14, 15}, {16, 17}
    //     }
    // };
    //
    // const int arr[] = {10, 20, 30};
    //
    // printf("%i\n", *(**a + 1));
    // printf("%i\n", a[0][1][0]);
    // printf("%i\n", *(arr+1) + 1);


    int n = 5;
    int *nn = &n;
    int **nnn = &nn;
    int arr2[n];

    int * josse [10] = { nn, nn, nn, nn, nn, nn, nn, nn, nn, nn };

    // TODO: bij het alloceren van een array, allocceer vanaf de bovenkant van TypeInfo.indirections tot dat je een niet-array indirectie tegenkomt
    int *(* a2[2])[10] = { &josse, &josse };
    a2[0] = &josse;

    // int ** a2[5][10] = {
    //     { 0, 1, 2, 2 },
    //     { 0, 1, 2 },
    //     { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    //     { 0, 0, 0, 0, 0, 0, 7, 0, 0, 0 },
    //     { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }
    // };

    // int *a3 = a[2];

    // printf("%i, %i\n", a2[1][2], a2[3][6]);

    // int a4 = 1, b = 2, c[] = {1, 2}, d[][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, f[] = {};
    //
    // f[100] = 40;
    // printf("%i\n", f[100]/*[12]*/);
}
