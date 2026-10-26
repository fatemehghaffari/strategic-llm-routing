# SCOUT B5: secondary extensions and lower bounds (Agent B, round 2, 17 September 2026)

STATUS: IN PROGRESS. Sections are appended as they are finished; a section not present below has not been written. Nothing in this file has been reviewed by anyone else. Every statement carries one of the labels PROVED, PROVED UNDER STRONGER ASSUMPTIONS, INCOMPLETE, FALSE, OPEN, CONJECTURE; the final table in Section I collects them.

Sources read in full before writing: audit/round2/prompts/COMMON.md, audit/round2/B/CONTEXT_PROOF_CONTRACT.md, audit/round2/B/LEAD_PRELIMINARY_CLAIMS.md, and sections/setting.tex, Stochastic_SAMF_Conditions.tex, appendix_samf.tex, Private_information_setting.tex, appendix_private.tex, contextual.tex, contextual_samf_algorithm.tex, appendix_contextual.tex. Notation follows the proof contract: E_S expectation under profile S, 1{.} indicator, (x)_+ = max(x,0), log natural, [K] = {1,...,K}, D = Kd, cells are half-open cubes of side h, J = number of cells, diam(C) = sqrt(D) h.

Scratch scripts and their outputs live under the scoutB5 scratch directory named in the role brief; each numerical check quoted below names its script.

