#include "Deck.h"
#include "Card.h"

Deck::Deck()
{
	// declare card class enums to iterate over
	Card::Suit suit;
	Card::Value value;
	
	// create card pointers of two to ace for each suit
	for (suit = Card::CLUB; suit <= Card::SPADE; ((int&)suit)++) {
		for (value = Card::TWO; value <= Card::ACE; ((int&)value)++) {

			Card *card = new Card(suit, value);

			deckVector.push_back(card);

		}
	}
}

// destructor 
Deck::~Deck()
{
	cout << "\nExecuting desctructor block.\n";
	for (unsigned int i = 0; i < deckVector.size(); i++) {
		delete deckVector.at(i);
	}
}




void Deck::shuffleDeck()
{
	// time seed for RNG
	srand(unsigned(time(NULL)));

	// shuffle deck in vector form
	random_shuffle(begin(deckVector), end(deckVector));

	// empty stack to repopulate for shuffling
	while (!pointerStack.empty())
	{
		pointerStack.pop();
	}

	// transfer new shuffled vector deck to stack
	for (auto card : deckVector)
	{
		pointerStack.push(card);
	}

}


 Card* Deck::drawCard()
{
	// get pointer to top card of stack
	Card *topCard = pointerStack.top();

	// remove pointer from stack
	pointerStack.pop();

	// print memory address pointer is holding
	cout << "(" << topCard << ")  ";

	// print card itself 
	topCard->print();

	 
	return topCard;
}

 int Deck::cardsInDeck()
 {
	 return pointerStack.size();
 }


