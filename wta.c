#include<string.h>
#include<time.h>
#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include"hand.h"

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
	hand * data = malloc(10*NLINES*sizeof(hand));
	hand * mu = malloc(10*NCLUSTERS*sizeof(hand));

	//fill data
	for(int i = 0; i < NLINES; i++){
		char * tmp;
		fgets(buf,255,in);
		tmp = strtok(buf,",");
		for(int j = 0; j < 10; j++){
			data[i].cards[j] = atof(tmp);
			tmp = strtok(NULL,",");
		}
	}

	//randomly fill mu
	time_t t;
	srand((unsigned)time(&t));
	for(int i = 0; i < NCLUSTERS; i++){
		int tmp = rand() % NLINES;
		for(int j = 0; j < 10; j++){
			mu[i].cards[j] = data[tmp].cards[j];
		}
	}
	
	//---------Perform WTA----------
	for(int i = 0; i < NLINES; i++)
		update_mu(&data[i],mu,NCLUSTERS);
	//print mu	
	for(int i = 0; i < NCLUSTERS; i++){
		for(int j = 0; j < 10; j++){
			printf("%lf ",mu[i].cards[j]);
		}
		printf("\n");
	}

	//---------Cleanup----------
	free(data);
	free(mu);
	fclose(in);
}
