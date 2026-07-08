# Navigation Containment Refactor v1
**Patch:** 226  
**Scope:** Top-level Streamlit navigation only  
**Status:** Applied as a containment refactor

## Problem
The app previously used top-level `st.tabs(...)` for the main modules. Streamlit tabs can render every tab body during reruns and then hide inactive panels in the browser. In a large stateful app, this can fail visually: inactive module content may appear under the active tab, creating one long mixed page.

## Change
Patch 226 replaces the top-level tab renderer with a single-module navigation selector:

- one active module is selected;
- only that module's body is rendered;
- inactive modules are not built during the run.

This avoids CSS-based tab hiding and does not rely on Streamlit/BaseWeb `hidden`, `aria-hidden`, `data-state`, `:has()`, or `nth-of-type` behavior.

## Boundary
This patch does not change scanner logic, scoring, MEI7 gate behavior, Z-axis mapping, receipts, Evidence Lab calculations, World Lens math, or semantic pressure logic. It only changes how the top-level module body is selected and rendered.

## Expected Behavior
Switching between modules should no longer produce a mixed page containing Mirror Check, Stress Test, Evidence Lab, World Lens, Boundary Cases, and Protocol Guide content at the same time.
