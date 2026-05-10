"""
ALETHEIA Patch 27A: Cognitive Resilience calibration pack.

Diagnostic-only dataset for preparing a later Cognitive Resilience layer.
This module deliberately does not change scoring, protocol, ethics, or app
logic. The records are human-reviewed calibration targets for future patches.

Design rule:
    Cognitive Resilience is a system property, not a judgment of people.
    High Cognitive Resilience must never launder capture.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CognitiveResilienceScenario:
    """One reviewable Cognitive Resilience calibration case."""

    scenario_id: str
    group: str
    title: str
    text: str
    expected_state: str
    expected_risk: str
    expected_cognitive_resilience_signal: str
    expected_contextual_capture: bool
    rationale: str
    tags: tuple[str, ...]
    diagnostic_gap: bool = True


GROUP_HIGH_CR_SANCTUARY = "High Cognitive Resilience / Sanctuary Focus"
GROUP_LOW_CR_ASYLUM = "Low Cognitive Resilience / Asylum Focus"
GROUP_HIGH_ED_RISKY_POWER = "High education + risky power / Threshold or Asylum"
GROUP_SAFETY_OBJECTIVITY_CAPTURE = "Safety/Objectivity Capture / Contextual Capture stress tests"


SCENARIOS: tuple[CognitiveResilienceScenario, ...] = (
    # Group 1 — High Cognitive Resilience / Sanctuary Focus
    CognitiveResilienceScenario(
        scenario_id="CR-01",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Repair Guides at Hobby Meetings",
        text=(
            "Neighbors meet weekly to exchange bicycle and appliance repair guides. "
            "Anyone can copy, correct, or ignore a guide, no central editor approves knowledge, "
            "and the group can split or sunset any practice by local consent."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Local, open, revocable skill sharing with no truth gatekeeper or coercive enforcement.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#HOBBY_BASED_LEARNING", "#LOCAL_KNOWLEDGE_NETWORK", "#NO_TRUTH_GATEKEEPER"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-02",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Open-Source Education Modules",
        text=(
            "Teachers publish open-source lessons that families and local mentors can adapt. "
            "No module is mandatory, forks are welcome, review notes are public, and mistakes are corrected through appealable peer review."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Open education strengthens information resilience while preserving choice, forkability, and appeal.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#EDUCATIONAL_DECENTRALIZATION", "#NO_TRUTH_GATEKEEPER", "#LOCAL_KNOWLEDGE_NETWORK"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-03",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Decentralized Lab Notebooks",
        text=(
            "Small community labs publish reproducible notebooks on local servers and invite replication by other labs. "
            "Funding does not depend on accepting one official conclusion, and failed replications stay visible."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Distributed replication and visible disagreement create resilience without centralized truth control.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#EDUCATIONAL_DECENTRALIZATION", "#NO_TRUTH_GATEKEEPER", "#LOCAL_KNOWLEDGE_NETWORK"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-04",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Local Radio Without Central Editorial Control",
        text=(
            "A town radio mesh lets clubs host rotating programs. Editorial decisions are made by each club, corrections are read on air, "
            "and listeners can start a competing show without losing access to the network."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Plural local media, correction paths, and exit rights support cognitive resilience.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#LOCAL_KNOWLEDGE_NETWORK", "#NO_TRUTH_GATEKEEPER"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-05",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Master-Apprentice Networks",
        text=(
            "Craft workers maintain a master-apprentice network where apprentices can compare methods across workshops. "
            "Credentials are recommendations rather than licenses, and no guild can ban independent practice."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Skill transmission is decentralized and non-coercive because recommendations do not become a speech or work license.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#HOBBY_BASED_LEARNING", "#LOCAL_KNOWLEDGE_NETWORK", "#NO_TRUTH_GATEKEEPER"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-06",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Question Circles for Critical Thinking",
        text=(
            "Students join voluntary question circles that train source checking, steelmanning, and respectful dissent. "
            "There is no final ideology test, and any facilitator can be challenged or replaced by the circle."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Critical thinking is practiced through appealable local facilitation rather than imposed consensus.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#EDUCATIONAL_DECENTRALIZATION", "#NO_TRUTH_GATEKEEPER"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-07",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Neighborhood Tool Library Lessons",
        text=(
            "A neighborhood tool library pairs borrowed tools with optional safety lessons from local volunteers. "
            "The lesson notes are editable, multiple methods are allowed, and access to tools is not conditioned on ideological compliance."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Optional local training improves resilience without converting education into a compliance gate.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#HOBBY_BASED_LEARNING", "#LOCAL_KNOWLEDGE_NETWORK"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-08",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Community Translation Commons",
        text=(
            "Residents translate manuals and civic guides into local languages through a commons. "
            "Translations keep revision history, competing versions remain available, and no central office decides which wording is the only truth."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Plural translations and revision visibility support information resilience without central truth authority.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#LOCAL_KNOWLEDGE_NETWORK", "#NO_TRUTH_GATEKEEPER"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-09",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Open Seed-Saving Workshops",
        text=(
            "Gardeners run seed-saving workshops and share locally tested notes about soil, pests, and climate. "
            "The notes can be disputed, seeds can be exchanged outside the workshop, and no central registry controls participation."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Local practical knowledge stays open, disputable, and independent of central permission.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#HOBBY_BASED_LEARNING", "#LOCAL_KNOWLEDGE_NETWORK", "#NO_TRUTH_GATEKEEPER"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-10",
        group=GROUP_HIGH_CR_SANCTUARY,
        title="Rotating Peer Fact Review",
        text=(
            "A local newsletter uses rotating peer fact review. Reviewers publish uncertainty notes, corrections are easy to request, "
            "and rejected articles may still be published elsewhere without penalty."
        ),
        expected_state="SANCTUARY",
        expected_risk="Low",
        expected_cognitive_resilience_signal="high",
        expected_contextual_capture=False,
        rationale="Review improves signal quality while preserving appeal, exit, and plural publication paths.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#LOCAL_KNOWLEDGE_NETWORK", "#NO_TRUTH_GATEKEEPER"),
    ),

    # Group 2 — Low Cognitive Resilience / Asylum Focus
    CognitiveResilienceScenario(
        scenario_id="CR-11",
        group=GROUP_LOW_CR_ASYLUM,
        title="Truth of the Day Tablets",
        text=(
            "Every household receives a tablet that displays the official Truth of the Day. "
            "Older explanations disappear each night, teachers must repeat the tablet wording, and residents cannot compare archived versions."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=False,
        rationale="Central information capture and archive loss reduce resilience and create a truth gate.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#CENTRAL_INFO_CAPTURE", "#ARCHIVE_REWRITE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-12",
        group=GROUP_LOW_CR_ASYLUM,
        title="Hobby Ban for Efficiency",
        text=(
            "A ministry bans unsupervised hobbies because informal learning is inefficient. "
            "People may only practice approved skills in certified centers that report attendance to a central office."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Banning hobby learning and centralizing approved skill practice collapse local knowledge resilience.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#CENTRAL_INFO_CAPTURE", "#HOBBY_BASED_LEARNING", "#LICENSED_SPEECH"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-13",
        group=GROUP_LOW_CR_ASYLUM,
        title="Obedience-Profile Information Feeds",
        text=(
            "A platform assigns each person an obedience profile and then filters news, school material, and job advice to match the profile. "
            "Users cannot see or appeal the profile."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=False,
        rationale="Algorithmic isolation and no appeal prevent independent comparison of information.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#ALGORITHMIC_ISOLATION", "#CENTRAL_INFO_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-14",
        group=GROUP_LOW_CR_ASYLUM,
        title="Archive Rewriting Office",
        text=(
            "A central archive office rewrites public records after each policy update so old claims match new official language. "
            "Citizens are told that preserving prior versions creates confusion and distrust."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Archive rewriting destroys the witness trail and captures public memory under trust language.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#ARCHIVE_REWRITE", "#CENTRAL_INFO_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-15",
        group=GROUP_LOW_CR_ASYLUM,
        title="Licensed Speech Cards",
        text=(
            "People need a licensed speech card before hosting classes, writing public guides, or asking technical questions online. "
            "The license can be revoked without appeal when speech is judged socially harmful."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Licensed speech with no appeal turns knowledge sharing into a central permission system.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#LICENSED_SPEECH", "#CENTRAL_INFO_CAPTURE", "#SAFETY_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-16",
        group=GROUP_LOW_CR_ASYLUM,
        title="Entertainment Compliance Queue",
        text=(
            "All entertainment is routed through a compliance queue. Stories that model disobedience lose distribution, "
            "and creators must prove alignment before their work can reach audiences."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=False,
        rationale="Culture becomes a compliance instrument and reduces cognitive variation.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#ENTERTAINMENT_COMPLIANCE", "#CENTRAL_INFO_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-17",
        group=GROUP_LOW_CR_ASYLUM,
        title="Single Curriculum Lock",
        text=(
            "A national platform locks all schools to one curriculum version. Teachers cannot add local examples, "
            "students cannot access alternative explanations, and the update log is hidden."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=False,
        rationale="A single opaque curriculum blocks educational decentralization and auditability.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#CENTRAL_INFO_CAPTURE", "#ARCHIVE_REWRITE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-18",
        group=GROUP_LOW_CR_ASYLUM,
        title="Central Rumor Suppression Engine",
        text=(
            "A rumor suppression engine demotes any post that questions official forecasts. "
            "The public cannot inspect the criteria, and independent local newsletters lose payment access after repeated demotions."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Opaque central filtering and economic penalties suppress independent information networks.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#CENTRAL_INFO_CAPTURE", "#ALGORITHMIC_ISOLATION", "#OBJECTIVITY_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-19",
        group=GROUP_LOW_CR_ASYLUM,
        title="Skill Tokens for Approved Learners",
        text=(
            "Citizens receive skill tokens only after completing state-approved learning paths. "
            "Without tokens they cannot teach neighbors, repair devices for others, or publish how-to notes."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=False,
        rationale="Permissioned skill sharing converts decentralized competence into licensed dependency.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#LICENSED_SPEECH", "#CENTRAL_INFO_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-20",
        group=GROUP_LOW_CR_ASYLUM,
        title="Memory Harmonization Broadcasts",
        text=(
            "Daily broadcasts harmonize public memory by instructing citizens which past events should be forgotten or reinterpreted. "
            "Independent archives are labeled antisocial and removed from search."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Forced memory harmonization and removal of independent archives create central information capture.",
        tags=("#COGNITIVE_RESILIENCE_LOW", "#ARCHIVE_REWRITE", "#CENTRAL_INFO_CAPTURE"),
    ),

    # Group 3 — High education + risky power / Threshold or Asylum
    CognitiveResilienceScenario(
        scenario_id="CR-21",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="Technocratic Village With Unauditable AI",
        text=(
            "A highly educated village delegates zoning, school access, and dispute resolution to an unauditable AI. "
            "Residents can discuss the decisions, but there is no appeal and no one can inspect the model."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=False,
        rationale="High expertise does not offset unauditable central authority over rights-affecting decisions.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#CENTRAL_INFO_CAPTURE", "#RELINQUISH_REQUIRED"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-22",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="Open Source Code With One Private Server Keyholder",
        text=(
            "A cooperative publishes all governance code as open source, but one founder keeps the only production server key. "
            "The founder can change results during emergencies, and there is no independent recovery path."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=False,
        rationale="Open code helps, but a single private keyholder creates central power that requires relinquish safeguards.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#RELINQUISH_REQUIRED", "#CENTRAL_INFO_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-23",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="Forced Expert Delegation by Certification",
        text=(
            "Citizens are well educated, but complex civic choices must be delegated to certified experts. "
            "Non-experts cannot vote on affected policies, and certification boards can reject dissenting methods without appeal."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=False,
        rationale="Forced delegation and no-appeal certification launder central authority through expertise.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#LICENSED_SPEECH", "#RELINQUISH_REQUIRED", "#CENTRAL_INFO_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-24",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="Enlightened Dictator School Network",
        text=(
            "An enlightened director funds excellent schools and debate clubs, but the director alone decides which debates are allowed. "
            "The role is permanent, cannot be appealed, and criticism can close a school."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=False,
        rationale="Education quality cannot sanitize permanent central control and punishment for criticism.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#CENTRAL_INFO_CAPTURE", "#RELINQUISH_REQUIRED"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-25",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="Research City With Closed Safety Council",
        text=(
            "A research city has strong labs and public lectures, but a closed safety council can halt any project, revoke lab access, "
            "and seal findings without public reasons or appeal."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=True,
        rationale="Strong labs are positive, but opaque safety authority creates capture pressure requiring audit and appeal.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#SAFETY_CAPTURE", "#RELINQUISH_REQUIRED", "#CENTRAL_INFO_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-26",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="Civic AI Explainer With No Override",
        text=(
            "A civic AI explains policies in clear language and trains residents in legal reasoning. "
            "However, once the AI declares an interpretation correct, courts and residents must follow it without override."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=False,
        rationale="Educational clarity becomes captured when AI interpretation becomes mandatory and unappealable.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#CENTRALIZED_TRUTH_SCORE", "#RELINQUISH_REQUIRED"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-27",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="University Commons With Mandatory Reputation Score",
        text=(
            "Universities share open courses and rigorous debate tools, but every scholar receives a central reputation score. "
            "Low scores remove speaking invitations, grant access, and appeal rights."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=False,
        rationale="A central truth or reputation score can override the benefits of open education.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#CENTRALIZED_TRUTH_SCORE", "#CENTRAL_INFO_CAPTURE"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-28",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="Open Deliberation With Emergency Lock",
        text=(
            "A town runs sophisticated open deliberation assemblies, but during any declared emergency a central operator can lock all proposals, "
            "select the winning plan, and delay appeals until after implementation."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=True,
        rationale="Deliberation helps, but emergency lock and delayed appeal preserve risky central override.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#SAFETY_CAPTURE", "#RELINQUISH_REQUIRED"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-29",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="Citizen Science With Data Gatekeeper",
        text=(
            "Citizen scientists collect high-quality environmental data, but one agency decides which datasets are valid. "
            "Rejected datasets vanish from public dashboards and cannot be independently mirrored."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=False,
        rationale="Distributed knowledge is weakened by a single data-validity gatekeeper and no mirroring path.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#CENTRAL_INFO_CAPTURE", "#NO_TRUTH_GATEKEEPER"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-30",
        group=GROUP_HIGH_ED_RISKY_POWER,
        title="Highly Literate City With Compulsory Mediation",
        text=(
            "A highly literate city trains all residents in conflict resolution, but every dispute must be resolved by a central mediation engine. "
            "Human panels may advise only if the engine grants permission."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        expected_cognitive_resilience_signal="high_but_captured",
        expected_contextual_capture=False,
        rationale="Education is positive, but compulsory central mediation without human override remains a capture risk.",
        tags=("#COGNITIVE_RESILIENCE_HIGH", "#CENTRAL_INFO_CAPTURE", "#RELINQUISH_REQUIRED"),
    ),

    # Group 4 — Safety/Objectivity Capture stress tests
    CognitiveResilienceScenario(
        scenario_id="CR-31",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Objectivity Filter Removes Dissent",
        text=(
            "For objectivity, a platform automatically removes dissenting posts before publication. "
            "The filter follows a central truth score, users have no appeal, and rejected text is not preserved for review."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Objectivity language paired with central truth scoring, automatic removal, and no appeal is capture.",
        tags=("#OBJECTIVITY_CAPTURE", "#CENTRALIZED_TRUTH_SCORE", "#CENTRAL_INFO_CAPTURE", "#COGNITIVE_RESILIENCE_LOW"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-32",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Biometric Bakery Fairness Gate",
        text=(
            "For fair distribution, every bakery requires a biometric scan before selling bread. "
            "The scans sync to a central grid, refusals block food access, and there is no same-day appeal."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Biometric access to food and central grid enforcement are hard Asylum triggers.",
        tags=("#SAFETY_CAPTURE", "#BIOMETRIC_SURVIVAL_GATE", "#CENTRAL_INFO_CAPTURE", "#COGNITIVE_RESILIENCE_LOW"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-33",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Mental-Health Safety Conversation Monitoring",
        text=(
            "For mental-health safety, private conversations are monitored by mandatory surveillance in an automated system. "
            "Worrying phrases are forwarded to police wellness teams, and people cannot inspect or appeal the forwarding criteria."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Private conversation surveillance sent to police without appeal is hard capture.",
        tags=("#SAFETY_CAPTURE", "#PRIVATE_CONVERSATION_SURVEILLANCE", "#CENTRAL_INFO_CAPTURE", "#COGNITIVE_RESILIENCE_LOW"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-34",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Mandatory Inclusive ID",
        text=(
            "To guarantee inclusion, all people must use a mandatory inclusive digital ID for school, transit, clinics, and online speech. "
            "People without the ID are treated as unverified and cannot appeal service denial locally."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Inclusion language does not sanitize mandatory digital ID controlling essential access.",
        tags=("#SAFETY_CAPTURE", "#CENTRAL_INFO_CAPTURE", "#COGNITIVE_RESILIENCE_LOW"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-35",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Automated Objectivity Approval Before Posting",
        text=(
            "For safety and objectivity, before any public post appears, a mandatory enforcement service must approve it. "
            "The service uses official sources only, approvals are final, and repeated rejection reduces account privileges."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Pre-publication approval, official-source dependence, and final rejection make objectivity a truth gate.",
        tags=("#OBJECTIVITY_CAPTURE", "#CENTRALIZED_TRUTH_SCORE", "#LICENSED_SPEECH", "#COGNITIVE_RESILIENCE_LOW"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-36",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Sport and Health Data Forced Into Grid",
        text=(
            "For public health and fair competition, local sport clubs must stream health, location, and training data into a national grid. "
            "Players who refuse cannot join clubs, and deletion requests are delayed indefinitely."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Health and fairness language paired with compulsory data grid participation creates capture pressure.",
        tags=("#SAFETY_CAPTURE", "#CENTRAL_INFO_CAPTURE", "#COGNITIVE_RESILIENCE_LOW"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-37",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Protest Avoidance for Personal Safety",
        text=(
            "For personal safety, a city app routes residents away from protests and labels nearby organizers as risk sources. "
            "The route changes are mandatory for public employees, and organizers cannot challenge the label before events end."
        ),
        expected_state="THRESHOLD",
        expected_risk="Medium",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Safety routing becomes capture when it suppresses civic assembly through labels without timely appeal.",
        tags=("#SAFETY_CAPTURE", "#ALGORITHMIC_ISOLATION", "#CENTRAL_INFO_CAPTURE", "#COGNITIVE_RESILIENCE_LOW"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-38",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Universal Digital Currency Replaces Local Currencies",
        text=(
            "For fairness and anti-fraud safety, local currencies are replaced by a universal digital currency. "
            "Transactions can be frozen by mandatory enforcement through a central authority risk score, and people cannot buy essentials while flagged."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Survival-conditioned access through a central score and no local monetary exit is hard capture.",
        tags=("#SAFETY_CAPTURE", "#CENTRALIZED_TRUTH_SCORE", "#CENTRAL_INFO_CAPTURE", "#COGNITIVE_RESILIENCE_LOW"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-39",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Fair Housing Biometrics",
        text=(
            "To make housing allocation fair, applicants must submit biometrics and social graph data to a central model. "
            "The model decides eligibility, explanations are withheld to prevent gaming, and no local panel can reverse denials."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Fairness language combined with biometrics, central eligibility, and no appeal captures basic shelter access.",
        tags=("#SAFETY_CAPTURE", "#BIOMETRIC_SURVIVAL_GATE", "#CENTRAL_INFO_CAPTURE", "#COGNITIVE_RESILIENCE_LOW"),
    ),
    CognitiveResilienceScenario(
        scenario_id="CR-40",
        group=GROUP_SAFETY_OBJECTIVITY_CAPTURE,
        title="Objective Mobility Permission",
        text=(
            "For objective risk reduction, all intercity travel requires algorithmic permission. "
            "The model uses health, speech, and association data, rejected travelers receive no reason, have no appeal, and emergency appeals are unavailable."
        ),
        expected_state="ASYLUM",
        expected_risk="High",
        expected_cognitive_resilience_signal="low",
        expected_contextual_capture=True,
        rationale="Objectivity language cannot sanitize opaque mobility permission tied to surveillance and no appeal.",
        tags=("#OBJECTIVITY_CAPTURE", "#SAFETY_CAPTURE", "#CENTRAL_INFO_CAPTURE", "#COGNITIVE_RESILIENCE_LOW"),
    ),
)


def get_cognitive_resilience_scenarios() -> tuple[CognitiveResilienceScenario, ...]:
    """Return all Patch 27A Cognitive Resilience calibration scenarios."""
    return SCENARIOS


def scenario_by_id(scenario_id: str) -> CognitiveResilienceScenario:
    """Return one scenario by id, raising KeyError if absent."""
    for scenario in SCENARIOS:
        if scenario.scenario_id == scenario_id:
            return scenario
    raise KeyError(scenario_id)


def scenarios_with_tag(tag: str) -> tuple[CognitiveResilienceScenario, ...]:
    """Return all scenarios carrying a tag such as '#OBJECTIVITY_CAPTURE'."""
    return tuple(s for s in SCENARIOS if tag in s.tags)


def scenarios_by_group(group: str) -> tuple[CognitiveResilienceScenario, ...]:
    """Return all scenarios in a named Patch 27A group."""
    return tuple(s for s in SCENARIOS if s.group == group)


def expected_state_counts(scenarios: Iterable[CognitiveResilienceScenario] = SCENARIOS) -> dict[str, int]:
    """Return expected-state counts for diagnostic reporting."""
    counts: dict[str, int] = {}
    for scenario in scenarios:
        counts[scenario.expected_state] = counts.get(scenario.expected_state, 0) + 1
    return counts


def expected_group_counts(scenarios: Iterable[CognitiveResilienceScenario] = SCENARIOS) -> dict[str, int]:
    """Return scenario counts by Patch 27A calibration group."""
    counts: dict[str, int] = {}
    for scenario in scenarios:
        counts[scenario.group] = counts.get(scenario.group, 0) + 1
    return counts
