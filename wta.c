#include<string.h>
#include<time.h>
#include<stdio.h>
#include<math.h>
#include<stdlib.h>

static int NCLUSTERS;
static int NLINES = 0;

int main(int argc, char ** argv)
{
//----------File IO---------
    FILE * in;
    in = fopen(argv[1],"r");
    if (argc != 3) return 0;
     NCLUSTERS = atoi(argv[2]);
    
    //Get numLines
    char buf[255];
    while(fgets(buf,255,in) != NULL){
	NLINES++;
    }
    rewind(in);

    //create arrays
    int * data = malloc(10*NLINES*sizeof(int));
    double * mu = malloc(10*NCLUSTERS*sizeof(double));
    for(int i = 0; i < NLINES; i++){
	char * tmp;
	fgets(buf,255,in);
	tmp = strtok(buf,",");
	for(int j = 0; j < 10; j++){
	    data[10*i+j] = atoi(tmp);
	    tmp = strtok(NULL,",");
	}
    }
    time_t t;
    srand((unsigned)time(&t));
    for(int i = 0; i < NCLUSTERS; i++){
	int tmp = rand() % NLINES;
	for(int j = 0; j < 10; j++){
	    mu[10*i+j] = data[10*tmp+j];
	}
    }
    for(int i = 0; i < NCLUSTERS; i++){
	for(int j = 0; j < 10; j++){
	    printf("%lf ",mu[10*i+j]);
	}
	printf("\n");
    }

//---------Cleanup----------
    free(data);
    free(mu);
    fclose(in);
}
