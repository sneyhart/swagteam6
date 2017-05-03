/*
 * hand.c
 * Sam Neyhart
 * This contains the hand struct and some related functions
 * used in the final project of ECE 471.
 */

#include"hand.h"
#include<math.h>
#include<stdio.h>

static const double EPSILON = 0.01;
static const double EPSILON_MAX = 0.05;

int clus_equal(int *c1, int *c2,int NLINES)
{
	for(int i=0; i<NLINES;i++){
		if(c1[i]!=c2[i]){
			return 0;
		}
	}
	return 1;
}

void avg(hand *avgc, hand *data, int *c, int nl, int nc)
{
	int count[nc];
	for(int i=0; i<nc; i++)
		count[i]=0;
	for(int i=0; i<nc; i++){
		for(int j=0; j<10; j++){
			avgc[i].cards[j] = 0;
		}
	}
	for(int i=0; i<nl; i++){
		count[c[i]]++;
		for(int j=0; j<10; j++){
			avgc[c[i]].cards[j]+= data[i].cards[j];
		}
	}
	for(int i=0; i<nc; i++){
		for(int j=0; j<10; j++){
			avgc[i].cards[j]/=count[i];
			if (count[i]==0)
				avgc[i].cards[j]=-1;
		}
	}
}

double accuracy(int NLINES, int nclu, int nc, int *clus, int *clas, hand *avgclus, hand *avgclas)
{
	int truec[nclu];
	int count = 0;
	printf("\n");
	for(int i=0; i<nclu; i++){
		truec[i] = closest(&avgclus[i], avgclas, nc);
		printf("Cluster %d is class %d\n",i,truec[i]);
	}
	for(int i=0; i<NLINES; i++){
		count+=(truec[clus[i]]==clas[i]);
	}
	return count/(float)NLINES;
}

void kohonen_mu(hand *h1, hand *mu, int NCLUSTERS, int k, int kmax)
{	
	int close = closest(h1, mu, NCLUSTERS);
	hand win = mu[close];
	for(int i=0; i<NCLUSTERS; i++){
		hand tmp = vdiff(h1,&mu[i]);
		double e = EPSILON_MAX * pow(EPSILON/EPSILON_MAX,k/(double)kmax);
		double d = exp(-1*dist(&win,&mu[i]));
		tmp = scale(&tmp,e*d);
		for(int j=0; j < sizeof(tmp.cards)/sizeof(tmp.cards[0]); j++){
			mu[i].cards[j]+=tmp.cards[j];
		}
	}
}

void update_mu(hand *h1, hand *mu, int nc)
{
	int close = closest(h1, mu, nc);
	hand tmp = vdiff(h1, &mu[close]);
	tmp = scale(&tmp, EPSILON);
	for(int i = 0; i < sizeof(tmp.cards)/sizeof(tmp.cards[0]); i++)
		mu[close].cards[i] += tmp.cards[i];
}

hand vdiff(hand *h1, hand *h2)
{
	hand out = *h1;
	for(int i = 0; i < sizeof(out.cards)/sizeof(out.cards[0]); i++)
		out.cards[i] = h1->cards[i] - h2->cards[i];
	return out;
}

hand scale(hand *h1, double s)
{
	hand out = *h1;
	for(int i = 0; i < sizeof(out.cards)/sizeof(out.cards[0]); i++)
		out.cards[i]*=s;
	return out;
}

double dist(hand *h1, hand *h2)
{
	double dist = 0;
	for(int i = 0; i<sizeof(h1->cards)/sizeof(h1->cards[0]); i++){
		dist += pow(fabs(h1->cards[i]-h2->cards[i]),2);
	}
	return sqrt(dist);
}

int closest(hand *h1, hand *mu, int NCLUSTERS)
{
	double small = -1;
	int closest = -1;
	for(int i = 0; i < NCLUSTERS; i++){
		int tmp = dist(h1, &(mu[i]));
		if(small == -1 || small > tmp){
			small = tmp;
			closest = i;
		}
	}
	return closest;
}

void cluster(hand *data, hand *mu, int nl, int nc, int *clus)
{
	for(int i=0; i<nl; i++){
		clus[i] = closest(&data[i],mu,nc);
	}
}
