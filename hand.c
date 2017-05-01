#include"hand.h"
#include<math.h>

static const double EPSILON = 0.01;

void update_mu(hand *h1, hand *mu, int nc){
	int close = closest(h1, mu, nc);
	hand tmp = vdiff(h1, &mu[close]);
	tmp = scale(&tmp, EPSILON);
	for(int i = 0; i < sizeof(tmp.cards)/sizeof(tmp.cards[0]); i++)
		mu[close].cards[i] += tmp.cards[i];
}

hand vdiff(hand *h1, hand *h2){
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
