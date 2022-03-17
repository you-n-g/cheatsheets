



#include <pthread.h>
#include <semaphore.h>
// 编译的时候要带上   -lpthread

// reference: http://softpixel.com/~cwright/programming/threads/threads.c.php



//在 GNU/Linux下  unjoined threads are called zombies.

void *threadFunc(void *arg)
{
}

int main(void) {
    pthread_t pth;
    pthread_create(&pth,NULL,threadFunc,"processing...");
    pthread_join(pth,NULL);
    return 0;
}
