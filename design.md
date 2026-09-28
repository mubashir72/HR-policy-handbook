# UI/UX direction

## Experience

Use a calm, readable single page layout that puts the document and answer first. The tone should be clear and helpful for HR questions without implying that the assistant makes official decisions.

## Page structure

1. **Header:** “HR Policy Assistant” and one sentence explaining that answers come from the uploaded policy PDF.
2. **Document panel:** PDF uploader, accepted file guidance, current filename, page count, and progress or ready state. A replacement upload clearly starts a fresh document session.
3. **Conversation area:** Chat history with distinct user and assistant messages. The question input is disabled or explains what is missing until a document is indexed.
4. **Answer evidence:** Short answer first, followed by page references. A collapsed “Source excerpts” section shows the actual retrieved passages with page labels.
5. **Status and errors:** Inline messages next to the action that failed, written in plain language with a useful next step.

## Visual direction

- Prefer Streamlit's native components and theme options. Use generous spacing, a restrained neutral palette with one accent color, and strong text contrast.
- Keep line lengths comfortable on desktop and ensure the uploader, chat input, and evidence section work on narrow screens.
- Distinguish facts from uncertainty: use explicit language such as “I couldn't find this in the uploaded policy” when evidence is insufficient.
- Use visible labels for controls. Do not rely on color alone for loading or error states.

## Key states and microcopy

| State | Intended message |
| --- | --- |
| No document | “Upload an HR policy PDF to get started.” |
| Indexing | “Reading and indexing your policy…” |
| Ready | “Ready to answer questions about [filename].” |
| No extractable text | “This PDF has no readable text. Please upload a text based PDF.” |
| Missing API key | “A Groq API key is required to generate an answer.” |
| Unsupported answer | “I couldn't find enough information in this policy to answer that.” |

Page references should be easy to scan, such as “Page 4,” and source excerpts should remain clearly associated with their page. Avoid showing raw embedding scores unless debugging is explicitly enabled.
