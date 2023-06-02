#ifndef DECK_H
#define DECK_H

#include <iostream>
#include <string>
#include <vector>
#include <ctime>       
#include <random>
#include <algorithm>
#include <stack>
#include "card.h"

using namespace std;

class Deck
{
public:

	Deck();	

	~Deck();	

	void shuffleDeck();

	Card* drawCard();	

	int cardsInDeck();

	vector<Card*> deckVector;

	stack <Card*> pointerStack;
};
#endif

