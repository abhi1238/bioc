




from agents import function_tool
import logging

logger = logging.getLogger("uvicorn.error")

@function_tool(
    name_override="readme_tool",
    description_override="""
    Returns a Markdown summary of all major BioChirp features, core capabilities, supported query types, and example usage.
    Call this tool if the user asks about what BioChirp can do, how to use it, supported queries, or wants to see a guide to its features.
    """
)
async def readme_tool() -> str:
    """
    Returns a well-structured Markdown summary of BioChirp's key features, supported queries, and output formats.
    Provides a user-friendly fallback message if any error occurs.
    """
    logger.info("[RUNNING] readme tool")
    # print("[Running] readme tool")

    try:

        logger.info("[FINISHED] readme tool")

        
        return (
            "#  BioChirp: Conversational Retrieval of Biomedical Data\n\n"
            "BioChirp is an open-source conversational agent for biomedical research and clinical data science. "
            "You can query trusted biomedical databases using **plain language** and receive structured, explainable answers. "
            "BioChirp handles drugs, genes, diseases, pathways, targets, and even ambiguous or rare biomedical terms.\n\n"

            "##  Core Features\n"
            "- **Natural language** queries—no SQL or code required\n"
            "- **Synonym, abbreviation, and acronym expansion** (finds results even if you use alternative terms)\n"
            "- **Multi-database search**: TTD, CTD, HCDT, and more\n"
            "- **Schema-aware retrieval**: Only relevant columns/fields, across sources\n"
            "- **Context fallback**: For ambiguous or unknown terms, BioChirp searches the biomedical literature/web for clarification\n"
            "- **Export options**: Interactive tables, CSV download, summaries\n"

            "##  Example Queries\n"
            "- List all approved drugs for asthma\n"
            "- What drugs treat TB?\n"
            "- Find pathways for BRCA1 targets\n"
            "- What is the mechanism of action for imatinib?\n"
            "- Expand gene synonyms for EGFR\n"
            "- What does 'PCOS' stand for?\n"
            "- Show clinical trials for a given drug or disease\n"

            "##  Output Formats\n"
            "- Interactive tables (in chat)\n"
            "- Downloadable CSVs\n"
            "- Explanatory summaries and highlights\n"

            "##  Usage Tips\n"
            "- Use common names, official terms, or abbreviations (e.g., 'BRCA1', 'imatinib', 'COPD')\n"
            "- BioChirp will clarify or search for any unfamiliar term automatically\n"
            "- For complex tasks, you can ask for details about drugs, genes, diseases, targets, or recent biomedical literature\n"
        )
    except Exception:

        logger.exception("[readme tool] Error returning output from readme.")

        return (
            "# BioChirp: Capabilities Unavailable\n\n"
            "Sorry, an unexpected error occurred while retrieving BioChirp's feature summary. "
            "Please try again later or contact the support team if this issue persists."
        )