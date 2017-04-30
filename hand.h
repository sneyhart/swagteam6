/*
 *
 *
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
#endif
