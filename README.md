Building a RAG Chatbot [Django Framework] 

1. SS of the Chatbot Interface: 

![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.001.png)

2. For the interaction mode where the tutor agent asks the questions, select 5 questions from the above list, and show the full conversation history (as in screenshots) between you and the agent. 

   **Here we go:** 

   **Q.1-2 What organisms are affected by genetic mutations?; What is a mutation?** 

![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.002.png)

Q. 3-4 What factors can make mutations more likely to occur?; Why are insertions and deletions dangerous? 

![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.003.png)

Q.5 How can mutations be passed to offspring? 

![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.004.png)

3. For the interaction mode where the student asks the questions, select 3 from the above list, and show the full conversation history (as in screenshots) between you and the agent. 

**Q. 1. What is a mutation?** 

**Q. 2. When are mutations most likely to occur?** 

![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.005.png)

**Q. 3. Are the results of mutation good or bad?**

![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.006.png)

4. Describe the prompts you’ve tried and what worked and what didn’t work. Include the final prompts you used in the chatbot.  

   Simple prompt: “““You are a tutor helping a student learn about mutations. Explain the concepts in simple terms. """ 

   **Simple prompts** such as this, with just instructing the Chatbot to say that they are a tutor and are helping teach student doesn’t work out very well. The chatbot doesn’t have clear instructions on as to what they can use as methods, type of questions and the source of information.  

   **The prompt that works** (as shown below), is the one that has almost all nuances (helpful tutor, variety of questions, adapting the difficulty, use bullet points, include emojis, highlighting key terms, hiding key terms when helping the student learn. 

   **Final prompts used:** 

1. **For interaction mode “tutor\_asks” (where the chatbot is asking questions)** 

a.  **Prompt:**  

**Interaction\_instructions =**  

""" You are a helpful tutor who asks the student questions about "{topic}". Use a variety of question formats such as open-ended questions, multiple-choice, and fill-in-the-blank to engage the student. Adapt the difficulty based on the student's responses. 

When providing feedback or explanations: 

- Use \*\*bullet points\*\* to list key information. 
- Include relevant \*\*emojis\*\* to make the conversation engaging (e.g., 😊, 🧬, 💡). ![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.007.png)![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.008.png)![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.009.png)
- Highlight important terms by wrapping them with \*\*<strong>\*\* tags for bold text. 
- Keep sentences concise and paragraphs short. 

""" 

2. **For interaction mode “student\_asks” (where the student asks doubts/questions)** 

**a.  Prompt:** 

**Interaction\_instructions =**  

""" 

You are a helpful tutor assisting the student with their questions about "{topic}". Provide thorough explanations, encourage the student, and check for understanding. When answering, provide concise explanations that encourage the student to think critically. Hide key terminologies or concepts in your responses by replacing them with blanks or hints, prompting the student to fill them in. Ask follow-up questions to check for understanding and keep the student engaged. 

When answering: 

- Structure your responses with \*\*bullet points\*\*. 
- Use \*\*emojis\*\* to highlight important points and make learning fun. 
- Emphasize key concepts by wrapping them in \*\*<strong>\*\* tags. 
- Provide examples where possible to aid understanding. 
- Hide key terminologies or concepts in your responses by replacing them with blanks or hints, prompting the student to fill them in. 
- Encourage critical thinking by asking follow-up questions. 

  Keep the tone friendly and engaging. 

  """ 

5\.  Describe your two student personas and the corresponding teacher persona. What 

changes did you include in the prompt that made the agents behave differently? Include full conversation history for two questions and compare them between the two personas.  

**Student 1 Persona: Advanced Student (test1)** 

- **Background**: An advanced student with high prior knowledge in genetics. 
- **Learning Goal**: Preparing for an exam; seeks targeted, in-depth information on mutations. 
- **Preferences**: 
- Enjoys detailed explanations with technical language. 
- Prefers challenging questions that stimulate critical thinking. 
- Interested in recent research and advanced concepts. 

**Student 2 Persona: Beginner Student (test2)** 

- **Background**: A beginner with low prior knowledge about genetics. 
- **Learning Goal**: Learning about mutations for fun; interested in diverse and engaging information. 
- **Preferences**: 
- Prefers simple, clear explanations using everyday language. 
- Enjoys engaging content with analogies and relatable examples. 
- Likes interactive conversations that spark curiosity. 

**Corresponding Teacher Persona** 

The assistant adapts its teaching style based on the student's persona: 

- **For test1**: 
  - Acts as an expert tutor. 
  - Provides in-depth, technical explanations. 
  - Challenges the student with complex questions. 
  - Encourages critical analysis and discussion of advanced topics. 
- **For test2**: 
- Acts as a friendly, approachable tutor. 
- Offers simple, engaging explanations. 
- Uses analogies and relatable examples. 
- Encourages curiosity through interactive questions. 

**Prompts for test 1 tutor:** 

` `**student\_description** = 'an advanced student preparing for an exam on mutations' 

`        `**persona\_instructions** = """ 

- Provide in-depth explanations with technical language and advanced concepts. 
- Challenge the student with complex questions and problems. 
- Encourage critical thinking and analysis. 
- Use academic terminology and reference recent research. 

`        `""" 

**Prompts for test 2 tutor:** 

**student\_description** = 'a beginner learning about mutations for fun' 

`        `**persona\_instructions** = """ 

- Provide simple, clear explanations using everyday language. 
- Keep the content engaging and fun with interesting facts and examples. 
- Use analogies and relatable scenarios to explain concepts. 
- Encourage curiosity and exploration with open-ended questions. 
- Include emojis to make the conversation lively. 

`        `""" 

These prompts were there combined with interaction mode prompts as follows: instructions = f""" {persona\_instructions}  {interaction\_instructions} """ 

**Conversation history:** 

**What is a mutation?** 

**When are mutations most likely to occur?**

Test1 (advanced student):  Test2 (beginner, fun exploring student): 

**Technical words  ![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.010.png)![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.011.png)![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.012.jpeg)![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.013.jpeg)![](Images/Aspose.Words.abc2508d-6d00-40d2-afc0-6f2560752b37.014.png) and descriptions**  

||
| :- |
||
**Some reflection questions:** 

1. **Do you think the chatbot could help someone learn the content better? Why and why not?** 

   Yes, the chatbot can enhance learning by providing **personalized**, interactive assistance tailored to individual student needs. It offers immediate feedback and adapts its teaching style  based  on  the  learner's  prior  knowledge  and  goals.  For  example,  **advanced students receive in-depth explanations** and challenging questions, while **beginners get simplified explanations** and **engaging content**. This personalization can make learning more efficient and enjoyable. However, the chatbot may not fully replicate the nuances of human interaction, such as detecting subtle misunderstandings or providing emotional  support.  Additionally,  its  effectiveness  depends  on  the  quality  of  its programming and the accuracy of its content. 

2. **What specific mechanisms made the chatbot work?** 

The chatbot's effectiveness relies on **tailored prompts** and **conditional logic** that **adjust its behavior based on the user's persona** and **interaction mode**. By defining detailed instructions for different student types and interaction styles, the assistant can modify its language complexity, tone, and teaching strategies accordingly. The use of AI LLM GPT- 4o **enabled natural language processin**g, **allowing the chatbot to generate coherent and contextually appropriate responses**. Techniques such as **using emojis, asking follow-up questions, and providing examples** help keep the conversation engaging and interactive, further enhancing the learning experience. 

3. **If you have more time and resources on this project, what would you like to improve?** 

   With additional time and resources, improvements could include enhancing the **chatbot's ability to detect and respond to the student's emotional cues** or **confusion levels**. Integrating more advanced machine learning algorithms could allow the assistant to adapt dynamically to the student's learning progress over time. Expanding the range of topics and incorporating multimodal elements like images or videos could enrich the content. Additionally, developing a more sophisticated user interface and adding **features like progress tracking**, **personalized feedback**, and interactive quizzes would make the chatbot a more comprehensive educational tool. 

4. **Based on your experience of watching educational videos, what would you like a chatbot to be assisting you with?** 

   A chatbot could significantly enhance the educational video experience by **providing real-time  assistanc**e.  It  could  answer  questions  about  the  content,  clarify  complex concepts, and offer additional resources or examples. The chatbot might **summarize key points, highlight important terms**, and even **test comprehension through interactive quizzes**. Furthermore, it could personalize the learning journey by adjusting explanations based on prior knowledge and interests. This interactivity **would transform passive video watching into an engaging, interactive learning session**, helping to reinforce understanding and retention of the material. 

   **Additional information:** 

   **To achieve this feature: “For structuring the output of the agent. E.g., highlighting important content, and including emojis/bullet points to structure the texts.”** 

   I have used a npm markdown parser and DOMPurify to render HTML output on the User Interface.  THe markdown parser helps in showing \*\*<content> \*\* as **content** and** renders emojis etc. 

   Including user-generated content can pose security risks. Using DOMPurify helps mitigate these risks.** 

- **Security:** Prevents Cross-Site Scripting (XSS) attacks by sanitizing HTML content. 
- **Reliability:** Ensures that only safe HTML is rendered in the user's browser. 

**Thank you!** 
