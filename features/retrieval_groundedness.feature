@eval.groundedness @stage.staging @trigger.nightly @slice.faq_top200
Feature: RAG groundedness on top queries
  Scenario Outline: Answer is supported by retrieved context
    Given a user asks "<question>"
    When the assistant answers
    Then the answer should be grounded in the provided context
      And groundedness score should be >= 0.85

    Examples:
      | question                               |
      | How do I reset my enterprise password? |
      | What is the refund policy for partners? |
