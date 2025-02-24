#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Мин-куча (бинарная куча)
typedef struct {
    int *heap;
    int size;
    int capacity;
} MinHeap;

MinHeap* create_minheap(int capacity) {
    MinHeap* heap = (MinHeap*)malloc(sizeof(MinHeap));
    heap->size = 0;
    heap->capacity = capacity;
    heap->heap = (int*)malloc(capacity * sizeof(int));
    return heap;
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void heapify(MinHeap *heap, int idx) {
    int smallest = idx;
    int left = 2 * idx + 1;
    int right = 2 * idx + 2;

    if (left < heap->size && heap->heap[left] < heap->heap[smallest])
        smallest = left;
    if (right < heap->size && heap->heap[right] < heap->heap[smallest])
        smallest = right;
    if (smallest != idx) {
        swap(&heap->heap[idx], &heap->heap[smallest]);
        heapify(heap, smallest);
    }
}

void insert_minheap(MinHeap *heap, int key) {
    if (heap->size == heap->capacity) {
        printf("Overflow: Heap is full!\n");
        return;
    }

    int i = heap->size++;
    heap->heap[i] = key;
    while (i != 0 && heap->heap[(i - 1) / 2] > heap->heap[i]) {
        swap(&heap->heap[i], &heap->heap[(i - 1) / 2]);
        i = (i - 1) / 2;
    }
}

int extract_min(MinHeap *heap) {
    if (heap->size <= 0) return -1;
    if (heap->size == 1) return heap->heap[--heap->size];

    int root = heap->heap[0];
    heap->heap[0] = heap->heap[--heap->size];
    heapify(heap, 0);

    return root;
}

int get_min(MinHeap *heap) {
    return (heap->size > 0) ? heap->heap[0] : -1;
}

// Биноминальная куча
typedef struct BinomialNode {
    int key;
    int degree;
    struct BinomialNode *parent, *child, *sibling;
} BinomialNode;

typedef struct {
    BinomialNode *head;
} BinomialHeap;

BinomialHeap* create_binomial_heap() {
    BinomialHeap *heap = (BinomialHeap*)malloc(sizeof(BinomialHeap));
    heap->head = NULL;
    return heap;
}

BinomialNode* create_binomial_node(int key) {
    BinomialNode *node = (BinomialNode*)malloc(sizeof(BinomialNode));
    node->key = key;
    node->degree = 0;
    node->parent = node->child = node->sibling = NULL;
    return node;
}

void merge_binomial_heaps(BinomialHeap *heap1, BinomialHeap *heap2) {
    // Реализация слияния двух биноминальных куч
}

void insert_binomial_heap(BinomialHeap *heap, int key) {
    // Реализация вставки в биноминальную кучу
}

int extract_min_binomial_heap(BinomialHeap *heap) {
    // Реализация удаления минимума из биноминальной кучи
    return -1;
}

// Функция для тестирования
void run_tests() {
    int sizes[] = {1000, 10000, 100000, 1000000, 10000000}; // Для N = 10^i, где i от 3 до 7
    int num_sizes = 5;

    srand(time(NULL));

    for (int i = 0; i < num_sizes; i++) {
        int size = sizes[i];
        printf("Running tests for N=%d\n", size);

        // Генерация случайных данных
        int *data = (int*)malloc(size * sizeof(int));
        for (int j = 0; j < size; j++) {
            data[j] = rand() % 1000000;
        }

        // Тестирование MinHeap
        MinHeap *min_heap = create_minheap(size);
        clock_t start_time = clock();
        for (int j = 0; j < size; j++) {
            insert_minheap(min_heap, data[j]);
        }
        double minheap_insert_time = (double)(clock() - start_time) / CLOCKS_PER_SEC;

        start_time = clock();
        for (int j = 0; j < 1000; j++) {
            get_min(min_heap);
        }
        double minheap_search_time = (double)(clock() - start_time) / CLOCKS_PER_SEC / 1000;

        start_time = clock();
        for (int j = 0; j < 1000; j++) {
            extract_min(min_heap);
        }
        double minheap_remove_time = (double)(clock() - start_time) / CLOCKS_PER_SEC / 1000;

        printf("MinHeap - Insert: %f, Search: %f, Remove: %f\n", minheap_insert_time, minheap_search_time, minheap_remove_time);

        // Тестирование BinomialHeap (аналогично)
        BinomialHeap *binomial_heap = create_binomial_heap();
        start_time = clock();
        for (int j = 0; j < size; j++) {
            insert_binomial_heap(binomial_heap, data[j]);
        }
        double binomial_insert_time = (double)(clock() - start_time) / CLOCKS_PER_SEC;

        start_time = clock();
        for (int j = 0; j < 1000; j++) {
            extract_min_binomial_heap(binomial_heap);
        }
        double binomial_remove_time = (double)(clock() - start_time) / CLOCKS_PER_SEC / 1000;

        printf("BinomialHeap - Insert: %f, Remove: %f\n", binomial_insert_time, binomial_remove_time);

        free(data);
    }
}

int main() {
    run_tests();
    return 0;
}
