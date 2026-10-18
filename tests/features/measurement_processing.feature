Feature: Measurement Processing

  Scenario: Complete measurement lifecycle

    Given a valid measurement payload

    When a measurement is submitted

    Then the measurement status is processing

    When processing finishes

    Then the measurement status should be completed

    And hydration results should be available