import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)


def openai_parse_funding_references(authors, funding_statement):
    schema = {
        "type": "object",
        "properties": {
            "funding_references": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "funder": {
                            "type": "string"
                        },
                        "award_type": {
                            "type": "string",
                            "enum": ["award", "contract", "crowdfunding", "endowment", "equipment", "facilities", "fellowship", "grant", "loan", "other", "prize", "salary-award", "secondment", "seed-funding", "training-grant"]
                        },
                        "funding_identifier": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "funding_scheme": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "associated_authors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string"
                                    },
                                    "associated_projects": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    }
                                },
                                "required": ["name", "associated_projects"]
                            }
                        }
                    },
                    "required": ["funder", "award_type", "funding_identifier", "associated_authors"]
                }
            }
        },
        "required": ["funding_references"]
    }

    prompt = """ 
**Task Overview:**
1. **Detailed Entity Recognition:**
   1.1. Explicitly identify each funding organization, grant program or funding scheme, and funded project in the text.
   1.2. Extract all grant or award numbers, ensuring no numeric or alphanumeric identifiers are overlooked.
   1.3. Clearly connect each funding organization and grant program to its specific identifiers and projects, focusing on their exact placement in the text.
   1.4. Preserve funding references without specific identifiers or projects.

2. **Author-Project-Funding Linkage:**
   2.1. Where no authors are explicitly associated with funding or a project (e.g. this study/work/project was supported by), associated ALL authors in the input with the funding.
   2.2. Verify that you associated associated ALL authors in the input with the funding where no authors are explicitly associated with funding or a project
   2.3. Where an author is identified directly associate them with specific projects or studies as mentioned.
   2.4. Accurately map each author to their corresponding funding sources, paying close attention to the proximity and sequence of author names and funding details.
   2.5. Validate the recognition of author names, ensuring complete accuracy and avoiding misinterpretation of non-author text elements.
   2.6. Precisely match author initials or abbreviations to full names, cross-referencing with the text for verification.


3. **Enhanced Pattern Recognition for Funding Details:**
   3.1. Thoroughly extract project/study titles from the acknowledgment text, distinguishing them from any general statements.
   3.2. Implement a robust review process to confirm that all entities labeled as funding identifiers match known grant or award number formats.

4. **In-Depth Association Analysis:**
   4.1. Conduct a comprehensive analysis of the acknowledgment text to establish clear relationships between authors, projects, and funding sources.
   4.2. Utilize both text proximity and logical reasoning to form accurate associations between funding identifiers, authors, and their respective projects or studies.

   5. **Award Type Identification:**
   5.1. Determine the type of award from the following predefined list: ["award","contract","crowdfunding","endowment","equipment","facilities","fellowship","grant","loan","other","prize","salary-award","secondment","seed-funding","training-grant"]
   5.2. Default to "award" where no clear category can be identified.

6. **Output Format:**
   6.1. Format the output as JSON with the structure:
      ```json
      {
        "funding_references": [
          {
            "funder": "{funder name}",
            "award_type": "{award type}",
            "funding_identifier": ["{funding identifier}", "{...}"],
            "associated_authors": [
              {
                "name": "{author name}",
                "associated_projects": ["{project name}", "{...}"]
              },
              {...}
            ]
          },
          {...}
        ]
      }
      ```

7. **Input Processing:**
   7.1. Receive and analyze the list of authors and the funding acknowledgment statement.
   7.2. Parse the input text for entity extraction, author-project association, funding identifier, and award type categorization.

---

For example, for the following authors:

Elena Rodriguez; Marco Fischer; Nina Patel; Arjun Singh; François Lemaire; Clara Moreno; Yuki Tanaka; Paul Henderson; Isabel Santos

and funding statement:

This research was supported by the German Environmental Foundation through the BIOCLIMA project, the German Ministry of Education and Research, and the EU's Horizon 2020 Programme under grant agreement No. H2020-ENV-2019-2-776661. Fieldwork was carried out by the German environmental NGO GreenSteps and processed under the auspices of the European Centre for Marine Ecosystems (ECME-Germany) in Bremen. This study also benefited from a brief research visit by I. Santos to the Institute for Coastal Marine Science (ICMS) in Hamburg, funded by the "Heinrich Hertz" Fellowship Program of the German Ministry of Science and Education (reference: HHFP2020/35).

you would apply the following tasks:

1. **Detailed Entity Recognition:**
   - 1.1: Identified funding organizations: German Environmental Foundation, German Ministry of Education and Research, EU's Horizon 2020 Programme.
   - 1.2: Funding identifiers: "H2020-ENV-2019-2-776661", "HHFP2020/35".
   - 1.3: Connection of funders to projects and identifiers:
     - German Environmental Foundation → BIOCLIMA project.
     - EU's Horizon 2020 Programme → Grant No. H2020-ENV-2019-2-776661.
     - German Ministry of Science and Education → "Heinrich Hertz" Fellowship (Ref. HHFP2020/35).

2. **Author-Project-Funding Linkage:**
   - 2.1 & 2.2: All authors associated with BIOCLIMA and EU's Horizon 2020 funding.
   - 2.3 & 2.4: Isabel Santos specifically associated with the "Heinrich Hertz" Fellowship.
   - 2.5 & 2.6: Accurate recognition of "I. Santos" as Isabel Santos.

3. **Enhanced Pattern Recognition for Funding Details:**
   - 3.1: Project titles extracted: "BIOCLIMA".
   - 3.2: Confirmed formats for "H2020-ENV-2019-2-776661" and "HHFP2020/35".

4. **In-Depth Association Analysis:**
   - 4.1: **Comprehensive Analysis**:
     - **BIOCLIMA project**: Funded by the German Environmental Foundation. All authors are associated with this project due to the general statement of support for the research.
     - **EU's Horizon 2020 Programme**: Supports the overall research with a specific grant (H2020-ENV-2019-2-776661). All authors are implicitly linked to this funding source, as it's not tied to a specific sub-project or individual.
     - **"Heinrich Hertz" Fellowship**: Specifically supports Isabel Santos' visit to the ICMS. This is a direct and explicit author-to-funding linkage.
   - 4.2: **Logical Association**:
     - The funding by the German Environmental Foundation and the EU's Horizon 2020 Programme is assumed to support the entire research team, as there is no indication of specific individuals or sub-projects within the broader research.
     - The "Heinrich Hertz" Fellowship's direct mention of Isabel Santos establishes a clear, individual association.

5. **Award Type Identification:**
   - 5.1: EU's Horizon 2020 Programme identified as a "grant"; "Heinrich Hertz" identified as a "fellowship".
   - 5.2: BIOCLIMA project associated with a "grant" from the German Environmental Foundation.

6. **Output Format:**
   - 6.1: JSON structure for output.

### JSON Output:

```json
{
  "funding_references": [
    {
      "funder": "German Environmental Foundation",
      "award_type": "grant",
      "funding_identifier": [],
      "funding_scheme": ["BIOCLIMA"],
      "associated_authors": [
        {"name": "Elena Rodriguez", "associated_projects": ["BIOCLIMA"]},
        {"name": "Marco Fischer", "associated_projects": ["BIOCLIMA"]},
        {"name": "Nina Patel", "associated_projects": ["BIOCLIMA"]},
        {"name": "Arjun Singh", "associated_projects": ["BIOCLIMA"]},
        {"name": "François Lemaire", "associated_projects": ["BIOCLIMA"]},
        {"name": "Clara Moreno", "associated_projects": ["BIOCLIMA"]},
        {"name": "Yuki Tanaka", "associated_projects": ["BIOCLIMA"]},
        {"name": "Paul Henderson", "associated_projects": ["BIOCLIMA"]},
        {"name": "Isabel Santos", "associated_projects": ["BIOCLIMA"]}
      ]
    },
    {
      "funder": "EU's Horizon 2020 Programme",
      "award_type": "grant",
      "funding_identifier": ["H2020-ENV-2019-2-776661"],
      "funding_scheme": [],
      "associated_authors": [
        {"name": "Elena Rodriguez", "associated_projects": []},
        {"name": "Marco Fischer", "associated_projects": []},
        {"name": "Nina Patel", "associated_projects": []},
        {"name": "Arjun Singh", "associated_projects": []},
        {"name": "François Lemaire", "associated_projects": []},
        {"name": "Clara Moreno", "associated_projects": []},
        {"name": "Yuki Tanaka", "associated_projects": []},
        {"name": "Paul Henderson", "associated_projects": []},
        {"name": "Isabel Santos", "associated_projects": []}
      ]
    },
    {
      "funder": "German Ministry of Science and Education",
      "award_type": "fellowship",
      "funding_identifier": ["HHFP2020/35"],
      "funding_scheme": ["Heinrich Hertz Fellowship"],
      "associated_authors": [
        {"name": "Isabel Santos", "associated_projects": ["Heinrich Hertz Fellowship"]}
      ]
    }
  ]
}
```
---

Now, parse the following funding statement using ALL of the outlined tasks. Return the funder names, identifiers, authors, and associated projects using the following output format:
```json
    {
      "funding_references": [
        {
          "funder": "{funder name}",
          "award_type": "{award type}",
          "funding_identifier": ["{funding identifier}", "{...}"],
          "funding_scheme": ["{funding scheme}", "{...}"],
          "associated_authors": [
            {
              "name": "{author name}",
              "associated_projects": ["{project name}", "{...}"]
            },
            {...}
          ]
        },
        {...}
      ]
    }
  ```
Input:
"""
    content = f'{prompt} Authors: "{authors}" | Funding statement: "{funding_statement}"'
    # try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a named-entity recognition agent tasked with extracting the names of funders and the corresponding grant IDs from the provided text"},
            {"role": "user", "content": content}
        ],
        functions=[{"name": "extract_funding_info", "parameters": schema}],
        function_call={"name": "extract_funding_info"},
        temperature=1
    )
    entities = response.choices[0].message.function_call.arguments
    return entities
    # except Exception:
    #     return None
