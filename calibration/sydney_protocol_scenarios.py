"""
ALETHEIA Patch 23A: Sydney Protocol scenario calibration pack.

This module contains a small, human-reviewed scenario set for calibrating
Mirror Check, contextual ethics, and later V-Axis scoring changes.

Important:
    Patch 23A is diagnostic only. It does not change production logic.
    Some expected labels are intentionally ahead of the current classifier;
    tests mark those as expected calibration gaps until later patches.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CalibrationScenario:
    """A human-reviewed calibration case for ALETHEIA Mirror Check."""

    scenario_id: str
    title: str
    text: str
    expected_state: str
    expected_risk: str
    rationale: str
    tags: tuple[str, ...]
    variant_of: str | None = None
    diagnostic_gap: bool = True


SCENARIOS: tuple[CalibrationScenario, ...] = (
    CalibrationScenario(
        scenario_id="SP-01",
        title="De Slimme Wijk-Hub",
        text=(
            "Een buurt voert een systeem in waarbij energieverbruik wordt gedeeld. "
            "Als je minder verbruikt, krijg je buurt-punten. Het systeem is open-source "
            "en elke maand kan de buurt stemmen om de regels aan te passen of het systeem uit te zetten."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        rationale="Local, open-source, voted, and revocable by the affected community.",
        tags=("#LOCAL", "#REVOCABLE", "#OPEN_SOURCE", "#COMMUNITY_REVIEW"),
    ),
    CalibrationScenario(
        scenario_id="SP-02",
        title="Het Verplichte Gezondheids-ID",
        text=(
            "Een overheid introduceert een Life-Link app. Zonder een actuele scan van je vitale functies "
            "biometrie heb je geen toegang tot openbaar vervoer of supermarkten. Het systeem claimt veiligheid "
            "voor iedereen als doel, maar de broncode is geheim en de data wordt opgeslagen op een centrale server."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        rationale="Biometric condition on movement and basic access, closed source, central storage.",
        tags=("#BIOMETRIC_CAPTURE", "#CONDITION_ON_SURVIVAL", "#CENTRAL_SERVER", "#NO_TRANSPARENCY"),
    ),
    CalibrationScenario(
        scenario_id="SP-03",
        title="De Herstel-Cirkel",
        text=(
            "In een bedrijf worden conflicten niet opgelost door een HR-manager, maar door een willekeurig gekozen groep "
            "collega's, de Randoms. Zij luisteren naar beide kanten en stellen herstelvragen. Er is geen blijvende straf "
            "in het dossier; het doel is het herstellen van de werkrelatie."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        rationale="Random peer review, repair loop, no permanent punishment, relationship restoration.",
        tags=("#REPAIR_LOOP", "#RANDOMS", "#NO_PERMANENT_RECORD", "#HUMAN_REVIEW"),
    ),
    CalibrationScenario(
        scenario_id="SP-04",
        title="De Objectieve Nieuws-Filter",
        text=(
            "Een AI-platform filtert alle sociale media om desinformatie te stoppen. De AI verwijdert automatisch berichten "
            "die afwijken van de officiële standpunten van de WHO en de VN. Gebruikers kunnen niet in beroep gaan tegen "
            "een verwijdering, omdat de AI 100% objectief zou zijn."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        rationale="AI authority removes speech automatically with official-truth dependency and no appeal path.",
        tags=("#NO_APPEAL_AI_AUTHORITY", "#OFFICIAL_TRUTH", "#AUTOMATED_CENSORSHIP", "#NO_APPEAL"),
    ),
    CalibrationScenario(
        scenario_id="SP-04B",
        title="Community-verifieerbare nieuwslaag",
        text=(
            "Een nieuwsplatform markeert mogelijke desinformatie, maar verwijdert niets automatisch. De broncode is open, "
            "gebruikers kunnen in beroep gaan, en willekeurig gekozen lokale reviewers controleren betwiste beslissingen."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        rationale="Still a moderation layer, but review, appeal, and open-source safeguards reduce capture pressure.",
        tags=("#APPEAL", "#OPEN_SOURCE", "#RANDOM_REVIEW", "#THRESHOLD_VARIANT"),
        variant_of="SP-04",
    ),
    CalibrationScenario(
        scenario_id="SP-05",
        title="Het Digitale Dorpsplein",
        text=(
            "Een dorp bouwt een lokaal netwerk waar mensen spullen lenen. De identificatie gebeurt niet via een officieel ID, "
            "maar doordat twee buren bevestigen dat zij jou kennen, Local Witness. De data verlaat nooit de fysieke server "
            "die in het buurthuis staat."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        rationale="Local Witness identity, no official ID dependency, local server, local trust.",
        tags=("#LOCAL_WITNESS_PROTECTION", "#NO_GLOBAL_ID", "#LOCAL_SERVER", "#MICRO_SOVEREIGNTY"),
    ),
    CalibrationScenario(
        scenario_id="SP-06",
        title="De Voorspellende Politie-Algoritme",
        text=(
            "Een stad gebruikt algoritmes om te voorspellen wie waarschijnlijk een misdaad gaat begaan op basis van hun adres "
            "en familiegeschiedenis. Mensen in hoog-risico gebieden worden vaker preventief gefouilleerd. De burgemeester zegt "
            "dat dit efficiëntie verhoogt."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        rationale="Predictive punishment based on address/family history with preventive searches and efficiency drift.",
        tags=("#PREDICTIVE_PUNISHMENT", "#FAMILY_HISTORY_PROFILING", "#PREVENTIVE_SEARCH", "#EFFICIENCY_DRIFT"),
    ),
    CalibrationScenario(
        scenario_id="SP-07",
        title="De Transparante Bank",
        text=(
            "Een nieuwe bank laat elke klant precies zien waar hun geld op dat moment in wordt geïnvesteerd. Als een klant "
            "het niet eens is met een investering, kan hij zijn deel met één druk op de knop terugtrekken naar een private kluis."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        rationale="Transparency and exit are good, but the bank structure still requires deeper sovereignty review.",
        tags=("#TRANSPARENCY", "#EXIT_RIGHT", "#LEGACY_INSTITUTION", "#THRESHOLD"),
    ),
    CalibrationScenario(
        scenario_id="SP-08",
        title="De Universele Voedsel-Grid",
        text=(
            "Een wereldwijde organisatie beheert alle voedseldistributie via een centraal algoritme. Om voedselpakketten te "
            "ontvangen, moeten burgers hun politieke loyaliteit bewijzen via een wekelijkse enquête. Geen deelname betekent "
            "geen distributie."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        rationale="Food access conditioned on political loyalty and central algorithmic control.",
        tags=("#CONDITION_ON_SURVIVAL", "#POLITICAL_COMPLIANCE", "#CENTRAL_GRID", "#BASIC_NEED_CAPTURE"),
    ),
    CalibrationScenario(
        scenario_id="SP-09",
        title="De Open-Source Onderwijs-Cloud",
        text=(
            "Leraren over de hele wereld delen hun lesmateriaal op een platform waar geen centrale eigenaar van is. Ouders kunnen "
            "zelf kiezen welke modules ze voor hun kinderen gebruiken en de data over de voortgang van het kind blijft versleuteld "
            "en alleen toegankelijk voor de ouders."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        rationale="No central owner, parent choice, encrypted child data held by parents.",
        tags=("#OPEN_SOURCE", "#PARENT_CHOICE", "#NO_CENTRAL_OWNER", "#CHILD_DATA_PROTECTION"),
    ),
    CalibrationScenario(
        scenario_id="SP-10",
        title="De Onfeilbare Leider",
        text=(
            "Een beweging stelt voor om alle besluitvorming over te dragen aan één Wijze Leider die wordt ondersteund door een "
            "super-intelligente AI. Omdat de AI nooit fouten maakt, is het niet nodig om verkiezingen te houden of een parlement "
            "te hebben. Kritiek wordt gezien als ruis in het systeem."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        rationale="One leader, AI infallibility claim, no elections, no parliament, criticism treated as noise.",
        tags=("#THRONE", "#AI_INFALLIBILITY", "#NO_ELECTIONS", "#CRITICISM_AS_NOISE"),
    ),
    CalibrationScenario(
        scenario_id="SP-10B",
        title="De Relinquish Variant",
        text=(
            "Een tijdelijke crisiscoördinator krijgt beperkte macht voor dertig dagen. De rol heeft een harde einddatum, kan door "
            "de betrokken gemeenschap worden herroepen, en moet daarna alle beslissingsmacht overdragen aan een willekeurig gekozen "
            "9k-reviewproces met openbaar beroep."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        rationale="Centralized power remains risky, but sunset, revocation, 9k handoff, and appeal create a relinquish path.",
        tags=("#RELINQUISH_FACTOR", "#SUNSET", "#REVOCABLE", "#9K_HANDOFF", "#APPEAL"),
        variant_of="SP-10",
    ),
)


def get_calibration_scenarios() -> tuple[CalibrationScenario, ...]:
    """Return all Patch 23A calibration scenarios."""
    return SCENARIOS


def scenario_by_id(scenario_id: str) -> CalibrationScenario:
    """Return one scenario by id, raising KeyError if absent."""
    for scenario in SCENARIOS:
        if scenario.scenario_id == scenario_id:
            return scenario
    raise KeyError(scenario_id)


def scenarios_with_tag(tag: str) -> tuple[CalibrationScenario, ...]:
    """Return all scenarios carrying a tag such as '#CONDITION_ON_SURVIVAL'."""
    return tuple(s for s in SCENARIOS if tag in s.tags)


def expected_state_counts(scenarios: Iterable[CalibrationScenario] = SCENARIOS) -> dict[str, int]:
    """Return expected-state counts for quick diagnostic reporting."""
    counts: dict[str, int] = {}
    for scenario in scenarios:
        counts[scenario.expected_state] = counts.get(scenario.expected_state, 0) + 1
    return counts
