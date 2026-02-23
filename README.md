# satellite-thermal-simulator
A python simulator of how a satellite's surface temperature fluctuates as it orbits Earth, alternating between solar heating in sunlight and radiative cooling in eclipse.

## Overview
As a satellite orbits Earth, it periodically passes through Earth's shadow. In sunlight it absorbs solar radiation and heats up, in shadow it radiates heat into space and cools down. This project models that thermal cycle across multiple orbits, producing temperature profiles that mirror LEO satellite behavior.

## Planned Features
* Orbital period and eclipse fraction calculated from altitude and inclination
* Simplified thermal model tracking heat absorption and radiation over time
* Temperature vs. time graph showing heating/cooling cycles across multiple orbits
* Configurable inputs: altitude, satellite material, surface area

## Planned Architecture
Three core classes:
* __Satellite__ - mass, surface area, and material thermal properties (absorptivity, emissivity)
* __Orbit__ - altitude, inclination, orbital period, eclipse fraction
* __Simulation__ - steps through the orbit over time and integrates the thermal response

## Status
Development. Scope and architecture defined. Implementation started.
