int main(void) {
    int i, j, temp;
    int array[8]={100,1,88,54,3,4,78,55};
    for(i = 0; i < 8; i++) {
        j = i;
        while(j > 0 && array[j - 1] > array[j]) {
            temp = array[j - 1];
            array[j - 1] = array[j];
            array[j] = temp;
            j--;
        }
        for(j = 0; j <= i; j++) {
            printf("%d ", array[j]);
        }
        printf("\n");
        }
        return 0;
}