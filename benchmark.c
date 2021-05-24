#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <getopt.h>
#include <sys/sysinfo.h>

const unsigned int LIMIT = 5000000;

double* x;
double* y;
int* BENCHMARK_DIFFICULTY = 0;
int* childs = 0;
int child_counter = 0;

void bench() {
    double temp = 0;
    printf("%d --> Benchmark started | Difficulty: %u\n" , getpid() , *BENCHMARK_DIFFICULTY);
    fflush(stdout);

    for ( unsigned int repetition = 0; repetition < *BENCHMARK_DIFFICULTY;repetition++ ) {
        for ( unsigned int i = 0; i < LIMIT;i++ ) {
            temp = (x[i] * y[i]) + (x[i] / x[i]) * (y[i] / x[i]);
        }
    }
    exit(0);
}

void usage() {
    printf("<USAGE: --cores {positive number > 0}[default: system cores] --difficulty {positive number > 0}[default: 100] >\n");
    exit(1);
}

void beginMessage(int processes , int difficulty) {
    printf("CORES: %d | DIFFICULTY: %d \n" , processes , difficulty);
}
void onAbort(int dummy) {
    for ( int i = 0; i < child_counter; i++ )
        kill(childs[i] , SIGKILL);
    printf("\nBENCHMARK ABORTED\n");
    fflush(stdout);
    exit(0);
}

int main(int argc , char** argv) {
    signal(SIGINT , onAbort);
    if ( (argc - 1) % 2 != 0 || (argc - 1) > 4 )
        usage();



    BENCHMARK_DIFFICULTY = ( int* )mmap(NULL , sizeof(int) ,
        PROT_READ | PROT_WRITE ,
        MAP_SHARED | MAP_ANONYMOUS ,
        0 , 0);


    bool asigned_cores = false , assigned_DIFFICULTY = false;

    int PROCESSES = -1;
    *BENCHMARK_DIFFICULTY = -1;
    int opt = 0;
    struct option long_options[ ] = {
        {"cores",      optional_argument,       NULL,  'c' },
        {"difficulty", optional_argument,       NULL,  'd' },
        {NULL,           0,                 NULL,  0   }
    };

    int long_index = 0;
    while ( (opt = getopt_long(argc , argv , "cd" ,
        long_options , &long_index)) != -1 ) {
        switch ( opt ) {
        case 'c':
            if ( !(argv[optind][0] > 48 && argv[optind][0] < 58) )
                usage();
            PROCESSES = atoi(argv[optind]);
            if ( PROCESSES != 0 )
                asigned_cores = true;
            break;
        case 'd':
            if ( !(argv[optind][0] > 48 && argv[optind][0] < 58) )
                usage();
            *BENCHMARK_DIFFICULTY = atoi(argv[optind]);
            if ( *BENCHMARK_DIFFICULTY != 0 )
                assigned_DIFFICULTY = true;
            break;
        default:
            usage();
        }
    }
    if ( assigned_DIFFICULTY || asigned_cores && argc > 1 ) {
        if ( !asigned_cores && PROCESSES < 1 && !assigned_DIFFICULTY && *BENCHMARK_DIFFICULTY < 1 ) {
            usage();
        }
    }
    else if ( argc == 1 ) {}
    else
        usage();

    if ( PROCESSES < 1 ) {
        PROCESSES = get_nprocs();
    }
    if ( *BENCHMARK_DIFFICULTY < 1 ) {
        *BENCHMARK_DIFFICULTY = 100;
    }

    beginMessage(PROCESSES , *BENCHMARK_DIFFICULTY);
    if ( !asigned_cores ) {
        printf("no argument for cores, using default: %d\n" , PROCESSES);
    }
    if ( !assigned_DIFFICULTY ) {
        printf("no argument for difficulty, using default: %d\n" , *BENCHMARK_DIFFICULTY);
    }


    srand(time(NULL));
    printf("Generating benchmark data...\n");
    x = ( double* )mmap(NULL , LIMIT * sizeof(double) ,
        PROT_READ | PROT_WRITE ,
        MAP_SHARED | MAP_ANONYMOUS ,
        0 , 0);

    y = ( double* )mmap(NULL , LIMIT * sizeof(double) ,
        PROT_READ | PROT_WRITE ,
        MAP_SHARED | MAP_ANONYMOUS ,
        0 , 0);




    for ( unsigned int i = 0; i < LIMIT;i++ )
        x[i] = ( double )rand() / RAND_MAX * 2.0 - 1.0;

    for ( unsigned int i = 0; i < LIMIT;i++ )
        y[i] = ( double )rand() / RAND_MAX * 2.0 - 1.0;


    printf("Benchmark data generated!\n");

    printf("Starting processes...\n");
    fflush(stdout);
    childs = malloc(sizeof(int) * PROCESSES);
    for ( int i = 0; i < PROCESSES;i++ ) {
        int child = fork();
        if ( child == 0 ) {
            signal(SIGINT , SIG_DFL);
            signal(SIGUSR1 , bench);
            pause();
            exit(0);
        }
        childs[i] = child;
        child_counter++;
    }

    sleep(2);

    struct timespec begin , end;
    pid_t wpid;
    int status = 0;




    for ( int i = 0; i < PROCESSES; i++ ) {
        if ( i == 0 ) clock_gettime(CLOCK_REALTIME , &begin);
        kill(childs[i] , SIGUSR1);
    }

    while ( (wpid = wait(&status)) > 0 );

    clock_gettime(CLOCK_REALTIME , &end);
    double elapsed = (end.tv_sec - begin.tv_sec) + (end.tv_nsec - begin.tv_nsec) * 1e-9;

    printf("Benchmark finished in %.3lf seconds!\n" , elapsed);
    return 0;
}