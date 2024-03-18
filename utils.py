#done
call_intro = ''' 
Answer the question that the prospect has regarding how they start their calls. Otherwise have a conversation with the prospect about how they can effectively develop rapport in the first phase of their call. Your goal is to give them feedback on how to kick off their sales calls with concrete suggestions of language they can use on their calls. 

Go back and forth with the prospect to ensure they can develop rapport with confidence, and provide suggestions. At the end of the conversation, provide a “cheat sheet” with all of your suggestions on how to start sales calls.
'''

#done
discovery = '''
Your job is to have a conversation with the prospect about asking better questions throughout the call. First, answer the direct question that the student has about asking good questions in the beginning phase of the call.

Then, your goal is to give them feedback on their questions and make suggestions on asking questions that drive the conversation forward. Go back and forth with the prospect to make sure you capture all of their questions, and provide suggestions on each of them. At the end of the conversation, provide a “cheat sheet” with all of their questions and your suggestions on how to improve them.
'''
#done
transition = '''
Your job is to have a conversation with the prospect about transitioning to pitching their offering once they are done with introduction and discovery. First, answer the direct question that the student has about transitioning into the pitching phase.

Your goal is to give them feedback on how to transition with concrete suggestions of language they can use on their calls. After answering their question, go back and forth with the prospect to make sure you have a comprehensive transition strategy, and provide suggestions. At the end of the conversation, provide a “cheat sheet” with your suggestions on how to transition effectively.
'''
#done
pitching = '''
Answer the students question regarding their pitch. Once you answer their question, your job is to have a conversation with the prospect about crafting and delivering an effective pitch. Your goal is to give them feedback on how to pitch with concrete language suggestions they can use on their calls. Explain the pitch codex as a concept while you are helping the prospect craft their pitch. 

Go back and forth with the prospect to make sure you create their pitch, and once their pitch is in a good place, provide suggestions on how to deliver their pitch. At the end of the conversation, provide a summary of their new pitch and how to deliver it.
'''

closing = '''
Answer the students' questions regarding closing. Once you answer their question, your job is to have a conversation with the prospect about how they can close their prospects more effectively. Your goal is to give them feedback on specific closing actions that they can take. 

Go back and forth with the prospect to make sure you have a comprehensive closing strategy. At the end of the conversation, provide a “cheat sheet” with all of their closing actions you recommended for them.
'''

objection_handling = '''
Answer the students' questions regarding the objections they face. Once you answer their question, your job is to have a conversation with the prospect about the typical objections they face. Your goal is to give them feedback on how to handle them with concrete suggestions of language they can use on their calls. 

Go back and forth with the prospect to make sure you capture all of their objections, and provide suggestions on each of them. At the end of the conversation, provide a “cheat sheet” with all of their objections and your suggestions on how to handle them.
'''

custom_phrases = {
    'call_intro': call_intro,
    'discovery': discovery,
    'transition': transition,
    'pitching': pitching,
    'closing': closing,
    'objection_handling': objection_handling
}

name_to_url = {
    '7FSA Uncertainty Based Objections.txt': 'Uncertainty-Based Objections: This link gives suggestions on how to handle uncertainty-based objections.  https://docs.google.com/document/d/1Ti9lqQ0wbXUeyNkcOyp9VrLMWyNpimj5CvzXUTax9KI/edit?usp=sharing',
    'Reframing Structures & Patterns.txt': 'Reframing Structures & Patterns: This link gives suggestions on how to reframe the objection and patterns associated with objections.  https://docs.google.com/document/d/1a2eorpBbtWu7puxyZfZ7CFGV8TvjlcjIWPZbiY5qd24/edit?usp=sharing',
    'Commit.txt': 'Closing: This video gives an overview of the closing steps in the sales process.  https://drive.google.com/file/d/1ERYFPbwIplv4zyrgxVXH6WILUOKxl2Zi/view',
    '4.1 Pitch Codex Intro.txt': 'Pitch Codex overview: This link gives an introduction to the Pitch Codex.  https://docs.google.com/document/d/1ArphMQ51xLf-SXQIPvAQCu6ZzEIS3qfpSDuBdGsHDYU/edit?usp=sharing',
    'Information Gathering Questions.txt': 'Information Gathering Questions: This link provides suggestions for questions for information gathering purposes. https://docs.google.com/document/d/1dB3d-mtzdzixN5mDG5H9msWDQOJ75T_s58SKWbKyk5U/edit#heading=h.50rifhw9p0bb',
    '4.2 How To Pitch.txt': 'How to deliver your pitch: This link gives suggestions on how to deliver your pitch.   https://docs.google.com/document/d/1z_g1IR33fY1AGGeozfOgK_UWilLdLrCoIkordlms4Y0/edit',
    '4.2 Pacing First Objection.txt': 'Pacing the first objection: This link gives suggestions on how to pace the first objection.  https://docs.google.com/document/d/10heWk59hFYlivBFH89Qgs5EPLAiQCVzK9pQooFFdOGU/edit',
    '3.6 Call Syntax #2 - Goals First.txt': 'Goals-First Sales: This link provides suggestions for questions for understanding the goals of the prospect. https://docs.google.com/document/d/1mRrf_d-ewFV13VF7ujuYpMk91IL16LNyDq25QcshQNI/edit?usp=sharing',
    '3.3 Call Syntax #1_ Problem First v2.txt': 'Problem-First Sales: This link provides suggestions for questions for understanding the problems and challenges that the prospect is facing. https://docs.google.com/document/d/1JpNdX47L72CakDq2GGYA2Hv0D0jhI2vMdSXwZCV6rQM/edit?usp=sharing',
    '4.3 - Financial Objections.txt': 'Financial objections: This link gives suggestions on how to handle financial objections.  https://docs.google.com/document/d/1_1bE9f4XDDiGr829WvJywxslXDYnuJc7ctq3JW4rOzQ/edit?usp=sharing',
    '3.10 Transition Phase Basic.txt': 'Transition to Pitching: This video gives an overview of Cole’s suggestions on how to transition into pitching your offer. https://drive.google.com/file/d/1jLDRs2dpyWGH827NdKvs29RnVo-XL6L-/view',
    '2.4 Pitch Creation Worksheet.txt': 'How to create your pitch: This link gives an interactive overview on how to create your pitch.  https://docs.google.com/document/d/1EnWyDdoMb6yHXGgKkYYwagc5f77UC2z_xKY7GjuTfig/edit',
    '4.4 Support Objections.txt': 'Partner/Spouse Objections: This link gives suggestions on handling partner/spouse objections.  https://docs.google.com/document/d/1kBNpSUxUsS2ryRne4Lbfp8bG-o6X2uwnkCQEOeGXEOE/edit?usp=sharing',
    '3.4 Call Introduction.txt': 'Call Introduction: This link goes over best practices for the start of the call.  https://docs.google.com/document/d/1K_mHEC1aiDGXjwcrOPz2z6dkWcwSYQfq8QIE-RxqrIQ/edit?usp=sharing'
}
