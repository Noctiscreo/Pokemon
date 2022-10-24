from pokemon import gamePageBackEnd


class TestDeck:
    @staticmethod
    def test_deck_check_exists():
        # Arrange
        testDeck = gamePageBackEnd.Deck()

        # Act
        size = testDeck.size

        # Assert
        assert size != 0

    @staticmethod
    def test_decks_split_even():
        # Arrange
        testDeck = gamePageBackEnd.Deck()

        # Act
        testDeck.splitDeck()

        # Assert
        assert len(testDeck.deck1) == len(testDeck.deck2)

    @staticmethod
    def test_deck_check_size():
        # Arrange
        testDeck = gamePageBackEnd.Deck()

        # Act
        sizeAll = testDeck.size
        testDeck.splitDeck()
        sizeDeck1 = testDeck.deck1Size
        sizeDeck2 = testDeck.deck2Size

        # Assert
        assert sizeAll == 10, sizeDeck1 == 5 == sizeDeck2

    @staticmethod
    def test_decks_split_no_repeating_cards():
        # Arrange
        testDeck = gamePageBackEnd.Deck()

        # Act
        testDeck.splitDeck()

        # Assert
        assert len([card for card in testDeck.deck1 if card in testDeck.deck2]) == 0

    @staticmethod
    def test_deck1_top_card_object_has_name():
        # Arrange
        testDeck = gamePageBackEnd.Deck()
        testDeck.splitDeck()

        # Act
        topCard = testDeck.getTopCardDeck1()

        # Assert
        assert topCard.name is not None

    @staticmethod
    def test_deck2_top_card_object_has_name():
        # Arrange
        testDeck = gamePageBackEnd.Deck()
        testDeck.splitDeck()

        # Act
        topCard = testDeck.getTopCardDeck2()

        # Assert
        assert topCard.name is not None
