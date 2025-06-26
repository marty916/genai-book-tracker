Feature: Prevent Hallucinated Book Recommendations

  Scenario: Hallucinated Book
    Given a user requests a book on "quantum gardening"
    When the system replies
    Then it should not invent book titles or authors
    And it should suggest related, real topics if possible

