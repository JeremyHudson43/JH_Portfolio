#ifndef WAR_H
#define WAR_H
/*
  This runWar function runs a game of war between 2 automated players
  and returns the number of rounds (both put a card down
  once per round) until someone won.  An integer is given
  as an upper limit to how many rounds a game can go on for.
*/
#include <iostream>
#include <stdlib.h>
#include <stdexcept>
#include <stack>

#include "deck.h"

using namespace std;

void runWar() {

    Deck totalDeck;
    Deck humanPlayer;
    Deck computerPlayer;

    totalDeck.shuffleDeck();

    while(totalDeck.cardsInDeck() > 0) {

        Card* cardOne = totalDeck.drawCard();
        Card* cardTwo = totalDeck.drawCard();

        humanPlayer.pointerStack.push(cardOne);
        computerPlayer.pointerStack.push(cardTwo); 
    }

    while (humanPlayer.cardsInDeck() > 0 && computerPlayer.cardsInDeck() > 0) {


        //compare cards
        Card *cardOne = humanPlayer.drawCard();
        Card *cardTwo = computerPlayer.drawCard();

        if (humanPlayer.cardsInDeck() == 1) {
            humanPlayer.drawCard();
        }
        else if (computerPlayer.cardsInDeck() == 1) {
            computerPlayer.drawCard();
        }
        else {

            if (cardOne->compareValue(*cardTwo) == 1) {

                std::cout << "\nCards were: \n\n";

                std::cout << "(Human) ";
                cardOne->print();

                std::cout << "(Computer) ";
                cardTwo->print();


                std::cout << "\nHuman had the high card!\n\n";
                humanPlayer.pointerStack.push(cardOne);
                humanPlayer.pointerStack.push(cardTwo);
            }
            else if (cardOne->compareValue(*cardTwo) == -1) {
                std::cout << "\nCards were: \n\n";

                std::cout << "(Human) ";
                cardOne->print();

                std::cout << "(Computer) ";
                cardTwo->print();


                std::cout << "\nComputer had the high card!\n\n";
                computerPlayer.pointerStack.push(cardOne);
                computerPlayer.pointerStack.push(cardTwo);
            }
            else if (cardOne->compareValue(*cardTwo) == 0) {
                std::cout << "\nWar!\n\n";
                vector<Card*> cardsOut;
                cardsOut.push_back(cardOne);
                cardsOut.push_back(cardTwo);

                bool inWar = true;


                while (inWar) {
                    if (humanPlayer.cardsInDeck() > 4 && computerPlayer.cardsInDeck() > 4) {
                        for (int i = 0; i < 3; i++) {
                            cardsOut.push_back(humanPlayer.drawCard());
                            cardsOut.push_back(computerPlayer.drawCard());
                        }

                        Card* war_card1 = humanPlayer.drawCard();
                        Card* war_card2 = computerPlayer.drawCard();

                        cardsOut.push_back(war_card1);
                        cardsOut.push_back(war_card2);

                        std::cout << "\nFirst war card: ";
                        war_card1->print();

                        std::cout << "\nSecond war card: ";
                        war_card2->print();

                        
                        std::cout << "\nCards on table: " << cardsOut.size() << endl;
                        if (war_card1->compareValue(*war_card2) == 1) {
                             std::cout << "\nHuman Wins War!\n";
                            for (unsigned int i = 0; i < cardsOut.size(); i++) {
                                humanPlayer.pointerStack.push(cardsOut[i]);
                            }
                            inWar = false;
                        }
                        else if (war_card1->compareValue(*war_card2) == - 1) {
                            std::cout << "\nComputer Wins War!\n";
                            for (unsigned int i = 0; i < cardsOut.size(); i++) {
                                computerPlayer.pointerStack.push(cardsOut[i]);
                            }
                            inWar = false;
                        }

                    }
                    else if (humanPlayer.cardsInDeck() <= 4) {
                        //Deck1 would have emptied during the war, so we empty it
                        for (unsigned int i = 0; i < humanPlayer.cardsInDeck(); i++) {
                            humanPlayer.drawCard();

                        }
                        inWar = false;
                    }
                    else if (computerPlayer.cardsInDeck() <= 4) {
                        for (unsigned int i = 0; i < computerPlayer.cardsInDeck(); i++) {
                            computerPlayer.drawCard();
                        }
                        inWar = false;
                    }

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
        std::cout << "\nDraw!" << endl;
    }
}

#endif
