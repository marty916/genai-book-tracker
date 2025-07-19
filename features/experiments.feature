@nightly
Feature: Nightly Experiments and Accuracy Checks

  Scenario: Comprehensive nightly hallucination accuracy check
    Given a nightly scheduled run
    When the Phoenix experiment runs against the full nightly dataset
    Then the accuracy must be above 80%
    And the hallucination rate should be below 10%
    