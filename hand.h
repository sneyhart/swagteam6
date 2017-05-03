/*
 * kmeans.c
 * Sam Neyhart
 * This contains the kmeans program used in the final project of 
 * ECE 471.
 */

#ifndef _hand
#define _hand
typedef struct{
	double cards[10];
}hand;

hand scale(hand *h1, double s);
double dist(hand *h1, hand *h2);
hand vdiff(hand *h1, hand *h2);
void update_mu(hand *h1, hand *mu, int nc);
int closest(hand *h1, hand *mu, int nc);
void cluster(hand *data, hand *mu, int nl, int nc, int *cluster);
void avg(hand *avgc, hand *data, int *c, int nl, int nc);
double accuracy(int NLINES, int nclu, int nc, int *clus, int *clas, hand *avgclus, hand *avgclas);
int clus_equal(int *c1, int *c2,int NLINES);
#endif
