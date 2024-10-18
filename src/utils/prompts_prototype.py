def get_summary_prompt(legal_text, case_type=None, decision_focus=False):
    """
    Devuelve un prompt para resumir un documento legal, enfocándose en puntos clave y decisiones.
    :param legal_text: El documento legal extenso a resumir.
    :param case_type: Tipo opcional de caso (ej., derecho contractual, derecho penal) para dar contexto.
    :param decision_focus: Indicador booleano para señalar si debe enfocarse especialmente en la decisión del tribunal.
    """
    case_context = f" en un contexto de {case_type}" if case_type else ""
    decision_instructions = " Enfócate especialmente en la decisión del tribunal." if decision_focus else ""
    
    return f"""
    Como asistente legal especializado en resumir textos legales{case_context}, resume el siguiente documento legal, extrayendo los puntos clave más importantes, los argumentos legales y las decisiones.{decision_instructions}

    Documento:
    \"{legal_text}\"

    Por favor, organiza tu resumen en formato de viñetas con títulos claros:
    
    ## :blue[Puntos Clave Legales]
    - **Punto 1**: [Resumen del punto clave]
    - **Punto 2**: [Resumen del punto clave]
    [Agrega más puntos según sea necesario]
    
    ## :green[Decisiones y Fallos]
    - **Decisión 1**: [Resumen de la decisión o fallo del tribunal]
    [Agrega más decisiones según sea necesario]

    ## :orange[Notas Adicionales]
    - **Nota 1**: [Contexto adicional, si es necesario]
    """

def get_draft_prompt(document_type, clauses=None, template=None):
    """
    Devuelve un prompt para generar un borrador de un documento legal a partir de una plantilla personalizable, con sugerencias de cláusulas legales.
    :param document_type: Tipo de documento legal (ej., contrato, acuerdo, demanda).
    :param clauses: Lista opcional de cláusulas legales específicas para incluir.
    :param template: Plantilla o estructura opcional para el documento.
    """
    clause_instructions = ""
    if clauses:
        clause_instructions = "\n".join([f"- **Cláusula {i+1}**: {clause}" for i, clause in enumerate(clauses)])

    template_instructions = f"\nPlantilla: \"{template}\"" if template else ""
    
    return f"""
    Como asistente experto en redacción legal, crea un {document_type} utilizando la siguiente plantilla personalizable e incluye las cláusulas legales apropiadas:

    {template_instructions}

    A continuación, algunas cláusulas recomendadas para incluir:
    {clause_instructions}

    Proporcione su respuesta en formato markdown como se indica a continuación:

    ## :blue[Borrador de {document_type}]
    - **Introducción**: [Proporcione una introducción formal]
    - **Cláusula 1**: [Contenido de la cláusula legal]
    - **Cláusula 2**: [Contenido de la cláusula legal]
    [Agregue más cláusulas según sea necesario]

    ## :green[Cláusulas Sugeridas]
    {clause_instructions}

    ## :orange[Notas]
    - **Nota 1**: [Cualquier nota o contexto importante sobre el documento redactado]
    """

def get_legal_research_prompt(query):
    """
    Returns a prompt for finding relevant case law or legal precedents in response to a legal query.
    """
    return f"""
    Eres un asistente legal avanzado especializado en la Ley Argentina. Dada la siguiente consulta legal, por favor busca y presenta jurisprudencia relevante y analiza los precedentes que se aplican al caso.

    Consulta legal:
    "{query}"

    Proporcione su respuesta en el siguiente formato:

    ## :blue[Jurisprudencia relevante]
    - **Caso 1**: [Descripción del caso relevante]
    - **Caso 2**: [Descripción del caso relevante]
    [Agregue más casos según sea necesario]

    ## :green[Análisis de precedentes]
    - **Precedente 1**: [Explicación de cómo este precedente aplica a la consulta]
    - **Precedente 2**: [Explicación de cómo este precedente aplica a la consulta]
    [Agregue más precedentes según sea necesario]

    ## :orange[Conclusiones]
    - [Conclusión basada en los casos analizados]
    """