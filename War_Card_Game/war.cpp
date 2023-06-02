#include <iostream>
#include <map>
#include "deck.h"

using namespace std;

int main() {

    Deck totalDeck;
    Deck humanPlayer;
    Deck computerPlayer;

    totalDeck.shuffleDeck();

    // deal cards from total 52 card deck
    while (totalDeck.cardsInDeck() > 0) {

        Card* cardOne = totalDeck.drawCard();
        Card* cardTwo = totalDeck.drawCard();

        humanPlayer.pointerStack.push(cardOne);
        computerPlayer.pointerStack.push(cardTwo);
    }

    // continue while both players have at least one card in their hand 
    while (humanPlayer.cardsInDeck() > 0 && computerPlayer.cardsInDeck() > 0) {

        Card* humanCard = humanPlayer.drawCard();
        Card* computerCard = computerPlayer.drawCard();

        int standardCompare = humanCard->compareValue(*computerCard);

        // human card has greater value than computer card  
        if (standardCompare == 1) {

            std::cout << "\nCards were: \n\n";

            std::cout << "(Human) ";
            humanCard->print();

            std::cout << "(Computer) ";
            computerCard->print();


            std::cout << "\nHuman had the high card!\n\n";

            // add both cards to human hand 
            humanPlayer.pointerStack.push(humanCard);
            humanPlayer.pointerStack.push(computerCard);
        }

        // computer card has greater value than human card  
        else if (standardCompare == -1) {
            std::cout << "\nCards were: \n\n";

            std::cout << "(Human) ";
            humanCard->print();

            std::cout << "(Computer) ";
            computerCard->print();


            std::cout << "\nComputer had the high card!\n\n";

            // add both cards to computer hand 
            computerPlayer.pointerStack.push(humanCard);
            computerPlayer.pointerStack.push(computerCard);
        }

        // human and computer cards are same rank 
        else if (standardCompare == 0) {

            std::cout << "\nWar!\n\n";
            vector<Card*> cardsOnTable;

            cardsOnTable.push_back(humanCard);
            cardsOnTable.push_back(computerCard);

            bool inWar = true;

            while (inWar) {

                if (humanPlayer.cardsInDeck() > 3 && computerPlayer.cardsInDeck() > 3) {

                    // draw one card per player and put onto the table face down
                    cardsOnTable.push_back(humanPlayer.drawCard());
                    cardsOnTable.push_back(computerPlayer.drawCard());
                    

                    // flip up third card for both players 
                    Card* humanWarCard = humanPlayer.drawCard();
                    Card* computerWarCard = computerPlayer.drawCard();

                    int warCompare = humanWarCard->compareValue(*computerWarCard);

                    // 
                    cardsOnTable.push_back(humanWarCard);
                    cardsOnTable.push_back(computerWarCard);

                    std::cout << "\n(Human war): ";
                    humanWarCard->print();

                    std::cout << "\n(Computer war): ";
                    computerWarCard->print();


                    std::cout << "\nCards on table: " << cardsOnTable.size() << endl;

                    // human war card has greater value than computer card  
                    if (warCompare == 1) {

                        std::cout << "\nHuman Wins War!\n";

                        // add all war cards to human deck 
                        for (unsigned int i = 0; i < cardsOnTable.size(); i++) {
                            humanPlayer.pointerStack.push(cardsOnTable[i]);
                        }
                        inWar = false;
                    }

                    // human card has greater value than computer card  
                    else if (warCompare == -1) {

                        std::cout << "\nComputer Wins War!\n";

                        // add all war cards to computer deck 
                        for (unsigned int i = 0; i < cardsOnTable.size(); i++) {
                            computerPlayer.pointerStack.push(cardsOnTable[i]);
                        }
                        inWar = false;
                    }

                }
                // Since each iteration of war requires 3 cards, 
                else if (humanPlayer.cardsInDeck() <= 3) {
                    for (unsigned int i = 0; i < humanPlayer.cardsInDeck(); i++) {
                        humanPlayer.drawCard();

                    }
                    inWar = false;
                }
                else if (computerPlayer.cardsInDeck() <= 3) {
                    for (unsigned int i = 0; i < computerPlayer.cardsInDeck(); i++) {
                        computerPlayer.drawCard();
                    }
                    inWar = false;
                }

            }

        }
    }

    if (humanPlayer.cardsInDeck() == 0) {
        std::cout << "\nHuman Wins the Game!" << endl;
    }
    else if (computerPlayer.cardsInDeck() == 0) {
        std::cout << "\nComputer Wins the Game!" << endl;
    }
    else {
        std::cout << "\nDraw game" << endl;
    }

    return 0;

}
