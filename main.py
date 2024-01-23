from aifuncs import initialize_all_vdbs, generate_cole_response

##### EXAMPLE #####
#initialize all vector databases
call_intro = initialize_vdb('call_intro')
goal_first_or_problem_first = initialize_vdb('goal_first_or_problem_first')
objection_handling = initialize_vdb('objection_handling')
pitch = initialize_vdb('pitch')
skilled_questions = initialize_vdb('skilled_questions')
unknown_or_NA = None #initialize_vdb('unknown_or_NA')

dbs = {
    "call_intro": call_intro,
    "goal_first_or_problem_first": goal_first_or_problem_first,
    "objection_handling": objection_handling,
    "pitch": pitch,
    "skilled_questions": skilled_questions,
    "unknown_or_NA": unknown_or_NA
}

file_path = 'prompts/answer_prompt.txt'
with open(file_path, 'r') as file:
    prompt = file.read()

outbound = "Hi there, I'm Cole. CEO of Closers.io. I'm here to help you with your sales calls. What's your question?"
inbound = ""
messages = []

while inbound != "Exit":
    print("###################################################")
    inbound = input("Cole: " 
                    + outbound 
                    + "\n###################################################"
                    +'\nYou: ')
    
    if inbound == "Exit":
        break
    
    #append user input to messages
    messages.append({"role": "user", "content": inbound})

    #classify inquiry
    topic = which_rag(messages, "gpt-3.5-turbo")

    #get appropriate vector database
    if topic != 'unknown_or_NA':
        db = dbs[topic]

        #do similarity search and get examples
        examples = find_examples(db, inbound)

        #format custom system prompt
        prompt = prompt + examples

    custom_prompt = {"role": "system", "content": prompt}

    #format messages for response generation
    llm_messages = [custom_prompt, *messages]

    #generate response
    outbound = generate_response(llm_messages, "gpt-4-1106-preview")

    #colify
    outbound = colify(messages, outbound)

    if outbound:
        messages.append({"role": "assistant", "content": outbound})

    else:
        print("Sorry man, I'm late to a meeting. Just hit me up on Telegram!")
        break