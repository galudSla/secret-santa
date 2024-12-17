import gradio as gr
from functions import send_emails, santa_pick, chatgpt_recommendation 


with gr.Blocks() as demo:
    gr.Markdown(
    """
    # Secret Santa Generator!
    ## Type the name and the email of each participant   
    #### Optionally you can add information about each person to get gift recommendations.  
    ## Get the secret result in your email
    """)
    text_count = gr.State(1)
    add_btn = gr.Button("CLICK TO ADD USER")
    add_btn.click(lambda x: x + 1, text_count, text_count)

    @gr.render(inputs=text_count)
    def render_count(count):
        names = []
        emails = []
        infos = []
        for i in range(count):
            with gr.Row():
                with gr.Column(): 
                    name = gr.Textbox(key=f"name-{i}", label=f"Name {i+1}")
                    email = gr.Textbox(key=f"email-{i}", label=f"Email {i+1}")
                    
                with gr.Column():
                    info = gr.Textbox(value='', key=f"info-{i}", label=f"Information {i+1} (could be left blank)")
            
            names.append(name)
            emails.append(email)
            infos.append(info)

        def santa_run(*data):
            names = data[:count]
            emails = data[count:2*count]
            infos = data[2*count:]
            participants = {names[i]: {'email': emails[i], 'gift_prompt': infos[i]} for i in range(count)}
            
            participants = santa_pick(participants)
            participants = chatgpt_recommendation(participants)
            send_emails(participants)
            
            return 'Santa has completed his mission.'

        santa_btn.click(santa_run, inputs=names + emails + infos, outputs=output)

    santa_btn = gr.Button("START SECRET SANTA")
    output = gr.Textbox(label="Output")


demo.launch(debug=True)