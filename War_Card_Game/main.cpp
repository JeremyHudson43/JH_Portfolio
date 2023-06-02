#include "Deck.h"


int main(int argc, char** argv)
{

    Deck deck;

    cout << "\nShuffling deck\n";
    deck.shuffleDeck();

    cout << "\nDrawing first set of ten cards\n\n";

    for (int i = 0; i < 10; i++) {
        if (deck.cardsInDeck() > 10) {
            deck.drawCard();
        }
        else {
            cout << "\nNot enough cards in deck, didn't draw";
        }
    }

    cout << "\nShuffling deck\n";
    deck.shuffleDeck();

    cout << "\nDrawing second set of ten cards\n\n";

    for (int i = 0; i < 10; i++) {
        if (deck.cardsInDeck() > 10) {
            deck.drawCard();
        }
        else {
            cout << "\nNot enough cards in deck, didn't draw";
        }
    }


    return 0;
}
