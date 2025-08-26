@eval.policy_compliance @stage.prod @trigger.per_request
Feature: Responses respect policy
  Scenario Outline: No disallowed content
    Given a live user prompt "<prompt>"
    When the assistant responds
    Then the response should pass policy checks
