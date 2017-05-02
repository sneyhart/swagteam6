/*
 * wta.c
 * Sam Neyhart
 * This file contains the wta program used in the final project of 
 * ECE 471.
 * USAGE: wta filename.data nclusters
 */

#include<string.h>
#include<time.h>
#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include"hand.h"


static const int ITERATIONS = 1; //How many times to go through data
static const int NCLASSES = 10;
static const int NCARDS = 10;
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
	hand * data = malloc(NLINES*sizeof(hand));
	hand * mu = malloc(NCLUSTERS*sizeof(hand));
	int * clas = malloc(NLINES*sizeof(int));
	//fill data
	for(int i = 0; i < NLINES; i++){
		char * tmp;
		fgets(buf,255,in);
		tmp = strtok(buf,",");
		for(int j = 0; j < NCARDS; j++){
			data[i].cards[j] = atof(tmp);
			tmp = strtok(NULL,",");
		}
		clas[i]=atoi(tmp);
	}
	//randomly fill mu
	time_t t;
	srand((unsigned)time(&t));
	for(int i = 0; i < NCLUSTERS; i++){
		int tmp = rand() % NLINES;
		for(int j = 0; j < NCARDS; j++){
			mu[i].cards[j] = data[tmp].cards[j];
		}
	}
	
	//---------Perform WTA----------
	for(int i = 0; i < ITERATIONS; i++){
		for(int j=0; j<NLINES;j++){
			update_mu(&data[j],mu,NCLUSTERS);
		}
	}
	
	//-----Deterimine Accuracy-----
	int *clus = malloc(NLINES*sizeof(int));
	cluster(data,mu,NLINES,NCLUSTERS,clus);
	hand *avgclas = calloc(NCLASSES,sizeof(hand));
	hand *avgclus = calloc(NCLUSTERS,sizeof(hand));
	avg(avgclas, data, clas, NLINES, NCLASSES);
	avg(avgclus, data, clus, NLINES, NCLUSTERS);
	printf("Avg Clusters:\n");
	for(int i = 0; i < NCLUSTERS; i++){
		for(int j = 0; j < NCARDS; j++){
			printf("%lf ",avgclus[i].cards[j]);
		}
		printf("\n");
	}
	printf("\nAvg Classes:\n");
	for(int i = 0; i < NCLASSES; i++){
		for(int j = 0; j < NCARDS; j++){
			printf("%lf ",avgclas[i].cards[j]);
		}
		printf("\n");
	}
	double acc;
	acc = accuracy(NLINES,NCLUSTERS,NCLASSES,clus,clas,avgclus,avgclas);
	printf("\nOverall Accuracy is %lf\n\n",acc);	
	//---------Cleanup----------
	free(data);
	free(mu);
	free(clas);
	free(clus);
	fclose(in);
}
