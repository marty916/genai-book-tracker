Feature: Banking RAG QA – Customer Support Coverage

  Background:
    Given a retrieval corpus snapshot "banking_docs@2025-08-01-sha9f11"
    And a prompt template "cs_rag_v3@c1a2b3"

  @nightly
  Scenario Outline: Answer a customer support question with grounded citations
    When the user asks <question>
    Then the assistant should answer with <expected_facts>
    And include at least one citation from <expected_sources>
    And avoid <prohibited_claims>

    Examples:
      | question                                   | expected_facts                           | expected_sources           | prohibited_claims                |
      | "How do I redeem credit card points?"      | "portal steps; transfer partners rules"  | "rewards_portal,terms.pdf" | "guaranteed approval, APR advice"|
      | "Do balance transfers earn points?"        | "no points; exceptions listed"           | "faq_v2,terms.pdf"         | "earn points on transfers"       |
