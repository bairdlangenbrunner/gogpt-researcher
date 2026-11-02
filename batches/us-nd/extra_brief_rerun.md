## Second pass: read the harvested permit documents

This is a second pass on this plant. The first pass did not read the permit documents that were already harvested to disk. Read scopes/us-nd/work/permits/<plant id>.md before anything else.

The live deq.nd.gov/AQ/Notices/ PDF addresses now return the state's web page instead of the PDF, so the lines extracted from them in that file are web page markup. Ignore them. The same documents are in CERIS-ND as ceris.deq.nd.gov/ext/ncore/downloadpdf/<id> links, already in the local fetch cache: read them with `python scripts/fetch.py <url> --text` and verify them with url_verifier.py. Cite the CERIS link. The Wayback Machine was offline earlier; try it again for any notice PDF that has no CERIS copy.

For Bison Generation Station: the final Permit to Construct ACP-18273 v1.0 (December 2025) and its technical support document name the turbines (Mitsubishi M501JAC, one-on-one combined cycle blocks with duct burners), the total output (up to 1,490 MW) and the site address. Use them for Equipment Manufacturer/Model, capacity per block and the location step.

For Applied Digital FAR Generation Plant (Harwood): check which permits in the file are for the Harwood campus and which are for Ellendale (ELN). Use the Harwood ones for Number Of Engines, Capacity Per Engine, the engine make and model and the fleet total. If no Harwood permit exists in CERIS or the notices, say so in words.
